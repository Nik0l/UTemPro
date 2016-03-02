__author__ = 'nb254'
import csv
import pandas as pd
from Features import features as features
from Variables import FILES as files
from Variables import KEYS as keys
from Variables import file_name as file_name
from Variables import DIR_DATA as DIR
import FeatureExtractor as extractor

def mergePostFeatures():
    df = pd.read_csv(DIR + 'posts/quest_stats.csv')

    df1 = pd.read_csv(DIR + 'posts/nlp_features.csv')
    df2 = pd.read_csv(DIR + 'posts/users_activity.csv')
    #df3 = pd.read_csv(DIR + 'posts/ans_time_accepted.csv') #TODO somehow dublicated
    df3 = pd.read_csv(DIR + 'posts/tags/tag_features.csv')
    df4 = pd.read_csv(DIR + 'posts/tags/tag_specificity.csv')
    df5 = pd.read_csv(DIR + 'posts/post_text_lengths.csv')
    df6 = pd.read_csv(DIR + 'posts/TEMP_CL.csv')
    dfs = [df1, df2,  df3, df4, df5, df6]
    #dfs = [df1, df2]
    df_res = df
    for df in dfs:
         df_res = pd.merge(df_res, df, how='left', on='PostId')
    return df_res

def mergeUserFeatures():
    df = pd.read_csv(DIR + 'users/data_loc.csv')

    df1 = pd.read_csv(DIR + 'users/accepted_answers_per_user.csv')
    df2 = pd.read_csv(DIR + 'users/quest_per_user.csv')
    df3 = pd.read_csv(DIR + 'users/answer_per_user.csv')
    df4 = pd.read_csv(DIR + 'users/users_av_ans_time.csv')
    df5 = pd.read_csv(DIR + 'users/temp_features.csv')
    df6 = pd.read_csv(DIR + 'users/temporal_user_activities.csv')

    dfs = [df1, df2, df3, df4, df5, df6]
    df_res = df
    for df in dfs:
         df_res = pd.merge(df_res, df, how='left', on='UserId')
    return df_res

def cleanData(df):
    #TODO clean the data
    df = df.fillna(0)
    col_names = UserFeatures + PostsFeatures
    col_names.remove('TAG_SPECIFICITY')
    for col_name in col_names:
       df[col_name] = df[col_name].astype(int)
    return df

def mergeAll(key_users, key_posts):
    df_p = mergePostFeatures()
    df_p = df_p[key_posts + PostsFeatures]
    df_p.to_csv(DIR + 'posts_all.csv')
    df_u = mergeUserFeatures()
    df_u = df_u[key_users + UserFeatures]
    df_u.to_csv(DIR + 'users_all.csv')
    df_ML = df_res = pd.merge(df_p, df_u, how='left', on='UserId')
    df_ML = cleanData(df_ML)
    return df_ML

def normalize(df):
    df_norm = (df - df.mean()) / (df.max() - df.min())
    df_norm = df_norm - df_norm.min()
    return df_norm

#db_name = 'beer'
db_name = 'stackoverflow'
DIR = '/mnt/nb254_data/exp/'
key_users = ['UserId']
key_posts = ['PostId']

UserFeatures = ['U_QUESTIONS', 'U_ANSWERS', 'NUM_OF_A_ACCEPTED_BY_OTHERS',
                'U_AV_ANS_TIME', 'DAYS_ON_SITE', 'U_REPUTATION', 'U_UPVOTES', 'U_DOWNVOTES',
                'U_VIEWS', 'time_diff', 'qh1', 'qh2', 'qh3', 'qh4',
                'qh5', 'qh6', 'qh7', 'qh8', 'qh9', 'qh10', 'qh11', 'qh12', 'qh13', 'qh14',
                'qh15', 'qh16', 'qh17', 'qh18', 'qh19', 'qh20', 'qh21', 'qh22', 'qh23', 'qh24',
                'qm1', 'qm2', 'qm3', 'qm4', 'qm5', 'qm6', 'qm7', 'qm8', 'qm9', 'qm10', 'qm11',
                'qm12', 'Q_LAST_WEEK', 'A_LAST_WEEK', 'P_NUM_LAST_DAY']

PostsFeatures = ['UserId', 'Q_VIEWS', 'WH_TITLE', 'WH_BODY', 'VERBS_TITLE', 'VERBS_BODY', 'SELF_REF_BODY',
                 'TITLE_LENGTH', 'BODY_LENGTH', 'TAG_POPULARITY_AV', 'NUM_POP_TAGS', 'TAG_SPECIFICITY',
                 'URLS_BODY', 'IMAGES_BODY']
FeaturePredict = ['TEMP_CL']

# extracts all features
extractor.extractForML(db_name, DIR)
dfML = mergeAll(key_users, key_posts)
dfML.to_csv(DIR + 'dataML.csv', index=False)
dfnorm = normalize(dfML)
dfnorm.to_csv(DIR + 'normMLa.csv', index=False)  
