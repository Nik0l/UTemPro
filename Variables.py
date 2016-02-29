# variables, constants.
__author__ = 'nb254'

DIR_DATA = '/mnt/nb254_data/src/data_SO/'
hl_stats = 'high_level_stats/'
derived_data = 'derived_data/'
# the files with all the extracted features
fn = {'hl_stat': DIR_DATA + hl_stats + 'high_level_statistics.csv',
      'num_ans': DIR_DATA + hl_stats + 'numberofanswers.csv',
      'rep_usr': DIR_DATA + hl_stats + 'users_reputation.csv',
      'qst_usr': DIR_DATA + 'quest_per_user.csv',
      'pst_own': DIR_DATA + 'posts_per_user.csv',
      'pst_sts': DIR_DATA + 'posts_stats.csv',
      'ans_tme': DIR_DATA + 'answertime-accepted.csv',
      'acc_ans': DIR_DATA + 'accepted_answers.csv',
      'usr_sta': DIR_DATA + 'users_stats.csv',
      'usr_loc': DIR_DATA + 'unique_locations.csv',
      'usr_ltz': DIR_DATA + 'unique_loc_timezones.csv', # locations and timezones
      'usr_lc1': DIR_DATA + derived_data + 'unique_locations1.csv', #locations with latitudes and longitudes
      'usr_evr': DIR_DATA + 'users_stats_evr.csv', # users stats and location merged together
      'usr_lcn': DIR_DATA + 'loc_not_iden.csv', # not identified locations
      'qst_sta': DIR_DATA + 'quest_stats.csv',
      'txt_dat': DIR_DATA + 'post_text_data.csv',
      'pst_ttb': DIR_DATA + derived_data + 'post_title_length.csv',
      'usr_bhr': DIR_DATA + 'users_behaviour.csv',
      'usr_act': DIR_DATA + 'users_activity.csv'}

# the files with features derived from the features above by some transformation
fn_der = {'uac_ans': DIR_DATA + 'derived_data/accepted_answers_per_user.csv',
          'ttl_sta': DIR_DATA + 'derived_data/title_stats.csv',
          'ans_sta': DIR_DATA + 'derived_data/answerers_stats.csv',#user statistics: activity, tags etc
          'qst_tmp': DIR_DATA + 'derived_data/quest_weekend.csv',
          'pst_nlp': DIR_DATA + 'derived_data/NLP_features.csv',
          'unq_tgs': DIR_DATA + 'tags/unique_tag_pairs.csv',#tags statistics and features
          'tg_cooc': DIR_DATA + 'tags/tags_coocurance.csv',
          'tg_stat': DIR_DATA + 'tags/tags_stats.csv',
          'tgs_sts': DIR_DATA + 'tags_stats.csv',
          'usr_tfc': DIR_DATA + 'users_activity_features.csv'}
# filenames wich must be classified in the first or second group at some point
filenames = {'posts_length': 'derived_data/posts_length_stat.csv',
             'questions_length': 'derived_data/questions_length_stat.csv',
             'questions_t_length': 'derived_data/questions_t_length_stat.csv',
             'answers_length': 'derived_data/answers_length_stat.csv'}

header = {'quest_per_user': ['UserId', 'U_QUESTIONS'],
          'answer_per_user': ['UserId', 'U_ANSWERS'],
          'posts_per_user':  ['UserId', 'posts'],
          'users_stats': ['UserId', 'Name', 'LOCATION', 'DataCreated', 'DAYS_ON_SITE', 'U_REPUTATION', 'U_UPVOTES', 'U_DOWNVOTES', 'U_VIEWS'],
          'users_av_ans_time': ['UserId', 'U_AV_ANS_TIME'],
          'accepted_question_title_length': ['PostId', 'UserId', 'TitleQ', 'BodyQ'],
          'quest_stats': ['QuestionId', 'UserId', 'AnswererId', 'Q_VIEWS',  'Tags', 'TimeAsked', 'TimeAnswered', 'SecondsToAcceptedAnswer', 'AnswerId'],
          'ans_time_first': ['QuestionId', 'Q_ASKED', 'SecondsToFirstAnswer'],
          'ans_time_accepted': ['QuestionId', 'Q_ASKED', 'SecondsToFirstAnswer'],
          'ans_time_upvoted': ['QuestionId', 'Q_ASKED', 'SecondsToFirstAnswer'],
          'ans_time_upvoted_ex': ['QuestionId', 'Q_ASKED', 'SecondsToFirstAnswer', 'AnswerId', 'AskerId', 'AnswererId'],
          'post_title_length_OLD': ['PostId', 'UserId', 'PostTypeId', 'TITLE_LENGTH', 'BODY_LENGTH'],
          'post_text_data': ['PostId', 'UserId', 'Q_Title', 'Q_Body', 'TITLE_LENGTH', 'BODY_LENGTH'],
          'users_activity': ['PostId', 'UserId', 'TimePosted', 'PostType'],
          'accepted_answers': ['AcceptedAnswerId', 'UserId'],
          'posts_stats': ['TimeCreated', 'PostTypeId'],
          'users_behaviour': ['q', 'a', 'av', 'u', 'v', 'qa', 'qv', 'qva'],
          'tags_stats': [ 'QuestionId', 'SecondsToUpvotedAnswer', 'Q_Body', 'Tags'],
          'title_stats': ['TITLE_LENGTH', 'BODY_LENGTH', 'ANSWERS_NUM', 'Q_TITLE'],
          'users_activity_features': ['UserId', 'Q_U_MONTH', 'Q_U_HOUR', 'A_U_MONTH', 'A_U_HOUR'],
          'users_activity_temporal': ['UserId', 'Q_WEEK', 'A_WEEK', 'P_WEEK'],
          'users_posts_times': ['PostId', 'UserId', 'TimePosted', 'PostType', 'year', 'month', 'day', 'hour', 'min']}

#FILES_U = ["users_stats", "accepted_answers_per_user", "answer_per_user", "quest_per_user", "user_av_ans_time", "posts_per_user", "users_activity_features", "users_locations1"]
FILES = {'U': ["users_stats", "answer_per_user", "quest_per_user", "users_av_ans_time", "posts_per_user", "derived_data/users_locations1", "derived_data/accepted_answers_per_user"],
         'UD': ["accepted_answers_per_user", "users_locations1"],
         'Q': ["derived_data/NLP_features", "tags/tags_stats1", "quest_stats1", "derived_data/quest_weekend", "derived_data/post_title_length1"],
         'ALL': ['data_for_ML/QUESTIONS', 'data_for_ML/USERS'],
         'ML': ['data_for_ML/DATA_MERGED', 'data_for_ML/TEMP_CL'],
         'ML1': ['data_for_ML/DATA_MERGED', 'data_for_ML/TEMP_CL1', 'data_for_ML/TEMP_CL2', 'data_for_ML/TEMP_CL3', 'data_for_ML/TEMP_CL4', 'data_for_ML/TEMP_CL5']}

KEYS = {'U': [['UserId', 'UserId', 'UserId', 'UserId', 'UserId', 'UserId', 'UserId', 'UserId'],['UserId', 'UserId', 'UserId', 'UserId', 'UserId', 'UserId', 'UserId']],
        'Q': [['PostID', 'QuestionId', 'QuestionId', 'QuestionId'],['QuestionId','QuestionId','QuestionId', 'QuestionId']],
        'ALL': [['UserId'], ['UserId']],
        'ML': [['QuestionId'], ['QuestionId']]}

file_name = {'u': "data_for_ML/USERS.csv",
             'q': "data_for_ML/QUESTIONS.csv",
             'all': "data_for_ML/DATA_MERGED.csv",
             'ml': "data_for_ML/data_ML.csv"}
