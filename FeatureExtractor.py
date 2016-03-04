__author__ = 'nb254'

import os
import QueryDB as query
import DecisionTree as tree
import util as util
import numpy as np
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

#header1 = ['Tags', 'SecondsToFirstAnswer']
#db_name = 'stackoverflow'
time_stats = {'n_dimension': 0,
              'n_samples': 0,
              't0': time.time(),
              'time_taken': 0.0,
              }

features = {'raw_light': time_stats,
            'raw_heavy': time_stats,
            'easy': time_stats,
            'hard_st': time_stats,
            'hard_tags': time_stats,
            'all': time_stats}

def extractUserFeatures(c, DIR):
    if not os.path.exists(DIR + 'users'):
        os.makedirs(DIR + 'users')
    quest_per_user = pd.DataFrame(query.questPerUser(c), columns=header['quest_per_user'])
    quest_per_user.to_csv(DIR + 'users/quest_per_user.csv', index=False)

    answer_per_user = pd.DataFrame(query.ansPerUser(c), columns=header['answer_per_user'])
    answer_per_user.to_csv(DIR + 'users/answer_per_user.csv', index=False)

    posts_per_user = pd.DataFrame(query.postsPerUser(c), columns=header['posts_per_user'])
    posts_per_user.to_csv(DIR + 'users/posts_per_user.csv', index=False)

    users_stats = pd.DataFrame(query.usersStats(c), columns=header['users_stats'])
    users_stats.to_csv(DIR + 'users/users_stats.csv', encoding='utf-8', index=False)

    users_av_ans_time = pd.DataFrame(query.usersAvAnsTime(c), columns=header['users_av_ans_time'])
    users_av_ans_time.to_csv(DIR + 'users/users_av_ans_time.csv', index=False)

def extractQuestFeatures(c, DIR):
    if not os.path.exists(DIR + 'posts'):
        os.makedirs(DIR + 'posts')

    accepted_answers = pd.DataFrame(query.acceptedAnswers(c), columns=header['accepted_answers'])
    accepted_answers.to_csv(DIR + 'posts/accepted_answers.csv', index=False)

    post_text_data = pd.DataFrame(query.postsText_Data(c), columns=header['post_text_data'])
    post_text_data = post_text_data.drop_duplicates(['PostId'])
    post_text_data.to_csv(DIR + 'posts/post_text_data.csv', encoding='utf-8', index=False)

    quest_stats = pd.DataFrame(query.questStats(c), columns=header['quest_stats'])
    quest_stats.to_csv(DIR + 'posts/quest_stats.csv', index=False)

def extractAnsTime(c, DIR, MODE, VERSION):
    if not os.path.exists(DIR + 'posts'):
        os.makedirs(DIR + 'posts')
    if MODE == 'FIRST':
        ans_time_first = query.firstAnsTime(c)
        util.save_to_csv(ans_time_first, header['ans_time_first'], 'posts/ans_time_first.csv')
    elif MODE == 'ACCEPTED':
        ans_time_accepted = pd.DataFrame(query.acceptAnsTime(c), columns=header['ans_time_accepted'])
        ans_time_accepted.to_csv(DIR + 'posts/ans_time_accepted.csv', index=False)
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
        num_of_tags.append([df_tags['PostId'][index], df_tags['Tags'][index].count('>') ])
    df = pd.DataFrame(num_of_tags, columns=['PostId', 'NUM_TAGS'])
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

def extractUserActivityFeatures(c, DIR):
   if not os.path.exists(DIR + 'users'):
        os.makedirs(DIR + 'users')
   users_activity = pd.DataFrame(query.usersActivity(c), columns=header['users_activity'])
   users_activity.to_csv(DIR + 'posts/users_activity.csv', index=False)

   posts = useractivity.makePosts(users_activity)
   posts = posts[posts['UserId'] != -1]
   return posts

def titleBodyLength(data):
   df = data[['PostId','TITLE_LENGTH', 'BODY_LENGTH']]
   df.rename(columns={'PostId':'QuestionId'}, inplace=True)
   return df

def extractTagFeatures(DIR, df_tags):
    # CAUTION: takes long time for large datasets...
    df = extractNumTags(df_tags)
    print 'extracted the feature: NUM_TAGS'
    if not os.path.exists(DIR + 'posts/tags'):
        os.makedirs(DIR + 'posts/tags')
    df.to_csv(DIR + 'posts/tags/num_tags.csv', index=False)
    df = pd.read_csv(DIR + 'posts/quest_stats.csv')
    df_unique = tags.uniqueTags(df)
    df_unique.to_csv(DIR + 'posts/tags/1Tags_occurancy.csv', index=False)
    #print 'df unique', len(df_unique)
    tag_features = tags.tagFeatures(df_tags, df_unique)
    tag_features.to_csv(DIR + 'posts/tags/tag_features.csv', index=False)
    print 'extracted the features: TAG_POPULARITY_AV, NUM_POPTAGS'
    df2, df2_occ = tags.tags(df)
    #print 'df2 occ', len(df2_occ)
    df2.to_csv(DIR + 'posts/tags/two_tags.csv', index=False)
    df2_occ.to_csv(DIR + 'posts/tags/2Tags_occurancy1.csv',index=False)
    #optimization step - to create a table with only unique tags
    df2_unique = tags.uniqueTagsFromTwoDf(df_unique, df2_occ)
    #print 'df2 unique', len(df2_unique)
    df2_unique.to_csv(DIR + 'posts/tags/1Tags_unique_occ.csv', index=False)
    #df_unique = pd.read_csv('/mnt/nb254_data/src/data_SO/tags/1Tags_unique_occ.csv')
    df_occ = tags.specificityCalc(df2_occ, df2_unique)
    df_occ.to_csv(DIR + 'posts/tags/Tags_occurancy.csv', index=False)
    df_occ = pd.read_csv(DIR + 'posts/tags/Tags_occurancy.csv')
    df1 = pd.read_csv(DIR + 'posts/tags/two_tags.csv')
    df_m = tags.matchAtoB(df_occ, df1)
    print 'extracted the feature: TAG_SPECIFICITY'
    df_m.to_csv(DIR + 'posts/tags/tag_specificity.csv',index=False)

def extractLocs(DIR):
   data = pd.read_csv(DIR + 'users/users_stats.csv')
   #TODO write your user's name
   user_name  = 'NikolayBurlutskiy'
   #user_name=None
   df = extractLocations(DIR, user_name, data)
   df.to_csv(DIR + 'users/data_loc.csv')

def extractLocations(DIR, user_name, data):

   df_locs = data['LOCATION']
   # create a file with unique locations
   uniq_locs = loc.UniqueLocations(df_locs)
   uniq_locs = uniq_locs.dropna()
   if not os.path.exists(DIR + 'location'):
        os.makedirs(DIR + 'location')
   uniq_locs.to_csv(DIR + 'location/unique_loc.csv', index=False)
   # find latitude and longitude of these unique locations

   uniq_locs = pd.read_csv(DIR + 'location/unique_loc.csv')
   print uniq_locs

   locs = list(uniq_locs['LOCATION'])
   print locs
   file_name_s = DIR + '/location/unique_loc_latlon.csv'
   loc.findLocations(user_name, locs, file_name_s)
   print 'extracted LAT and LON'

   loc.findTimezones(user_name, DIR + 'location/unique_loc_latlon.csv', DIR + 'location/locations_done.csv')

   locations = pd.read_csv(DIR + 'location/locations_done.csv')
   locations.rename(columns={'Location':'LOCATION'}, inplace=True)
   locations = locations.sort(['LOCATION'], ascending=False)
   locations = locations.reset_index()
   #locations = locations.drop(['index'], axis=1, inplace=True)
   print locations.head()
   #data = pd.read_csv(DIR + 'users_stats.csv')
   data = data.sort(['LOCATION'], ascending=False)
   data = data.reset_index()
   print data.head()
   #transform location to a unique number
   df2 = intFromLoc(DIR, data)
   print 'extracted the feature LOCATION_NUM'
   data = pd.concat([data, df2], axis=1)
   df = pd.merge(data, locations, how='left', on='LOCATION')
   return df

def intFromLoc(DIR, df):
    dloc = df['LOCATION']
    dloc_unique = list(set(dloc))
    df1 = pd.DataFrame(dloc_unique, columns=['LOCATION'])
    df1.to_csv(DIR + 'location/unique_locations.csv')
    dfloc = pd.read_csv(DIR + 'location/unique_locations.csv')
    dfloc.columns = ['index', 'LOCATION']
    unique_num = []
    for index in xrange(0, len(df)):
        if df['LOCATION'][index] in dloc_unique:
           ind = dfloc[dfloc['LOCATION']== df['LOCATION'][index]].index.tolist()
           if ind != []:
              unique_num.append(dfloc['index'][ind[0]])
              if (index % 1000) == 0:
                  print index
        else:
           print "doesn't work"
           print index
    df2 = pd.DataFrame(unique_num, columns=['LOCATION_NUM'])
    return df2


def extractEasyFeatures(c, DIR):
   extractUserFeatures(c, DIR)
   extractQuestFeatures(c, DIR)
   extractAnsTime(c, DIR, 'ACCEPTED', '')

   data = pd.read_csv(DIR + 'posts/accepted_answers.csv')
   acc_answers = userAccAns(data)
   acc_answers.to_csv(DIR + 'users/accepted_answers_per_user.csv', index=False)

   posts = extractUserActivityFeatures(c, DIR)
   #if you saved the posts then you can simply open them
   posts.to_csv(DIR + 'posts/users_posts_times.csv', index=False)

   post_text_data = pd.read_csv(DIR + 'posts/post_text_data.csv')
   # extract NLP features: WARNING: very slow
   nlp.NLPExtract(post_text_data, DIR + 'posts/nlp_features.csv')

   post_lengths = post_text_data[['PostId', 'TITLE_LENGTH', 'BODY_LENGTH']]
   post_lengths.to_csv(DIR + 'posts/post_text_lengths.csv', index=False)


def extractHardFeatures(DIR):
    #TODO uncomment

   posts = pd.read_csv(DIR + 'posts/users_posts_times.csv')
   #activities = useractivity.usersActivityFast(posts)
   year, month, day = useractivity.theLatestPostTime(posts)
   #extract last week and last day posts
   posts_week, posts_day = useractivity.extractDayWeekActivity(posts, year, month, day)
   #print posts_week
   df_result = useractivity.extractTimeIntervalFeatures(posts_week, posts_day)
   print 'extracted Q_LAST_WEEK, A_LAST_WEEK, P_NUM_LAST_WEEK'
   df_result.to_csv(DIR + 'users/temp_features.csv', index=False)

   activities = useractivity.usersActivityFast(posts)
   df_tr = useractivity.userActivityTransform(activities)
   df_tr.to_csv(DIR + 'users/temporal_user_activities.csv', index=False)

   df = pd.read_csv(DIR + 'posts/quest_stats.csv')
   # extract features when a question was asked
   q_wknd = timefeatures.dateWeekend(df)
   q_wknd.to_csv(DIR + 'posts/quest_weekend.csv', index=False)

   extractLocs(DIR)

   df_tags = pd.read_csv(DIR + 'posts/quest_stats.csv')
   extractTagFeatures(DIR, df_tags)

def createTimeLabel(input, time_stamp, file_name):
    i = 0;
    myfile = open(file_name, 'wb')
    wr = csv.writer(myfile)
    wr.writerow(['PostId', 'TEMP_CL'])
    for elem in input['SecondsToAcceptedAnswer']:
      if elem > time_stamp:
         row = int(1)
      else:
         row = int(0)
      wr.writerow([input['PostId'][i], row])
      i = i + 1

def createTimeLabels(DIR, input):
    #create a label '1' if longer than an hour and '0' otherwise
    HOUR    = 60 * 60 # one hour = 60 seconds by 60 minutes
    #MEDIAN_TIME = 21174 #for fitness
    FIVE_MINUTES = 5 * 60 # 5 minutes
    DAY = HOUR * 24
    MONTH = DAY * 30
    MEDIAN_TIME = 491
    TEST_TIME = 82000 #for fitness
    MED_REAL = 60 * 30
    times = [FIVE_MINUTES, MEDIAN_TIME, HOUR, DAY, MONTH]
    #createTimeLabel(input, FIVE_MINUTES, DIR + 'data_for_ML/TEMP_CL1.csv')
    createTimeLabel(input, MEDIAN_TIME, DIR + 'posts/TEMP_CL.csv')
    #createTimeLabel(input, HOUR, DIR + 'data_for_ML/TEMP_CL3.csv')
    #createTimeLabel(input, DAY, DIR + 'data_for_ML/TEMP_CL4.csv')
    #createTimeLabel(input, MONTH, DIR + 'data_for_ML/TEMP_CL5.csv')

#def somethingold():
    #users_behaviour = query.UsersBehaviour(c)
    #util.save_to_csv([users_behaviour.values()], header['users_behaviour'], DIR + 'users_behaviour.csv')
    #ExtractTagStats()
    #data = query.TagStats(c)
    #tree.TreePredict(data)
    #posts_stats = pd.DataFrame(query.postsStats(c), columns=header['posts_stats'])
    #posts_stats.to_csv(DIR + 'posts/posts_stats.csv', index=False)
    #accepted_question_title_length = pd.DataFrame(query.questWithAcceptedAnswers(c), columns=header['accepted_question_title_length'])
    #accepted_question_title_length.to_csv(DIR + 'posts/accepted_question_title_length.csv', encoding='utf-8', index=False)

def extractForML(db_name, DIR):
    c = query.DBConnect(db_name)
    #extractEasyFeatures(c, DIR)
    extractHardFeatures(DIR)
    input = pd.read_csv(DIR + 'posts/quest_stats.csv', error_bad_lines=False)
    t_median = input['SecondsToAcceptedAnswer'].median()
    print t_median
    createTimeLabel(input, t_median, DIR + 'posts/TEMP_CL.csv')
