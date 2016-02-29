# Statistics on users for high-level analysis.
__author__ = 'nb254'
from collections import Counter
import time

import csv
import pandas as pd
import math
from datetime import date
from dateutil.relativedelta import relativedelta
import Features as features
import TagAnalysis as tga
import util
import TimeFeatures as tmpf

NUM_OF_ANS = 4
HOUR = 60 * 60

def dataCut(data, time_cutoff):
   data_sorted = data.sort(['TimeAsked'], ascending=False)
   data_entries = 0
   for (i, timestamp) in enumerate(data_sorted['TimeAsked']):
       time_answered = tmpf.parseTime(timestamp)
       if time_answered < time_cutoff:
           data_entries = i
           print data_entries, 'questions to cut'
           break
   data_cut = data_sorted[1:data_entries]
   return data_cut

def activeAnswerers(answersUserIds, num_of_answers):
   users_answers = Counter(answersUserIds)
   #find active answerers: the ones who answer more than N answers
   #print users_answers
   answerers = []
   for answerer in users_answers:
      if users_answers[answerer] > num_of_answers:
         #print "answerer: " + str(answerer) + " with number of answers: " + str(users_answers[answerer])
         answerers.append(answerer)
   return answerers

def respAnswerers(data, ANSWER_TIME):
   users_answers = []
   for index, row in data.iterrows():
      resp_time = int(row['SecondsToAcceptedAnswer'])
      if resp_time < ANSWER_TIME:
         if not math.isnan(row['AnswererId']):
            users_answers.append(int(row['AnswererId']))
   #find active answerers: the ones who answer more than N answers
   users_ans = Counter(users_answers)
   return users_ans

def tags(data, answersUserIds, quest_tags):
   i = 0
   tags = [] # tags of active answerers
   for index, row in data.iterrows():
      if not math.isnan(row['AnswererId']):
         if row['AnswererId'] in answersUserIds:
            for tag in quest_tags[i]:
               tag = tag.replace('"', '')
               #print tag
               # nasty cheating
               tags.append(tag + "_" + str(int(row['AnswererId'])))
            i = i + 1
   #print tags
   return tags

def answerersPerTag(active_tags):
   unique = list(Counter(active_tags))
   stat  = Counter(unique)
   temp   = []
   for elem in stat:
      elem = elem.replace("_", " ")
      elem = elem.split()
      temp.append(elem[0])
   answerersPerTag = Counter(temp)
   return answerersPerTag

def avScores(data, ans_per_tag, quest_tags):
   av_scores = []
   i = 0
   act_pas_ratio = 0
   res_pas_ratio = 0
   #count average scores for each question
   tags = list(ans_per_tag)
   for index, row in data.iterrows():
      av_score = [0, 0, 0]
      for tag in quest_tags[i]:
         #tag = tag.replace("'", '')
         #print tag
         for j in range(0, len(av_score)):
            if tag in tags[j]:
               av_score[j] = float(av_score[j] + ans_per_tag[j][tag])
      av_score[:] = [x / len(quest_tags[i]) for x in av_score] # divide each element by the length
      if av_score[1] != 0:
         act_pas_ratio = float(av_score[0] / av_score[1])
         res_pas_ratio = float(av_score[2] / av_score[1])
      av_scores.append([row['QuestionId'],
                        row['UserId'],
                        row['AnswererId'],
                        row['Tags'],
                        row['TimeAsked'],
                        av_score[0], act_pas_ratio,
                        av_score[2], res_pas_ratio])
      i = i + 1
   return av_scores

def prepareData(data, NUM_OF_ANS, TIME, not_saved=True):

   if not_saved:
       answersUserIds = data['AnswererId'].fillna(0.0).astype(int)
       all_answerers = activeAnswerers(answersUserIds, 0)
       util.saveElemsToCSV(DIR + 'temp/all_answerers.csv', all_answerers, header='')
       act_answerers = activeAnswerers(answersUserIds, NUM_OF_ANS)
       util.saveElemsToCSV(DIR + 'temp/act_answerers.csv', act_answerers, header='')
       resp_users_ans = respAnswerers(data, TIME)
       util.writeDict(DIR + 'temp/resp_users_ans.csv', resp_users_ans)
       # the list of tags for all questions
       quest_tags = tga.tagList(data)
       util.saveElemsToCSV(DIR + 'temp/quest_tags.csv', quest_tags, header='')
   else:
       all_answerers = util.openListFromCSV(DIR + 'temp/all_answerers.csv')
       all_answerers = [int(i) for i in all_answerers]
       act_answerers = util.openListFromCSV(DIR + 'temp/act_answerers.csv')
       act_answerers = [int(i) for i in act_answerers]
       resp_users_ans = util.openDictfromCSV(DIR + 'temp/resp_users_ans.csv')
       resp_users_ans = [int(i) for i in resp_users_ans]
       quest_tags = util.openListFromCSV(DIR + 'temp/quest_tags.csv')
   answerers = [act_answerers, all_answerers, resp_users_ans]
   return answerers, quest_tags

def numSubsAns(data, answerers, quest_tags):
   tagsa = [0, 0, 0]
   ans_per_tag = [0, 0, 0]
   #compute the number of active subscribers for each tag
   for i in range (0, len(answerers)):
      tagsa[i] = tags(data, answerers[i], quest_tags)
      ans_per_tag[i] = answerersPerTag(tagsa[i])
   av_scores = avScores(data, ans_per_tag, quest_tags)
   return av_scores
'''
DIR = '/mnt/nb254_data/learning/data/'
filename = 'DATA_MERGED.csv'
#filename = 'DATAtoy1.csv'
filename_res = 'temp/useractivity.csv'
data = pd.read_csv(DIR + filename)
t_old, t_new = tmpf.findTimeSpan(data)
print 'from', t_old, 'to', t_new
#from 2008-07-31 21:42:52 to 2014-09-14 00:13:09
time_cutoff = time.strptime('2014-03-14 00:13:09', "%Y-%m-%d %H:%M:%S")
#datacut = dataCut(data, time_cutoff)
#datacut.to_csv(DIR + 'temp/datacut.csv')
datacut = pd.read_csv(DIR + 'temp/datacut.csv')
answerers, quest_tags = prepareData(datacut, NUM_OF_ANS=NUM_OF_ANS, TIME=HOUR, not_saved=True)
results = numSubsAns(datacut, answerers, quest_tags)

header = features.KEYS_US_ACT + features.USER_ACTIVITY
util.saveStatToCSV(DIR + filename_res, results, header, one_row=False)
'''
