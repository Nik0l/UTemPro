__author__ = 'Nikolay Burlutskiy'

from Features import features as features
from itertools import combinations

BASIC = ['U_QUESTIONS', 'U_ANSWERS', 'NUM_OF_A_ACCEPTED_BY_OTHERS',
         'U_REPUTATION', 'U_UPVOTES', 'U_DOWNVOTES', 'U_VIEWS', 'Q_VIEWS']
AGE = ['DAYS_ON_SITE']
TAG1 = ['TAG_POPULARITY_AV', 'NUM_POP_TAGS', 'TAG_SPECIFICITY']
TAG2 = ['NUM_TAGS']
NLP = ['WH_TITLE', 'WH_BODY', 'TITLE_LENGTH', 'BODY_LENGTH', 'VERBS_TITLE', 'VERBS_BODY',
       'SELF_REF_BODY', 'URLS_BODY', 'IMAGES_BODY']
SPATIAL = ['LON', 'LAT', 'LOCATION_NUM', 'time_diff']
P_U_HOUR = ['qh1', 'qh2', 'qh3', 'qh4', 'qh5', 'qh6', 'qh7', 'qh8', 'qh9', 'qh10', 'qh11', 'qh12',
    'qh13', 'qh14', 'qh15', 'qh16', 'qh17', 'qh18', 'qh19', 'qh20', 'qh21', 'qh22', 'qh23', 'qh24']
P_U_MONTH = ['qm1', 'qm2', 'qm3', 'qm4', 'qm5', 'qm6', 'qm7', 'qm8', 'qm9', 'qm10', 'qm11', 'qm12']
TEMPORAL = ['U_AV_ANS_TIME', 'Q_LAST_WEEK', 'A_LAST_WEEK', 'P_NUM_LAST_DAY']

def setAllFeatures():
    features_all = ['QuestionId', 'SecondsToAcceptedAnswer', 'U_REPUTATION',
          'U_QUESTIONS', 'U_ANSWERS', 'NUM_OF_A_ACCEPTED_BY_OTHERS', 'U_POSTS', 'U_AV_ANS_TIME',
          'DAYS_ON_SITE', 'U_REPUTATION', 'U_UPVOTES', 'U_DOWNVOTES', 'U_VIEWS', 'Q_VIEWS',
          'LON', 'LAT', 'time_diff', 'USERS_SAME_LOC', 'WH_TITLE', 'WH_BODY','DAYS_ON_SITE',
          'Q_MARKS_TITLE', 'Q_MARKS_BODY', 'VERBS_TITLE', 'VERBS_BODY', 'SELF_REF_TITLE', 'SELF_REF_BODY',
          'URLS_BODY', 'IMAGES_BODY', 'CODE_BLOCKS', 'TOTAL_CODE_LENGTH', 'WEEKDAY_Q'] + features['tags']
    #features_all.remove('TAG_SPECIFICITY')
    return features_all

def setFeaturesVariations():
    features_s = ['QuestionId', 'SecondsToAcceptedAnswer', 'LAT', 'LON', 'time_diff', 'USERS_SAME_LOC']
    features_st = ['QuestionId', 'SecondsToAcceptedAnswer', 'LAT', 'LON', 'time_diff', 'USERS_SAME_LOC',
               'NUM_OF_A_ACCEPTED_BY_OTHERS', 'U_AV_ANS_TIME','WEEKDAY_Q']
    features_u_st = ['QuestionId', 'SecondsToAcceptedAnswer', 'U_REPUTATION',
          'U_QUESTIONS', 'U_ANSWERS', 'U_POSTS', 'DAYS_ON_SITE', 'U_REPUTATION', 'U_UPVOTES',
          'U_DOWNVOTES', 'U_VIEWS', 'Q_VIEWS', 'WH_TITLE', 'WH_BODY','DAYS_ON_SITE',
          'Q_MARKS_TITLE', 'Q_MARKS_BODY', 'VERBS_TITLE', 'VERBS_BODY', 'SELF_REF_TITLE', 'SELF_REF_BODY',
          'URLS_BODY', 'IMAGES_BODY', 'CODE_BLOCKS', 'TOTAL_CODE_LENGTH', 'WEEKDAY_Q']
    features_u_tag = ['QuestionId', 'SecondsToAcceptedAnswer', 'U_REPUTATION',
          'U_QUESTIONS', 'U_ANSWERS', 'U_POSTS', 'DAYS_ON_SITE', 'U_REPUTATION', 'U_UPVOTES',
          'U_DOWNVOTES', 'U_VIEWS', 'Q_VIEWS', 'WH_TITLE', 'WH_BODY','DAYS_ON_SITE',
          'Q_MARKS_TITLE', 'Q_MARKS_BODY', 'VERBS_TITLE', 'VERBS_BODY', 'SELF_REF_TITLE', 'SELF_REF_BODY',
          'URLS_BODY', 'IMAGES_BODY', 'CODE_BLOCKS', 'TOTAL_CODE_LENGTH', 'WEEKDAY_Q'] + features['tags']
    features_u_tag.remove('TAG_SPECIFICITY')
    features_all_no_nlp = ['QuestionId', 'SecondsToAcceptedAnswer', 'U_REPUTATION',
          'U_QUESTIONS', 'U_ANSWERS', 'NUM_OF_A_ACCEPTED_BY_OTHERS', 'U_POSTS', 'U_AV_ANS_TIME',
          'DAYS_ON_SITE', 'U_REPUTATION', 'U_UPVOTES', 'U_DOWNVOTES', 'U_VIEWS', 'Q_VIEWS',
          'LON', 'LAT', 'time_diff', 'USERS_SAME_LOC', 'WEEKDAY_Q'] + features['tags']
    #features_all_no_nlp.remove('TAG_SPECIFICITY')
    features_all = setAllFeatures()
    features_variations = [features_s, features_st, features_u_st, features_u_tag, features_all_no_nlp, features_all]
    return features_variations

def setFeaturesToUse():
    features_to_use = ['QuestionId', 'SecondsToAcceptedAnswer', 'U_REPUTATION', #'DAYS_ON_SITE',
          'U_QUESTIONS', 'U_ANSWERS', 'NUM_OF_A_ACCEPTED_BY_OTHERS', 'U_POSTS', 'U_AV_ANS_TIME',
          'DAYS_ON_SITE', 'U_REPUTATION', 'U_UPVOTES', 'U_DOWNVOTES', 'U_VIEWS', 'Q_VIEWS',
          'LON', 'LAT', 'time_diff', 'USERS_SAME_LOC', 'WH_TITLE', 'WH_BODY','DAYS_ON_SITE',
          'Q_MARKS_TITLE', 'Q_MARKS_BODY', 'VERBS_TITLE', 'VERBS_BODY', 'SELF_REF_TITLE', 'SELF_REF_BODY',
          'URLS_BODY', 'IMAGES_BODY', 'CODE_BLOCKS', 'TOTAL_CODE_LENGTH', 'WEEKDAY_Q'] + features['tags']
    #features_to_use.remove('TAG_SPECIFICITY')
    return features_to_use

def setFeaturesToUseAll():
    features_to_use = BASIC + AGE + NLP + SPATIAL + TEMPORAL + P_U_HOUR + P_U_MONTH + TAG
    return features_to_use

def selectFeatures(name, feature_predict):
   #LABEL = ['TEMP_CL']
   #################
   RAW_LIGHT = BASIC
   EASY_LIGHT = AGE + NLP + TAG2
   HARD_ST = SPATIAL + TEMPORAL + P_U_HOUR + P_U_MONTH
   HARD_TAG = TAG1
   FEATURES = {'RL': " + ".join(RAW_LIGHT),
               'EL': " + ".join(EASY_LIGHT),
               'HS': " + ".join(HARD_ST),
               'HT': " + ".join(HARD_TAG)
   }
   features = ''
   if name == 'all':
       features = FEATURES['RL'] + ' + ' + \
                  FEATURES['EL'] + ' + ' +\
                  FEATURES['HS'] + ' + ' +\
                  FEATURES['HT']
       print features
   elif name == 'RL':
       features = FEATURES['RL']
       print features
   elif name == 'NOTAGS':
       features = FEATURES['RL'] + ' + ' + \
                  FEATURES['EL'] + ' + ' +\
                  FEATURES['HS']
   elif name == 'NOSTEMP':
       features = FEATURES['RL'] + ' + ' + \
                  FEATURES['EL'] + ' + ' +\
                  FEATURES['HT']
   features = feature_predict[0] + ' ~ ' + features
   print features
   return features

def AllCombinations(list_of_elements):
   combs = []
   for L in range(0, len(list_of_elements) + 1):
     for subset in combinations(list_of_elements, L):
       combs.append(subset)
       print(subset)
   return combs

#selectFeatures('all', ['TEMP_CL'])

'''
FEATURES = {'wnd_q': 'WEEKDAY_Q + WEEKEND_Q',
            'wnd_a': 'WEEKDAY_A + WEEKEND_A',
            'nlp': 'WH_TITLE + WH_BODY + Q_MARKS_TITLE + Q_MARKS_BODY + VERBS_TITLE + VERBS_BODY + '
                   'SELF_REF_TITLE + SELF_REF_BODY + URLS_BODY + IMAGES_BODY',
            'tags': 'TAG_POPULARITY_AV + NUM_POP_TAGS',#'tags': 'TAG_POPULARITY_AV + NUM_POP_TAGS + TAG_SPECIFICITY',
            'user': 'U_QUESTIONS + U_ANSWERS + U_POSTS + NUM_OF_A_ACCEPTED_BY_OTHERS + DAYS_ON_SITE + '
                    'U_REPUTATION + U_UPVOTES + U_DOWNVOTES + U_VIEWS',
            'tmp': 'U_AV_ANS_TIME',
            'loc': 'LAT + LON + time_diff'} #'loc': 'LAT + LON + TIME_ZONE + time_diff'
if name == 'all':
       features = FEATURES['wnd_q'] + ' + ' + \
                  FEATURES['nlp']+'+'+\
                  FEATURES['tags']+' + '+\
                  FEATURES['user']+' + '+\
                  FEATURES['tmp']+' + '+\
                  FEATURES['loc']
       print features
   elif name == 'usr':
       features = FEATURES['user']
   elif name == 'qst':
       features = FEATURES['nlp']
       print features
   elif name == 'qst_full':
       features = FEATURES['nlp'] + ' + ' + \
                  FEATURES['tags']
   elif name == 'all_no_temp_spat':
       features = FEATURES['nlp']+' + '+\
                  FEATURES['tags']+' + '+\
                  FEATURES['user']
       print features
   elif name == 'all_no_tags':
       features = FEATURES['wnd_q']+ ' + '+\
                  FEATURES['nlp']+' + '+\
                  FEATURES['user']+' + '+\
                  FEATURES['tmp']
       print features
   elif name == 'NLP':
       _features = list(df.columns.values)
       _features.remove('TEMP_CL')
       _features.remove('QuestionId')
       features = "+".join(_features)

   features = feature_predict[0] + '~' + features
