__author__ = 'nb254'
#requires question_title_length.csv for processing: TITLE, BODY, POSTID, USERID
import nltk, csv
import pandas as pd
import Features as features
#test = "<p>I have an original Arduino UNO R3 that I bought and an <a href='http://arduino.cc/en/Main/ArduinoBoardSerialSingleSided3' rel='nofollow'>Arduino Severino (S3V3)</a> that I"'"ve built.</p><p>I have no problems uploading sketches to the UNO, but sometimes, when uploading to the Severino board, I have to hard reset it at a specific time during the upload process, when the IDE says something like this below:</p><pre><code>avrdude: Version 5.11, compiled on Sep  2 2011 at 19:38:36 Copyright (c) 2000-2005 Brian Dean, http://www.bdmicro.com/ Copyright (c) 2007-2009 Joerg Wunsch System wide configuration file is C:\arduino-1.0.3\hardware/tools/avr/etc avrdude.conf Using Port:.\COM1 Using Programmer : arduino Overriding Baud Rate : 115200 avrdude: Send: 0 [30]   [20] avrdude: Send: 0 [30]   [20]  avrdude: Send: 0 [30]   [20] </code></pre> <p>If I don"'"t reset it when one of the <code>Send</code> messages are being displayed, I get the <code>not in sync</code> message, as below:</p><pre><code>avrdude: Recv: avrdude: stk500_getsync(): not in sync: resp=0x00</code></pre><p>Other times, if I'm lucky, I can upload to the Severino board without having to reset it.</p><p>So, my questions are:</p><ol><li><p><strong>Why does that happen? Why Severino needs a hard reset during upload?</strong></p></li><li><p><strong>Why is the problem intermitent?</strong> Why does it happen sometimes and others it doesn't?</p></li><li><p><strong>How can I fix that problem?</strong> Is there a simple change to the Severino design that would fix that?</p></li></ol>"


def NLPExtract(data, file_name):
    HEADER = features.KEYS + features.NLP_FEATURES
    # the file where all 'wh' and '?' will be saved
    csv_writer = csv.writer(open(file_name, 'wb'))
    csv_writer.writerow(HEADER)
    i = 0
    #print data
    for index, row in data.iterrows():
       #TODO:  delete the second condition
       if i > 0:
          print row
          res = NLPFeatures(row)
          csv_writer.writerow(res)
       i = i + 1

# counts words of a particular type, for example, 'WP' - 'wh' words
def NLPFeatures(row):
  post_id = row['PostId']
  user_id = row['UserId']
  #print row
  try:
     res = NLPFeaturesCalc(row['Q_Title'], row['Q_Body'])
     res = [post_id, user_id] + res
  except UnicodeDecodeError:
     #TODO: convert to unicode, currently just ignoring the error
     print('UnicodeDecodeError: ' + row['Q_Title'])
     #res    = [post_id, user_id, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
     #title_fixed = row['Q_Title'].encode('utf-8')
     #body_fixed  = row['Q_Body'].encode('utf-8')
     res = [post_id, user_id] + [0]*12
  return res

def NLPFeaturesCalc(title, body):
   num_qm  = 0
   num_wp  = 0
   symbols = ['VBG', 'VBZ', 'VBP', 'VB', 'VBD', 'VBN'] #verbs
   selfRef = ['I','my','myself', 'we', 'We', 'My', 'Myself', 'i'] # self-reference nouns
   # tokens of the title and the body
   tokens  = [nltk.word_tokenize(title), nltk.word_tokenize(body)]
   tagged  = [nltk.pos_tag(tokens[0]), nltk.pos_tag(tokens[1])]
   ############### construct features ############################
   num_qm  = [Count(tokens[0], '?'), Count(tokens[1], '?')] # number of question marks
   num_wp  = [CountP(tagged[0], 'WP'), CountP(tagged[1], 'WP')]# number of 'wh' words
   num_av  = [CountV(tagged[0], symbols), CountV(tagged[1], symbols)] #number of active verbs
   num_sr  = [CountM(tokens[0], selfRef), CountM(tokens[1], selfRef)] #self-reference
   num_url = body.count('<a href=') # how many url links are there
   num_img = body.count('<img') # how many images are there
   num_cst = body.count('<code>') # how many start code blocks
   num_cen = body.count('</code>') # how many end code blocks
   cod_len = CodeLength(body, num_cst, num_cen) # total length of code in chars
   res     = [num_wp[0], num_wp[1], num_qm[0], num_qm[1], num_av[0], num_av[1], num_sr[0], num_sr[1], num_url, num_img, num_cst, cod_len]
   return res

def CountP(data, TYPE):
  num = 0
  for x in data:
     if x[1] == TYPE:
        num = num + 1
  return num
# counts a number of particular words or symbols, for example, '?'
def Count(data, symbol):
  num = 0
  for x in data:
     if x == symbol:
        num = num + 1
  return num

# counts a number of multiple symbols
def CountM(data, symbols):
  num = 0
  for sym in symbols:
     num = num + Count(data, sym)
  return num

# counts a number of multiple symbols
def CountV(data, symbols):
  num = 0
  for sym in symbols:
     num = num + CountP(data, sym)
     #print num
     #print sym
  return num

# checks if it is a substring
def SubString(data, text):
  if text in data:
     return 1
  else:
     return 0

def CodeLength(text, num_cst, num_cen):#text and the number of start and end code blocks
   cod_len = 0
   if num_cst <> num_cen or num_cst * num_cen == 0:
      return cod_len
   else:
      s = text.replace(" ","")
      s = s.replace("</code>"," ")
      s = s.replace("<code>"," ")
      #print s
      s = s.split()
      i = 0
      for line in s:
         if i%2 <> 0:
            cod_len = cod_len + len(line)
         i = i + 1
   #print cod_len
   return cod_len
