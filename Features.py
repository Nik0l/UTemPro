#Script to extract features.
__author__ = 'nb254'
# features used in the predictions #
UserId          = {'name': "UserId", 'x_from': 0, 'x_to': 1500000, 'title': "User's Id"}
U_QUESTIONS     = {'name': "U_QUESTIONS",'x_from': 0, 'x_to': 1500000, 'title': "Number of questions"}
U_ANSWERS       = {'name': "U_ANSWERS",'x_from': 0, 'x_to': 1500000, 'title': "Number of answer"}
U_A_ANSWERS_OTH = {'name': "NUMBER_OF_A_ANSWERS_BY_OTHERS", 'x_from': 0, 'x_to': 2000, 'title': "Number of accepted answers of a user by other users"}
U_POSTS         = {'name': "U_POSTS",'x_from': 0, 'x_to': 2000, 'title': "Number of posts"}
U_AV_ANS_TIME   = {'name': "U_AV_ANS_TIME",'x_from': 0, 'x_to': 2000, 'title': "Average answering time for previous questions"}
LOCATION        = {'name': "LOCATION",'x_from': 0, 'x_to': 2000, 'title': "Location of a questioner"}
DAYS_ON_SITE    = {'name': "DAYS_ON_SITE",'x_from': 0, 'x_to': 2000, 'title': "Days in the community"}
U_REPUTATION    = {'name': "U_REPUTATION",'x_from': 0, 'x_to': 2000, 'title': "Reputation of a questioner"}
U_UPVOTES       = {'name': "U_UPVOTES",'x_from': 0, 'x_to': 2000, 'title': "Number of upvotes by other users"}
U_DOWNVOTES     = {'name': "U_DOWNVOTES",'x_from': 0, 'x_to': 2000, 'title': "Number of downvotes by other users"}
U_VIEWS         = {'name': "U_VIEWS",'x_from': 0, 'x_to': 1500000, 'title': "Number of user's views"}
time_diff       = {'name': "time_diff",'x_from': -1200, 'x_to': 1200, 'title': "Time difference"}
RESP_TIME       = {'name': "SecondsToAcceptedAnswer", 'x_from': 0, 'x_to': 200000000, 'title': "Response time in seconds"}
Q_VIEWS         = {'name': "Q_VIEWS",'x_from': 0, 'x_to': 1500000, 'title': "Number of question views"}
LAT             = {'name': "LAT",'x_from':-90, 'x_to': 90, 'title': "Latitude of a questioner"}
LON             = {'name': "LON",'x_from': -180, 'x_to': 180, 'title': "Longitude of a questioner"}

WH_TITLE        = {'name': "WH_TITLE",'x_from': 0, 'x_to': 20, 'title': "Number of 'wh' in the title of a question"}
WH_BODY         = {'name': "WH_BODY",'x_from': 0, 'x_to': 20, 'title': "Number of 'wh' in the body of a question"}
Q_MARKS_TITLE   = {'name': "Q_MARKS_TITLE",'x_from': 0, 'x_to': 20, 'title': "Number of question marks in the title of a question"}
Q_MARKS_BODY    = {'name': "Q_MARKS_BODY",'x_from': 0, 'x_to': 20, 'title': "Number of question marks in the body of a question"}
VERBS_TITLE     = {'name': "VERBS_TITLE",'x_from': 0, 'x_to': 20, 'title': "Number of verbs in the title of a question"}
SELF_REF_TITLE  = {'name': "SELF_REF_TITLE",'x_from': 0, 'x_to': 20, 'title': "Number of self-referencing in the title of a question"}
SELF_REF_BODY   = {'name': "SELF_REF_BODY",'x_from': 0, 'x_to': 20, 'title': "Number of self-referencing in the body of a question"}
URLS_BODY       = {'name': "URLS_BODY",'x_from': 0, 'x_to': 300, 'title': "Number of urls in the body of a question"}
IMAGES_BODY     = {'name': "IMAGES_BODY",'x_from': 0, 'x_to': 300, 'title': "Number of images in the body of a question"}
CODE_BLOCKS     = {'name': "CODE_BLOCKS",'x_from': 0, 'x_to': 20, 'title': "Number of code blocks in the body of a question"}
TOTAL_CODE_LEN  = {'name': "TOTAL_CODE_LENGTH",'x_from': 0, 'x_to': 20, 'title': "Total code length in characters in the body of a question"}
TAG_POP_AV      = {'name': "TAG_POPULARITY_AV",'x_from': 0, 'x_to': 20, 'title': "Popularity of tags in a question"}
NUM_POP_TAGS    = {'name': "NUM_POP_TAGS",'x_from': 0, 'x_to': 20, 'title': "Number of popular tags in a question"}
WEEKDAY_Q       = {'name': "WEEKDAY_Q",'x_from': 0, 'x_to': 20, 'title': "Work day when a questions was asked"}

# users' features
U_FEATURES = [UserId, U_QUESTIONS, U_ANSWERS, U_A_ANSWERS_OTH, U_POSTS, U_AV_ANS_TIME, LOCATION, LAT, LON, DAYS_ON_SITE, U_REPUTATION, U_UPVOTES, U_DOWNVOTES, U_VIEWS, time_diff]
# post features
P_FEATURES = [WH_TITLE, WH_BODY, Q_MARKS_TITLE, Q_MARKS_BODY, VERBS_TITLE, SELF_REF_TITLE, SELF_REF_BODY, URLS_BODY, IMAGES_BODY, IMAGES_BODY, CODE_BLOCKS, TOTAL_CODE_LEN, Q_VIEWS, RESP_TIME]
# tag features
T_FEATURES = [TAG_POP_AV, NUM_POP_TAGS]
# all features
FEATURE_LIST = U_FEATURES + P_FEATURES + T_FEATURES

NLP_FEATURES  = ['WH_TITLE', 'WH_BODY', 'Q_MARKS_TITLE', 'Q_MARKS_BODY', 'VERBS_TITLE', 'VERBS_BODY', 'SELF_REF_TITLE', 'SELF_REF_BODY', 'URLS_BODY', 'IMAGES_BODY', 'CODE_BLOCKS', 'TOTAL_CODE_LENGTH']
KEYS          = ['PostID', 'UserId']
KEY           = ['QuestionId']
KEYS_US_ACT   = ['QuestionId', 'UserId', 'AnswererId', 'Tags', 'TimeAnswered']
KEY_LOC       = ['Location']
TIME_FEATURES = ['WEEKDAY_Q', 'WEEKEND_Q', 'WEEKDAY_A', 'WEEKEND_A']
TAG_KEYS      = ['QuestionId', 'Tags']
TAG_FEATURES  = ['TAG_POPULARITY_AV', 'NUM_POP_TAGS', 'TAG_SPECIFICITY']
USER_ACTIVITY = ['NUM_SUBS_ANS', 'PERCENT_SUBS_ANS', 'NUM_SUBS_T', 'PERSENT_SUBS_T']
USER_LOC      = ['LAT', 'LON', 'TIME_ZONE', 'time_diff', 'DISTANCE', 'COUNTRY', 'ADMIN_REGION']


##################### users' related features#####################
features = {'usr': ["UserId"],
            'qst': ["U_QUESTIONS"],
            'ans': ["U_ANSWERS"],
            'aca': ["NUM_OF_A_ACCEPTED_BY_OTHERS"],
            'pos': ["U_POSTS"],
            'ant': ["U_AV_ANS_TIME"],
            'ustats': ["LOCATION", "DAYS_ON_SITE", "U_REPUTATION", "U_UPVOTES", "U_DOWNVOTES", "U_VIEWS"],
            'loc': ['LOCATION', 'LON', 'LAT', 'TIME_ZONE', 'time_diff', 'COUNTRY', 'ADMIN_REGION', 'USERS_SAME_LOC'],
            'act': ['Q_U_MONTH', 'Q_U_HOUR', 'A_U_MONTH', 'A_U_HOUR'],
            'q_stat_old': ['QuestionId', 'UserId', 'AnswererId', 'SecondsToAcceptedAnswer', 'Q_VIEWS'],
            #'q_stat': ['QuestionId', 'AnswererId', 'SecondsToAcceptedAnswer', 'Q_VIEWS'],
            'q_stat': ['QuestionId', 'AnswererId', 'SecondsToAcceptedAnswer', 'Q_VIEWS', 'TimeAsked'],
            #'nlp': ['UserId', 'WH_TITLE', 'WH_BODY', 'Q_MARKS_TITLE', 'Q_MARKS_BODY', 'VERBS_TITLE', 'VERBS_BODY', 'SELF_REF_TITLE', 'SELF_REF_BODY', 'URLS_BODY', 'IMAGES_BODY', 'CODE_BLOCKS', 'TOTAL_CODE_LENGTH'],
            'nlp': ['WH_TITLE', 'WH_BODY', 'Q_MARKS_TITLE', 'Q_MARKS_BODY', 'VERBS_TITLE', 'VERBS_BODY', 'SELF_REF_TITLE', 'SELF_REF_BODY', 'URLS_BODY', 'IMAGES_BODY', 'CODE_BLOCKS', 'TOTAL_CODE_LENGTH'],
            'tags': ['TAG_POPULARITY_AV', 'NUM_POP_TAGS', 'TAG_SPECIFICITY'],
            'wknd': ['WEEKDAY_Q', 'WEEKEND_Q', 'WEEKDAY_A', 'WEEKEND_A']}

class Feature:
    """A class representing features of qa forums"""
    name   = ''
    x_from = 0
    x_to   = 0
    title  = ''

    def __init__(self, name, x_from, x_to, title):
        self.name   = name
        self.x_from = x_from
        self.x_to   = x_to
        self.title  = title

#for feature in FEATURE_LIST:
   #print feature['name']
