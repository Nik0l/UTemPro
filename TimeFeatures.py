# aka Temporal features are calculated here. For example, how many questions a user asked last week, activity of a user on weekends.
__author__ = 'nb254'
import time
import csv
from datetime import date
import Features as feature
from time import mktime
from datetime import datetime

header_w = feature.KEY + feature.TIME_FEATURES

QUESTIONID_INDEX    = 0
TIME_ASKED_INDEX    = 5
TIME_ANSWERED_INDEX = 6

def DataWeekend(data):
   data_w = []
   i = 0
   for row in data:
       if i>0:#ignore the header
          sq = row[TIME_ASKED_INDEX].replace("T", " ")
          sq = sq[1:20]
          #print sq
          time_asked = time.strptime(sq, "%Y-%m-%d %H:%M:%S")
          weekday_q   = time.strftime("%w", time_asked)
          if weekday_q == '0' or weekday_q == '6':
             weekend_q = 1
          else:
             weekend_q = 0

          sa = row[TIME_ANSWERED_INDEX].replace("T", " ")
          sa = sa[1:20]
          #print sa
          time_answered = time.strptime(sa, "%Y-%m-%d %H:%M:%S")
          weekday_a     = time.strftime("%w", time_answered)
          if weekday_a == '0' or weekday_a == '6':
             weekend_a = 1
          else:
             weekend_a = 0
          #print week_day # sunday - zero
          quest_id = row[QUESTIONID_INDEX].replace('"', '')
          data_w.append([quest_id, weekday_q, weekend_q, weekday_a, weekend_a])
       i = i + 1
   return data_w

def SaveStatToCSV(file_name, data, header):
    with open(file_name, 'wb') as myfile:
        wr = csv.writer(myfile)
        wr.writerow(header)
        wr.writerows(data)
    return

def TimeFeature(filename_input, filename_output):
   #whether a question was asked on weekend
   f       = open(filename_input)
   reader  = csv.reader(f, delimiter=',', quotechar='|')
   workday = DataWeekend(reader)
   SaveStatToCSV(filename_output, workday, header_w)

def parseTime(s):
   print s
   try:
       s = s.replace("T", " ")
       s = s[0:19]
       time_answered = time.strptime(s, "%Y-%m-%d %H:%M:%S")
   except AttributeError:
       print s, 'is not valid time, ignore it'
       return None
   return time_answered

def findTimeSpan(data):
    time_the_oldest = time.strptime('2020-10-10 12:12:12', "%Y-%m-%d %H:%M:%S")
    time_the_newest = time.strptime('1800-02-10 12:12:12', "%Y-%m-%d %H:%M:%S")
    for timestamp in data['TimeAsked']:
        time_answered = parseTime(timestamp)
        if time_answered != None:
            if time_answered > time_the_newest:
                time_the_newest = time_answered
            if time_answered < time_the_oldest:
                time_the_oldest = time_answered
    t_old = datetime.fromtimestamp(mktime(time_the_oldest))
    t_new = datetime.fromtimestamp(mktime(time_the_newest))
    return t_old, t_new
