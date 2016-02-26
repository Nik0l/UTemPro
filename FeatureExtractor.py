__author__ = 'nb254'


import QueryDB as query
import DecisionTree as tree
import util as util
from Variables import header as header
from Variables import fn as fname
import pandas as pd
import UsersActivity as useractivity
import NLPFeatures as nlp
import TimeFeatures as timefeature
import TagAnalysis as tags
import UsersStats as users
import UsersLocation as loc
import time
import Stats as stats
from Variables import fn_der as fdname

DIR = '/mnt/nb254_data/src/data_SO/derived_data/'
header1 = ['Tags', 'SecondsToFirstAnswer']
db_name = 'stackoverflow'
#db_name = 'beer'

def ExtractUserFeatures(c):
   quest_per_user = query.QuestPerUser(c)
   util.save_to_csv(quest_per_user, header['quest_per_user'], 'quest_per_user.csv')

   answer_per_user = query.AnsPerUser(c)
   util.save_to_csv(answer_per_user, header['answer_per_user'], 'answer_per_user.csv')

   posts_per_user = query.PostsPerUser(c)
   util.save_to_csv(posts_per_user, header['posts_per_user'], 'posts_per_user.csv')

   users_stats = query.UsersStats(c)
   util.save_to_csv(users_stats, header['users_stats'], 'users_stats.csv')

   users_av_ans_time = query.UsersAvAnsTime(c)
   util.save_to_csv(users_av_ans_time, header['users_av_ans_time'], 'users_av_ans_time.csv')

def ExtractQuestFeatures(c):

   accepted_question_title_length = query.QuestWithAcceptedAnswers(c)
   util.save_to_csv(accepted_question_title_length, header['accepted_question_title_length'], 'accepted_question_title_length.csv')

   accepted_answers = query.AcceptedAnswers(c)
   util.save_to_csv(accepted_answers, header['accepted_answers'], 'accepted_answers.csv')

   posts_stats = query.PostsStats(c)
   util.save_to_csv(posts_stats, header['posts_stats'], 'posts_stats.csv')

   #post_title_length_OLD = query.PostsTitleLength_OLD(c)
   #query.SaveQuery(post_title_length_OLD, header['post_title_length_OLD'], 'post_title_length_OLD.csv')

   post_text_data = query.PostsText_Data(c)
   util.save_to_csv(post_text_data, header['post_text_data'], 'post_text_data.csv')

   quest_stats = query.QuestStats(c)
   util.save_to_csv(quest_stats, header['quest_stats'], 'quest_stats.csv')

def ExtractAnsTime(c, MODE, VERSION):
   if MODE == 'FIRST':
      ans_time_first = query.FirstAnsTime(c)
      util.save_to_csv(ans_time_first, header['ans_time_first'], 'ans_time_first.csv')
   elif MODE == 'ACCEPTED':
      ans_time_accept = query.AcceptAnsTime(c)
      util.save_to_csv(ans_time_accept, header['ans_time_accepted'], 'ans_time_accepted.csv')
   elif MODE == 'UPVOTED':
     ans_time_upvoted = query.UpvotedAnsTime(c)
     util.save_to_csv(ans_time_upvoted, header['ans_time_upvoted'], 'ans_time_upvoted.csv')
   if VERSION == 'EXTENDED':
    ans_time_upvoted_ex = query.UpvotedAnsTime1(c)
    util.save_to_csv(ans_time_upvoted_ex, header['ans_time_upvoted_ex'], 'ans_time_upvoted_ex.csv')

def ExtractTagStats(c):
    tags_stats = query.TagStats(c)
    util.save_to_csv(tags_stats, header['tags_stats'], 'tags_stats.csv')

def extractNumTags(filename):
    df_tags = pd.read_csv(filename)
    #print df_tags.shape[0]
    num_of_tags = []
    for index in xrange(0, len(df_tags)):
            num_of_tags.append([df_tags['QuestionId'][index], df_tags['Tags'][index].count(',') + 1])
    df = pd.DataFrame(num_of_tags, columns=['QuestionId', 'NUM_TAGS'])
    df.to_csv('/mnt/nb254_data/src/data_SO/tags/num_tags.csv', index=False)

def ExtractUserActivityFeatures():
   #users_activity = query.UsersActivity(c)
   #util.save_to_csv(users_activity, header['users_activity'], 'users_activity.csv')
   #fname['usr_act'] is 'users_activity.csv'
   #users_activity = useractivity.GetUserActivity(fname['usr_act'])
   filename = '/mnt/nb254_data/src/data_SO/' + 'users_activity.csv'
   users_activity = pd.read_csv(filename)
   posts = useractivity.MakePosts(users_activity)
   #if you saved the posts then you can simply open them
   #posts = pd.read_csv('users_posts_times3.csv')
   activities = useractivity.usersActivityFast(posts)
   #print activities
   util.save_to_csv(activities, header['users_activity_features'], 'users_activity_features.csv')

def ExtractUserTimeIntervalFeatures(year, month, day):
    #posts = pd.read_csv('users_posts_times3.csv')
    # = posts[posts['year'] == year]
    #posts = posts[posts['month'] == month]
    #posts = posts[posts['day'] > day]
    #posts = posts.sort(['day'], ascending=False)
    #posts = posts.sort(['UserId'], ascending=True)
    #posts.to_csv('posts_2014_09_07A.csv')
    #TODO if not saved, then indices must be put in order
    posts = pd.read_csv('posts_2014_09_07A.csv')
    posts_day = posts[posts['day'] > 12]
    posts_day = posts_day[['UserId','PostType', 'year', 'month', 'day', 'hour', 'min']]
    posts_day = posts_day.sort(['hour'], ascending=False)
    posts_day.to_csv('posts_2014_09_07A12.csv')
    posts_day = pd.read_csv('posts_2014_09_07A12.csv')
    num = 1

    activities_day = activityDay(posts_day)
    df_day = pd.DataFrame(activities_day, columns=['UserId', 'P_NUM_LAST_DAY'])
    print df_day
    #activities last week
    activities = activityWeek(posts)
    df_week = pd.DataFrame(activities, columns=['UserId', 'Q_LAST_WEEK', 'A_LAST_WEEK'])
    print df_week
    df_result = pd.merge(df_week, df_day, how='left', on='UserId')
    print df_result
    df_result = df_result.fillna(0)
    # columns=['UserId', 'Q_LAST_WEEK', 'A_LAST_WEEK', 'P_NUM_LAST_DAY']
    df_result.to_csv('temp_features.csv')

def activityDay(posts):
    activities_day = []
    comments = 0
    #activities last day
    for index in xrange(0, len(posts)-1):
        comments = comments + 1
        if posts['UserId'][index] != posts['UserId'][index+1]:
            activities_day.append([posts['UserId'][index], comments])
            comments = 0
    return activities_day

def activityWeek(posts):
    activities = []
    act = dict(
        questions = 0,
        answers = 0,
    )
    for index in xrange(0, len(posts)-1):
        updateActivities(posts, act, index)
        if posts['UserId'][index] != posts['UserId'][index+1]:
            activities.append([posts['UserId'][index], act['questions'], act['answers']])
            act['questions'] = 0
            act['answers']= 0
    return activities

def updateActivities(posts, act, index):
    if posts['PostType'][index] == 1: # question
        act['questions'] = act['questions'] + 1
    elif posts['PostType'][index] == 2: # answer
        act['answers'] = act['answers'] + 1

def UserAccAns():
    header = ['UserId', 'NUM_OF_A_ACCEPTED_BY_OTHERS']
    data = pd.read_csv(fname['acc_ans'])
    print data
    acc_answers = stats.CountAccAnswers(data)
    #print acc_answers
    util.save_to_csv(acc_answers, header, fdname['uac_ans'])

def TitleBodyLength():
   data = pd.read_csv(fname['txt_dat'])
   df1 = data[['PostId','TITLE_LENGTH', 'BODY_LENGTH']]
   df1.rename(columns={'PostId':'QuestionId'}, inplace=True)
   df1.to_csv(fname['pst_ttb'], index=False)

def ExtractComplexFeatures():
    # extract NLP features: WARNING: very slow
    nlp.NLPExtract(fname['txt_dat'], fdname['pst_nlp'])
    # extract features when a question was asked
    timefeature.TimeFeature(fname['qst_sta'], fdname['qst_tmp'])

def ExtractTagFeatures():
    # CAUTION: takes long time for large datasets...
    data = tags.Stats(fname['qst_sta'])
    tags.TagCoOcStats(data['pairs'], fdname['unq_tgs'])
    tags.TagPairsCoocurance(data['tags'], fdname['unq_tgs'], fdname['tg_cooc'])
    tags.TagFeatures(fname['qst_sta'], data['unique_tags'], data['tags'], fdname['tg_stat'])
'''
def ExtractUserActivityFeatures():
    time_cut_off = time.strptime('2013-10-26 17:44:02', "%Y-%m-%d %H:%M:%S")
    users_activity = users.NumSubsAns(fname['qst_sta'], time_cut_off)  #calculate the feature
    users.SaveStatToCSV(fdname['ans_sta'], users_activity)
'''
def ExtractLocations():
   # create a file with unique locations
   uniq_locs = loc.UniqueLocations(fname['usr_sta'])
   print uniq_locs
   loc.SavetoCSV(uniq_locs, ['Unique_Locations'], fname['usr_loc'])
   # find latitude and longitude of these unique locations
   #uniq_locs = loc.OpenCSV(fname['usr_loc'])
   #print uniq_locs
   #loc.WriteLocTZ(uniq_locs, fname['usr_lc1'])

   # create the file with the unique locations
   #loc.SpellChecker(fname['usr_lcn'], 'corrected_loc.csv')
   #locs = loc.OpenCSV('corrected_loc.csv')
   #loc.FindLocations(locs, 'LOCS.csv')
   #loc.FindTimezones(fname['usr_lc1'], fname['usr_ltz'])
   #data = csv.reader(open(fname['usr_sta']))
   #data_unique = csv.reader(open(fname['usr_lc1'])) # file with all location information
   #HEADER  = ['UserId'] + features.KEY_LOC + features.USER_LOC + ['USERS_SAME_LOC']
   # match the information from the unique locations file to the users' IDs
   #loc.MatchLocations(data, data_unique, HEADER, fname['usr_evr'])
def userActivityTransform():
    df = pd.read_csv('users_activity_features.csv')

    act = dict(
        q_hour = [],
        a_hour = [],
        q_month = [],
        a_month = [],
    )
    for index in xrange(0, len(df)):
        items_qh = transformString(df['Q_U_HOUR'][index])
        act['q_hour'].append([df['UserId'][index]] + items_qh)

        items_ah = transformString(df['Q_U_MONTH'][index])
        act['a_hour'].append(items_ah)

        items_qm = transformString(df['A_U_HOUR'][index])
        act['q_month'].append(items_qm)

        items_am = transformString(df['A_U_MONTH'][index])
        act['a_month'].append(items_am)


    dfq_hour = pd.DataFrame(act['q_hour'], columns=['UserId', 'qh1','qh2','qh3','qh4','qh5','qh6','qh7','qh8','qh9','qh10','qh11','qh12',
                                               'qh13','qh14','qh15','qh16','qh17','qh18','qh19','qh20','qh21','qh22','qh23','qh24'])
    dfa_hour = pd.DataFrame(act['a_hour'], columns=['ah1','ah2','ah3','ah4','ah5','ah6','ah7','ah8','ah9','ah10','ah11','ah12',
                                               'ah13','ah14','ah15','ah16','ah17','ah18','ah19','ah20','ah21','ah22','ah23','ah24'])

    dfq_month = pd.DataFrame(act['q_month'], columns=['qm1', 'qm2', 'qm3', 'qm4', 'qm5', 'qm6',
                                                      'qm7', 'qm8', 'qm9', 'qm10', 'qm11', 'qm12'])
    dfa_month = pd.DataFrame(act['a_month'], columns=['am1', 'am2', 'am3', 'am4', 'am5', 'am6',
                                                      'am7', 'am8', 'am9', 'am10', 'am11', 'am12'])
    result = pd.concat([dfq_hour, dfa_hour, dfq_month, dfa_month], axis=1)
    result.to_csv('/mnt/nb254_data/src/data_SO/temporal/temp_features1.csv', index=False)

def transformString(items):
    items = items.replace(",", "")
    items = items.replace("[", "")
    items = items.replace("]", "")
    items = items.split()
    return items

def MachineLearning(c):
   FILES_U = ["users_stats", "accepted_answers_per_user", "answer_per_user", "quest_per_user", "user_av_ans_time", "posts_per_user", "users_locations1"]
   FILES_Q = ["NLP_features", "tags_stats", "quest_stats1", "quest_weekend"]
   ExtractUserFeatures()
   #accepted answers
   accepted_answers = query.AcceptedAnswers(c)
   util.save_to_csv(accepted_answers, header['accepted_answers'], 'accepted_answers.csv')
   #TODO: calculate accepted answers per user:
   #accepted_answers_per_user = stats.CountAccAnswers(data)
   #accepted_answers_per_user = util.save_to_csv(accepted_answers_per_user, header['accepted_answers_per_user'], 'accepted_answers_per_user.csv')

   # users' locations
   #users_locations = query.UsersLocations()
   #util.save_to_csv(users_locations, header['users_locations'], 'users_locations.csv')
   # question features
   quest_stats = query.QuestStats(c)
   util.save_to_csv(quest_stats, header['quest_stats'], 'quest_stats.csv')
   #TODO: NLP features, tags stats, and quest on weekend
c = 0
#c = query.DBConnect(db_name)
#users_behaviour = query.UsersBehaviour(c)
#util.save_to_csv([users_behaviour.values()], header['users_behaviour'], DIR + 'users_behaviour.csv')
#ExtractTagStats()
#data = query.TagStats(c)
#tree.TreePredict(data)
#ExtractAnsTime('ACCEPTED', '')
#data = query.PostsText_Data1(c)
#data.to_csv("posts_texts_data.csv")
#ExtractUserFeatures()
#ExtractQuestFeatures()
#UserAccAns()
#TitleBodyLength()
#ExtractLocations()
#ExtractUserActivityFeatures()
#extract last week and last day posts
#ExtractUserTimeIntervalFeatures(2014, 9, 7)
#extractNumTags('/mnt/nb254_data/src/data_SO/tags/tags_stats.csv')
#userActivityTransform()
#ExtractTagStats()
#MachineLearning()
#post_text_data = query.PostsText_Data(c)
#util.save_to_csv(post_text_data, header['post_text_data'], 'post_text_data.csv')
#filename = 'users_activity.csv'
#data = pd.read_csv(filename)
#result = useractivity.MakePosts(data)
#result.to_csv("users_activity_posts.csv")

#ExtractComplexFeatures()
#ExtractTagFeatures()
#ExtractUserActivityFeatures()


