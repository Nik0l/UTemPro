# Calculating statistics on Q&A communities. Includes temporal statistics ( for example, how many questions were asked in a period), spatial statistics, number of users, questions, answers.
__author__ = 'nb254'
import numpy
import operator
import csv
import sqlite3
import pandas as pd
from collections import Counter
import re

def PrintStat(posts):
   # clean up outliers
   print "mean number of posts: "   + str(numpy.mean(posts['U_POSTS']))
   print "median number of posts: " + str(numpy.median(posts['U_POSTS']))
   print "max number of posts: "    + str(max(posts['U_POSTS']))
   print "min number of posts: "    + str(min(posts['U_POSTS']))

def TemporalStats(data):
   # statistics
   times = {'hh_less_fr': 0, 'h_less_fr': 0, 'd_less_fr': 0, 'm_less_fr': 0}
   mean_time_m   = numpy.mean(data['mins'])   # mean time
   median_time_m = numpy.median(data['mins']) # median time
   max_time_d    = max(data['days'])          # the longest time of answering in days
   min_time_m    = min(data['mins'])          # the fastest answer in minutes
   total_qs      = data['questions']          # number of questions
   if total_qs > 0:
     times['hh_less_fr'] = float(data['hh_less'] * 100 / total_qs) # % answered faster than in 1 hour
     times['h_less_fr']  = float(data['h_less'] * 100 / total_qs) # % answered faster than in 1 hour
     times['d_less_fr']  = float(data['d_less'] * 100 / total_qs) # % answered faster than in 1 day
     times['m_less_fr']  = float(data['m_less'] * 100 / total_qs) # % answered faster than in 1 month
   print "*****************************************************"
   print "mean: "                        + str(mean_time_m)   + " minutes"
   print "median: "                      + str(median_time_m) + " minutes"
   print "max: "                         + str(max_time_d)    + " days"
   print "min: "                         + str(min_time_m)    + " minutes"
   print "number of questions: "         + str(total_qs)
   print "answered faster than 30 min: " + str(times['hh_less_fr'])    + "%"
   print "answered faster than 1 hour: " + str(times['h_less_fr'])     + "%"
   print "answered faster than 1 day: "  + str(times['d_less_fr'])     + "%"
   print "answered faster than 1 month: "+ str(times['m_less_fr'])     + "%"

def CalcTempStat(filename):
   data = {'questions': 0, 'mins':[], 'hours':[], 'days':[], 'hh_less': 0, 'h_less': 0,'d_less': 0, 'm_less': 0}
   reader  = csv.reader(open(filename), delimiter=',', quotechar='|')
   for row in reader:
     if data['questions'] >= 1:
         time_sec = float(row[-1])  # address the last column (the file format is different)
         if time_sec > 0:
             data['mins'].append(time_sec/(60.0))
             data['hours'].append(time_sec/(60 * 60.0))
             data['days'].append(time_sec/(60 * 60 * 24.0))
             if time_sec < 60 * 30.0:
                 data['hh_less']= data['hh_less']+ 1 # 30 min
                 data['h_less'] = data['h_less'] + 1 # answered faster than in 1 hour
                 data['d_less'] = data['d_less'] + 1 # answered faster than in 1 day
                 data['m_less'] = data['m_less'] + 1 # in 1 month
             elif time_sec < 60 * 60.0:
                 data['h_less'] = data['h_less'] + 1 # answered faster than in 1 hour
                 data['d_less'] = data['d_less'] + 1 # answered faster than in 1 day
                 data['m_less'] = data['m_less'] + 1 # in 1 month
             elif time_sec < 60 * 60 * 24.0:
                 data['d_less'] = data['d_less'] + 1 # answered faster than in 1 day
                 data['m_less'] = data['m_less'] + 1 # 1 month
             elif time_sec < 60 * 60 * 24.0 * 30:
                 data['m_less'] = data['m_less'] + 1
     data['questions'] = data['questions'] + 1
   TemporalStats(data)
   return data


def GetPostsPerUser(filename):
   """ input file has one column of the number of questions per each user """
   posts_data  = pd.read_csv(filename)
   posts_users = list(posts_data['count(posts.OwnerUserId)'])
   posts_stats = dict(Counter(posts_users))
   return posts_stats

def GetQuesAnsByMonth(filename):
   """ input file has two column, when a post was created and what kind of post is it: 1 for questions and 0 for answers """
   allDates = dict()
   lines = csv.reader(open(filename), delimiter=',')
   for line in lines:
        Q = 0
        A = 0
	date = line[0][:7]
	if(line[1] == '1'):
		Q = 1
		A = 0
	elif(line[1] == '2'):
		Q = 0
		A = 1
	QandA    = allDates.get(date, [0, 0])
	QandA[0] = QandA[0] + int(Q)
	QandA[1] = QandA[1] + int(A)
	allDates[date] = QandA
   #print(allDates)
   sorted_dates = sorted(allDates.iteritems(), key=operator.itemgetter(0), reverse=False)
   #print(sorted_dates)
   QandA  = []
   data = {'questions': [], 'answers': [], 'labels': []}
   # creating two lists of y-values
   for date,QandA in sorted_dates:
	data['questions'].append(QandA[0])
	data['answers'].append(QandA[1])
	data['labels'].append(date)
   return data

def CalcPeople(sorted_counts):
      print sorted_counts
      total_questions = 0
      total_people    = 0
      for stat in sorted_counts:
         try:
            total_questions = total_questions + int(stat[0])
            total_people    = total_people    + int(stat[1])
         except ValueError:
            print stat[0]
            print stat[1]
      print total_questions
      print total_people

def SavePostLength(data, filename, ATTRIBUTE):
   """ counts occurance of a value and makes a dictionary: used for counting how many posts have particular number of characters in their body or title"""
   xs = []
   ys = []
   length_stat = dict(Counter(data[ATTRIBUTE]))
   xs  = list(length_stat)
   for x in xs:
      ys.append(length_stat[x])
   print xs
   print ys
   print "number of bars:", str(len(xs))
   #saving the data
   myfile = open(filename, 'wb')
   wr = csv.writer(myfile, quoting=csv.QUOTE_ALL)
   wr.writerow([ATTRIBUTE, 'number_of_posts'])
   i = 0
   for elem in xs:
      wr.writerow([elem, ys[i]])
      i = i + 1

def SaveBodyTitleStat(filename, filenames):
   """ input file has NLP features but only BODY_LENGTH and TITLE_LENGTH are of interest """
   data = pd.read_csv(filename)
   SavePostLength(data, filenames['posts_length'], 'BODY_LENGTH')
   print "total posts:", str(len(data))
   questions = data[data.QorA == 1]
   print "questions: ", str(len(questions))
   SavePostLength(questions, filenames['questions_length'], 'BODY_LENGTH')
   SavePostLength(questions, filenames['questions_t_length'], 'TITLE_LENGTH')
   answers = data[data.QorA == 2]
   print "answers: ", str(len(answers))
   SavePostLength(answers, filenames['answers_length'], 'BODY_LENGTH')

def PostsRepNormalized():
   ''' calculate posts per user where users are ranked by their reputation'''
   #result_answers = once(lambda: runquery(c,'''SELECT count(posts.Id), users.Id, users.DisplayName, users.Reputation from users, posts where posts.OwnerUserId=users.Id and posts.postTypeId=2 GROUP BY users.Id ORDER BY users.Reputation DESC'''))
   result_answers = [[1],[2],[3],[5],[3],[1],[2],[4],[6],[7],[5],[3],[4]]
   xs    = []
   ys    = []
   total = 0
   index = 0

   for row in result_answers:
	total = total + int(row[0]) # number of posts
	xs.append(index) # rank by reputation
	ys.append(total)
	index = index + 1
   print("found %d  total answers" % total)

   #normalize
   xs_norm = []
   ys_norm = []
   for x in xs:
	xs_norm.append(float(x) * 100 / index) # number of posts
   for y in ys:
	ys_norm.append(float(y) * 100 / total) # users ranked by their reputation
   data = {'RANK': xs, 'POSTS_NUM': ys_norm}
   return data

def CountAccAnswers(data):
   num = Counter(data['UserId'])
   num = num.items()
   return num

def UsersBehaviour(stats):
  print stats
  #print float(stats['q']) / 10
  data = {'nothing': 0, 'questions_only': 0, 'answers_only': 0, 'votes_only': 0, 'qanda': 0, 'qandv': 0, 'vanda': 0, 'all': 0}
  data['questions_only'] = float(stats['q'] - stats['qa'] - stats['qv'] + stats['qva']) / float(stats['u'])*100;
  print("Percentage of users who asked questions only: %f"% data['questions_only'])
  data['answers_only'] = float(stats['a'] - stats['qa'] - stats['av'] + stats['qva']) / float(stats['u'])*100;
  print("Percentage of users who answered questions only: %f"% data['answers_only'])
  data['votes_only'] = float(stats['v'] - stats['qv'] - stats['av'] + stats['qva']) / float(stats['u'])*100;
  print("Percentage of users who voted only: %f" % data['votes_only'])
  data['qanda'] = float(stats['qa'] - stats['qva']) / float(stats['u'])*100;
  print("Percentage of users who asked and answered only: %f"% data['qanda'])
  data['qandv'] = float(stats['qv'] - stats['qva']) / float(stats['u'])*100;
  print("Percentage of users who asked and voted only: %f"% data['qandv'])
  data['vanda'] = float(stats['av'] - stats['qva']) / float(stats['u'])*100;
  print("Percentage of users who answered and voted only: %f"% data['vanda'])
  data['all'] = float(stats['qva'])/float(stats['u'])*100;
  print("Percentage of users who asked, answered and voted: %f" % data['all'])
  combined = data['questions_only'] + data['answers_only'] + data['votes_only'] + data['qanda'] + data['qandv'] + data['vanda'] + data['all']
  data['nothing'] = 100.0 - combined
  print("People who signed up and did nothing: %f" % data['nothing'])
  return data

def PostTitleLength(filename):
   p=re.compile('<[^>]*>')
   allLengths = dict()
   lines = csv.reader(open(filename), delimiter=',')
   next(lines, None)
   data = {'questions': [], 'answers': [], 'titles': []}
   # CSV file in following form:
   # title length :: question length :: num answers :: body
   for line in lines:
	titleLen = line[0]
	quesLen  = line[1]
	numAns   = line[2]
	#body     = line[3]

	#clean up missing data in CSV file
	if titleLen=="":
		titleLen = 0
	if quesLen=="":
		quesLen  = 0
	if numAns=="":
		numAns   = 0

	#make three lists of values
 	if titleLen > 0:
	 	data['titles'].append(int(titleLen))
	# 	questions.append(int(quesLen))
		shortenedString=p.sub('', line[3])
		data['questions'].append(len(shortenedString))
	 	data['answers'].append(int(numAns))
   return data
