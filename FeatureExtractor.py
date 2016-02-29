__author__ = 'nb254'

import os
import QueryDB as query
import DecisionTree as tree
import util as util
from Variables import header as header
from Variables import fn as fname
import pandas as pd
import UsersActivity as useractivity
import NLPFeatures as nlp
import TimeFeatures as timefeatures
import TagAnalysis as tags
import UsersStats as users
import UsersLocation as loc
import time
import Stats as stats
from Variables import fn_der as fdname
from collections import Counter
import csv

#DIR = '/mnt/nb254_data/src/data_SO/derived_data/'
DIR = '/mnt/nb254_data/exp/'
header1 = ['Tags', 'SecondsToFirstAnswer']
#db_name = 'stackoverflow'
db_name = 'beer'

def extractUserFeatures(c):
   quest_per_user = pd.DataFrame(query.questPerUser(c), columns=header['quest_per_user'])
   quest_per_user.to_csv(DIR + 'quest_per_user.csv', index=False)

   answer_per_user = pd.DataFrame(query.ansPerUser(c), columns=header['answer_per_user'])
   answer_per_user.to_csv(DIR + 'answer_per_user.csv', index=False)

   posts_per_user = pd.DataFrame(query.postsPerUser(c), columns=header['posts_per_user'])
   posts_per_user.to_csv(DIR + 'posts_per_user.csv', index=False)

   users_stats = pd.DataFrame(query.usersStats(c), columns=header['users_stats'])
   users_stats.to_csv(DIR + 'users_stats.csv', encoding='utf-8', index=False)

   users_av_ans_time = pd.DataFrame(query.usersAvAnsTime(c), columns=header['users_av_ans_time'])
   users_av_ans_time.to_csv(DIR + 'users_av_ans_time.csv', index=False)

def extractQuestFeatures(c):
   accepted_question_title_length = pd.DataFrame(query.questWithAcceptedAnswers(c), columns=header['accepted_question_title_length'])
   accepted_question_title_length.to_csv(DIR + 'accepted_question_title_length.csv', encoding='utf-8', index=False)

   accepted_answers = pd.DataFrame(query.acceptedAnswers(c), columns=header['accepted_answers'])
   accepted_answers.to_csv(DIR + 'accepted_answers.csv', index=False)

   posts_stats = pd.DataFrame(query.postsStats(c), columns=header['posts_stats'])
   posts_stats.to_csv(DIR + 'posts_stats.csv', index=False)

   post_text_data = pd.DataFrame(query.postsText_Data(c), columns=header['post_text_data'])
   post_text_data.to_csv(DIR + 'post_text_data.csv', encoding='utf-8', index=False)

   quest_stats = pd.DataFrame(query.questStats(c), columns=header['quest_stats'])
   quest_stats.to_csv(DIR + 'quest_stats.csv', index=False)

def extractAnsTime(c, MODE, VERSION):
   if MODE == 'FIRST':
      ans_time_first = query.firstAnsTime(c)
      util.save_to_csv(ans_time_first, header['ans_time_first'], 'ans_time_first.csv')
   elif MODE == 'ACCEPTED':
       ans_time_accepted = pd.DataFrame(query.acceptAnsTime(c), columns=header['ans_time_accepted'])
       ans_time_accepted.to_csv(DIR + 'ans_time_accepted.csv', index=False)
   elif MODE == 'UPVOTED':
     ans_time_upvoted = query.upvotedAnsTime(c)
     util.save_to_csv(ans_time_upvoted, header['ans_time_upvoted'], 'ans_time_upvoted.csv')
   if VERSION == 'EXTENDED':
    ans_time_upvoted_ex = query.upvotedAnsTime1(c)
    util.save_to_csv(ans_time_upvoted_ex, header['ans_time_upvoted_ex'], 'ans_time_upvoted_ex.csv')

def userAccAns(data):
    header = ['UserId', 'NUM_OF_A_ACCEPTED_BY_OTHERS']
    #print data
    acc_answers = pd.DataFrame(stats.CountAccAnswers(data), columns=header)
    return acc_answers

def extractNumTags(df_tags):
    num_of_tags = []
    for index in xrange(0, len(df_tags)):
        num_of_tags.append([df_tags['QuestionId'][index], df_tags['Tags'][index].count('>') ])
    df = pd.DataFrame(num_of_tags, columns=['QuestionId', 'NUM_TAGS'])
    return df
'''
def extractNumTags(df_tags):
    num_of_tags = []
    for index in xrange(0, len(df_tags)):
        num_of_tags.append([df_tags['QuestionId'][index], df_tags['Tags'][index].count(',') + 1])
    df = pd.DataFrame(num_of_tags, columns=['QuestionId', 'NUM_TAGS'])
    return df

def extractTagStats(c):
    tags_stats = query.tagStats(c)
    util.save_to_csv(tags_stats, header['tags_stats'], 'tags_stats.csv')
'''

def extractUserActivityFeatures(c):

   users_activity = pd.DataFrame(query.usersActivity(c), columns=header['users_activity'])
   users_activity.to_csv(DIR + 'users_activity.csv', index=False)

   posts = useractivity.makePosts(users_activity)
   posts = posts[posts['UserId'] != -1]
   return posts

def titleBodyLength(data):
   df = data[['PostId','TITLE_LENGTH', 'BODY_LENGTH']]
   df.rename(columns={'PostId':'QuestionId'}, inplace=True)
   return df

def extractTagFeatures(df_tags):
    # CAUTION: takes long time for large datasets...
    df = extractNumTags(df_tags)
    print 'extracted the feature: NUM_TAGS'
    if not os.path.exists(DIR + 'tags'):
        os.makedirs(DIR + 'tags')
    df.to_csv(DIR + 'tags/num_tags.csv', index=False)
    df = pd.read_csv(DIR + 'quest_stats.csv')
    df_unique = tags.uniqueTags(df)
    df_unique.to_csv(DIR + 'tags/1Tags_occurancy.csv', index=False)
    #print 'df unique', len(df_unique)
    tag_features = tags.tagFeatures(df_tags, df_unique)
    tag_features.to_csv(DIR + 'tags/tag_features.csv', index=False)
    print 'extracted the features: TAG_POPULARITY_AV, NUM_POPTAGS'
    df2, df2_occ = tags.tags(df)
    #print 'df2 occ', len(df2_occ)
    df2.to_csv(DIR + 'tags/two_tags.csv', index=False)
    df2_occ.to_csv(DIR + 'tags/2Tags_occurancy1.csv',index=False)
    #optimization step - to create a table with only unique tags
    df2_unique = tags.uniqueTagsFromTwoDf(df_unique, df2_occ)
    #print 'df2 unique', len(df2_unique)
    df2_unique.to_csv(DIR + '/tags/1Tags_unique_occ.csv', index=False)
    #df_unique = pd.read_csv('/mnt/nb254_data/src/data_SO/tags/1Tags_unique_occ.csv')
    df_occ = tags.specificityCalc(df2_occ, df2_unique)
    df_occ.to_csv(DIR + 'tags/Tags_occurancy.csv', index=False)
    df_occ = pd.read_csv(DIR + 'tags/Tags_occurancy.csv')
    df1 = pd.read_csv(DIR + '/tags/two_tags.csv')
    df_m = tags.matchAtoB(df_occ, df1)
    print 'extracted the feature: TAG_SPECIFICITY'
    df_m.to_csv(DIR + 'tags/tag_specificity.csv',index=False)

def extractLocations(user_name, data):
   df_locs = data['LOCATION']

   # create a file with unique locations
   uniq_locs = loc.UniqueLocations(df_locs)
   uniq_locs.to_csv(DIR + 'unique_loc.csv', index=False)
   # find latitude and longitude of these unique locations
   uniq_locs = pd.read_csv(DIR + 'unique_loc.csv')
   print uniq_locs

   locs = list(uniq_locs['LOCATION'])
   file_name_s = DIR + 'unique_loc_latlon.csv'
   loc.findLocations(user_name, locs, file_name_s)
   print 'extracted LAT and LON'
   loc.findTimezones(user_name, DIR + 'unique_loc_latlon.csv', DIR + 'locations_done.csv')

   locations = pd.read_csv(DIR + 'locations_done.csv')
   locations.rename(columns={'Location':'LOCATION'}, inplace=True)
   locations = locations.sort(['LOCATION'], ascending=False)
   locations = locations.reset_index()
   #locations = locations.drop(['index'], axis=1, inplace=True)
   print locations.head()
   #data = pd.read_csv(DIR + 'users_stats.csv')
   data = data.sort(['LOCATION'], ascending=False)
   data = data.reset_index()
   print data.head()
   df = pd.merge(data, locations, how='left', on='LOCATION')
   return df

def extractEasyFeatures(c):
   extractUserFeatures(c)
   extractQuestFeatures(c)
   extractAnsTime(c, 'ACCEPTED', '')

   data = pd.read_csv(DIR + 'accepted_answers.csv')
   acc_answers = userAccAns(data)
   acc_answers.to_csv(DIR + 'accepted_answers_per_user.csv', index=False)

   posts = extractUserActivityFeatures(c)
   #if you saved the posts then you can simply open them
   posts.to_csv(DIR + 'users_posts_times.csv', index=False)

   post_text_data = query.postsText_Data(c)
   util.save_to_csv(post_text_data, header['post_text_data'], 'post_text_data.csv')
   post_text_data = pd.read_csv(DIR + 'post_text_data.csv')
   # extract NLP features: WARNING: very slow
   nlp.NLPExtract(post_text_data, DIR + 'nlp_features.csv')

def extractHardFeatures():
   posts = pd.read_csv(DIR + 'users_posts_times.csv')
   #activities = useractivity.usersActivityFast(posts)
   year, month, day = useractivity.theLatestPostTime(posts)
   #extract last week and last day posts
   posts_week, posts_day = useractivity.extractDayWeekActivity(posts, year, month, day)
   #print posts_week
   df_result = useractivity.extractTimeIntervalFeatures(posts_week, posts_day)
   print 'extracted Q_LAST_WEEK, A_LAST_WEEK, P_NUM_LAST_WEEK'
   df_result.to_csv(DIR + 'temp_features.csv', index=False)

   df = pd.read_csv(DIR + 'quest_stats.csv')
   # extract features when a question was asked
   q_wknd = timefeatures.dateWeekend(df)
   q_wknd.to_csv(DIR + 'quest_weekend.csv', index=False)

   extractLocs()

   df_tags = pd.read_csv(DIR + 'quest_stats.csv')
   extractTagFeatures(df_tags)

def extractLocs():
   data = pd.read_csv(DIR + 'users_stats.csv')
   #TODO write your user's name
   user_name  = ''
   df = extractLocations(user_name, data)
   df.to_csv(DIR + 'data_loc.csv')

c = query.DBConnect(db_name)
#users_behaviour = query.UsersBehaviour(c)
#util.save_to_csv([users_behaviour.values()], header['users_behaviour'], DIR + 'users_behaviour.csv')
#ExtractTagStats()
#data = query.TagStats(c)
#tree.TreePredict(data)

extractEasyFeatures(c)
extractHardFeatures()


