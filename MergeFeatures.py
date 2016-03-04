__author__ = 'nb254'

import pandas as pd
import FeatureSelector as fs

def mergePostFeatures(DIR):
    df = pd.read_csv(DIR + 'posts/quest_stats.csv')
    #print 'samples in posts before merging', len(df)
    df1 = pd.read_csv(DIR + 'posts/nlp_features.csv')
    df2 = pd.read_csv(DIR + 'posts/users_activity.csv')
    #df3 = pd.read_csv(DIR + 'posts/ans_time_accepted.csv') #TODO somehow dublicated
    df3 = pd.read_csv(DIR + 'posts/tags/tag_features.csv')
    df4 = pd.read_csv(DIR + 'posts/tags/tag_specificity.csv')
    df5 = pd.read_csv(DIR + 'posts/tags/num_tags.csv')
    df6 = pd.read_csv(DIR + 'posts/post_text_lengths.csv')
    df7 = pd.read_csv(DIR + 'posts/TEMP_CL.csv')
    dfs = [df1, df2,  df3, df4, df5, df6, df7]
    #dfs = [df1, df2]
    df_res = df
    for df in dfs:
         df_res = pd.merge(df_res, df, how='left', on='PostId')
    return df_res

def mergeUserFeatures(DIR):
    df = pd.read_csv(DIR + 'users/data_loc.csv')
    df = df.sort('UserId', ascending=True)
    #print df
    #print 'samples in users before merging', len(df)
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
    col_names = fs.UserFeatures + fs.PostsFeatures
    col_names.remove('TAG_SPECIFICITY')

    rows_with_strings  = df.apply(
       lambda row :
          any([ isinstance(e, basestring) for e in row ])
       , axis=1)
    df = df[~rows_with_strings]
    #print ~df.applymap(pd.np.isreal)
    print df['LON'].median()
    print df['LAT'].median()
    for col_name in col_names:
        print col_name
        df[col_name] = df[col_name].astype(int)
    return df

def mergeAll(DIR, key_users, key_posts, FeaturePredict):
    df_p = mergePostFeatures(DIR)
    df_p = df_p[key_posts + fs.PostsFeatures + FeaturePredict]
    #print 'samples in posts', len(df_p)
    df_p.to_csv(DIR + 'posts_all.csv')
    df_u = mergeUserFeatures(DIR)
    df_u = df_u[key_users + fs.UserFeatures]
    #print 'samples in users', len(df_p)
    df_u.to_csv(DIR + 'users_all.csv')
    df_ML = pd.merge(df_p, df_u, how='left', on='UserId')
    df_ML = cleanData(df_ML)
    return df_ML

