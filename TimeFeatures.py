__author__ = 'nb254'
import time
import csv
from datetime import date
import Features as feature
from time import mktime
from datetime import datetime
import pandas as pd

def dateWeekend(data):
   data_w = []
   for index in xrange(0, len(data)):
          #print data['TimeAsked'][index]
          sq = str(data['TimeAsked'][index]).replace("T", " ")
          sq = sq[0:19]
          #print sq
          time_asked = time.strptime(sq, "%Y-%m-%d %H:%M:%S")
          weekday_q   = time.strftime("%w", time_asked)
          if weekday_q == '0' or weekday_q == '6':
             weekend_q = 1
          else:
             weekend_q = 0

          sa = data['TimeAnswered'][index].replace("T", " ")
          sa = sa[0:19]
          #print sa
          time_answered = time.strptime(sa, "%Y-%m-%d %H:%M:%S")
          weekday_a     = time.strftime("%w", time_answered)
          if weekday_a == '0' or weekday_a == '6':
             weekend_a = 1
          else:
             weekend_a = 0
          #print week_day # sunday - zero
          quest_id = data['QuestionId'][index]
          data_w.append([quest_id, weekday_q, weekend_q, weekday_a, weekend_a])
   result = pd.DataFrame(data_w, columns=['QuestionId', 'WEEKDAY_Q', 'WEEKEND_Q', 'WEEKDAY_A', 'WEEKEND_A'])
   return result

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
