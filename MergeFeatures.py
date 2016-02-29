__author__ = 'nb254'
import csv
import pandas as pd
from Features import features as features
from Variables import FILES as files
from Variables import KEYS as keys
from Variables import file_name as file_name
from Variables import DIR_DATA as DIR

#create a label '1' if longer than an hour and '0' otherwise
HOUR    = 60 * 60 # one hour = 60 seconds by 60 minutes
#MEDIAN_TIME = 21174 #for fitness
FIVE_MINUTES = 5 * 60 # 5 minutes
DAY = HOUR * 24
MONTH = DAY * 30
MEDIAN_TIME = 491
TEST_TIME = 82000 #for fitness
MED_REAL = 60 * 30
#COLS_U  =  features_usr + features_qst + features_ans + features_aca + features_pos + features_ant + features_ustats + features_loc + features_act
COLS = {'U': features['usr'] +
             features['qst'] +
             features['ans'] +
             features['aca'] +
             features['pos'] +
             features['ant'] +
             features['ustats'],
        'Q': features['q_stat'] +
             features['usr'] +
             features['nlp'] +
             features['tags'] +
             features['wknd'] +
             ['Tags'] + ['TITLE_LENGTH'] + ['BODY_LENGTH']}
print COLS['U']
COLS['U'] = COLS['U'] + features['loc']
print COLS['U']
print COLS['Q']

def make_label(table, time_stamp, file_name):
    i = 0;
    myfile = open(file_name, 'wb')
    wr = csv.writer(myfile)
    wr.writerow(['QuestionId', 'TEMP_CL'])
    for elem in table['SecondsToAcceptedAnswer']:
      if elem > time_stamp:
         row = int(1)
         #print 'larger than 3600: ', elem
      else:
         row = int(0)
         #print 'smaller than 3600: ', elem
      wr.writerow([table['QuestionId'][i], row])
      i = i + 1

#merge files on questionss
def Merge(files, keys, file_name, keep_cols, how_merge):
   f = []
   for file_m in files:
     print file_m
     f.append(pd.read_csv(DIR + file_m + '.csv', error_bad_lines=False))
     print 'success'
   merged = f[0]
   for i in range (1, len(f)):
       if how_merge == '1':
          merged = pd.merge(merged, f[i], left_on = keys[0][i-1], right_on = keys[1][i-1])
       elif how_merge == '2':
          merged = pd.merge(merged, f[i], how='outer', left_on = keys[0][i-1], right_on = keys[1][i-1])
   #before saving the file, choose only required columns
   #print merged.head
   new_u = merged[keep_cols]
   #new_u = new_u
   new_u.to_csv(DIR + file_name, index=False)
   return new_u

def Rename(file_m, to_file_m, column_name_old, column_name_new):
   data = pd.read_csv(DIR + file_m, error_bad_lines=False)
   data.rename(columns={column_name_old: column_name_new}, inplace = True)
   data.to_csv(DIR + to_file_m, index=False)

def MergeUserFeatures():
   new_u = Merge(files['U'], keys['U'], file_name['u'], COLS['U'], '2')

def MergeQuestFeatures():
   Rename("tags/tags_stats.csv", "tags/tags_stats1.csv", 'Tags', 'Tags1')
   Rename("quest_stats.csv", "quest_stats1.csv", 'UserId', 'UserId1')
   Rename('derived_data/post_title_length.csv', 'derived_data/post_title_length1.csv', 'PostId', 'QuestionId')
   Rename('derived_data/post_title_length.csv', 'derived_data/post_title_length1.csv', 'UserId', 'UserId1')
   new_q = Merge(files['Q'], keys['Q'], file_name['q'], COLS['Q'], '1')

def MergeAll():
   new = Merge(files['ALL'], keys['ALL'], file_name['all'], COLS['U'] + COLS['Q'], '2')

def CreateTimeLabel(TIME, filename):
   new = pd.read_csv(DIR + 'quest_stats1.csv', error_bad_lines=False)
   table = make_label(new, TIME, filename)
   #print table

def CreateDataForML(FILES_NAMES):
   ################  finallly...  ###############
   #CreateTimeLabels()
   COLS_ML = COLS['U'] + COLS['Q'] + ['TEMP_CL']
   COLS_ML.remove('SecondsToAcceptedAnswer')
   new = Merge(files[FILES_NAMES], keys[FILES_NAMES], file_name['ml'], COLS_ML, '2')

def PrepareData():
   MergeUserFeatures()
   MergeQuestFeatures()
   MergeAll()
   CreateTimeLabel(MEDIAN_TIME, DIR + 'data_for_ML/TEMP_CL.csv')
   CreateDataForML('ML')

def CreateTimeLabels():
   CreateTimeLabel(FIVE_MINUTES, DIR + 'data_for_ML/TEMP_CL1.csv')
   CreateTimeLabel(MEDIAN_TIME, DIR + 'data_for_ML/TEMP_CL2.csv')
   CreateTimeLabel(HOUR, DIR + 'data_for_ML/TEMP_CL3.csv')
   CreateTimeLabel(DAY, DIR + 'data_for_ML/TEMP_CL4.csv')
   CreateTimeLabel(MONTH, DIR + 'data_for_ML/TEMP_CL5.csv')

def addUserActivityFeatures():
    df1 = pd.read_csv(DIR + 'data_for_ML/DATA_MERGED.csv')
    df4 = pd.read_csv(DIR + 'data_for_ML/useractivity.csv')
    file_name = 'data_for_ML/merged.csv'
    result = pd.merge(df1, df4, on='QuestionId')
    result.to_csv(DIR + file_name)

def addMoreUserActivityFeatures():
    #step 1 - merge all temporal features
    #df1 = pd.read_csv(DIR + 'temporal/temp_features1.csv')
    #df2 = pd.read_csv(DIR + 'temporal/temp_features.csv')
    #result = pd.merge(df1, df2, how='left', on='UserId')
    file_name = 'temporal/temp_features_all.csv'
    #result.to_csv(DIR + file_name)

    df3 = pd.read_csv(DIR + 'data_for_ML/data_ML.csv')
    df4 = pd.read_csv(DIR + file_name)
    file_name1 = 'data_for_ML/merged_all.csv'
    df5 = pd.merge(df3, df4, how='left', on='UserId')

    tag_spec = pd.read_csv('/mnt/nb254_data/src/data_SO/tags/tag_specificity.csv')
    df5.drop(['TAG_SPECIFICITY'], axis=1, inplace=True)
    result = pd.merge(df5, tag_spec, how='left', on='QuestionId')
    result.to_csv(DIR + file_name1)

def prepareForML(df):
    # drop unnecessary columns
    df.drop(['COUNTRY', 'ADMIN_REGION', 'Unnamed: 0',
         'U_POSTS', 'LOCATION.1', 'TIME_ZONE', 'USERS_SAME_LOC',
         'AnswererId', 'TimeAsked', 'UserId.1', 'CODE_BLOCKS',
         'TOTAL_CODE_LENGTH', 'WEEKDAY_Q', 'WEEKEND_Q', 'WEEKDAY_A',
         'WEEKEND_A', 'Tags', 'ah1', 'ah2', 'ah3', 'ah4', 'ah5', 'ah6',
         'ah7', 'ah8', 'ah9', 'ah10', 'ah11', 'ah12', 'ah13', 'ah14',
         'ah15', 'ah16', 'ah17', 'ah18', 'ah19', 'ah20', 'ah21', 'ah22',
         'ah23', 'ah24', 'am1', 'am2', 'am3', 'am4', 'am5', 'am6', 'am7',
         'am8', 'am9', 'am10', 'am11', 'am12', 'Unnamed: 0.1.1', 'QuestionId'
         'Q_MARKS_TITLE', 'Q_MARKS_BODY', 'SELF_REF_TITLE', 'UserId'], axis=1, inplace=True)
    # drop rows where temporal label is null
    df = df[pd.notnull(df['TEMP_CL'])]
    df.to_csv('dropped_cols1.csv')

    df = pd.read_csv('dropped_cols1.csv')
    #print df.shape[0]
    #print df.shape[1]
    df = df[pd.notnull(df['LAT'])]
    #print df.shape[0]
    #print df.shape[1]
    df.drop(['Unnamed: 0'], axis=1, inplace=True)
    df.to_csv('dropped_cols2.csv', index=False)

    df = pd.read_csv('dropped_cols2.csv')
    df.drop(['Unnamed: 0.1'], axis=1, inplace=True)

    df2 = pd.read_csv('/mnt/nb254_data/src/data_SO/tags/num_tags.csv')
    df = pd.merge(df, df2, how='left', on='QuestionId')

    df.drop(['QuestionId'], axis=1, inplace=True)
    feature_list = ['U_QUESTIONS', 'U_ANSWERS', 'NUM_OF_A_ACCEPTED_BY_OTHERS',
                'U_AV_ANS_TIME', 'DAYS_ON_SITE', 'U_REPUTATION', 'U_UPVOTES', 'U_DOWNVOTES',
                'U_VIEWS', 'time_diff', 'Q_VIEWS', 'WH_TITLE', 'WH_BODY',
                'VERBS_TITLE', 'VERBS_BODY', 'SELF_REF_BODY', 'TAG_POPULARITY_AV',
                'NUM_POP_TAGS', 'TITLE_LENGTH', 'BODY_LENGTH', 'qh1', 'qh2', 'qh3', 'qh4',
                'qh5', 'qh6', 'qh7', 'qh8', 'qh9', 'qh10', 'qh11', 'qh12', 'qh13', 'qh14',
                'qh15', 'qh16', 'qh17', 'qh18', 'qh19', 'qh20', 'qh21', 'qh22', 'qh23', 'qh24',
                'qm1', 'qm2', 'qm3', 'qm4', 'qm5', 'qm6', 'qm7', 'qm8', 'qm9', 'qm10', 'qm11',
                'qm12', 'TEMP_CL', 'URLS_BODY', 'IMAGES_BODY', 'Q_LAST_WEEK', 'A_LAST_WEEK',
                'P_NUM_LAST_DAY']

    df.to_csv('dropped_cols3.csv', index=False)
    df = df.fillna(0)
    #, 'Q_LAST_WEEK', 'A_LAST_WEEK', 'P_NUM_LAST_DAY']
    for feature in feature_list:
       print feature
       df[feature] = df[feature].astype(int)
    df.to_csv('test2.csv', index=False)
    df1 = pd.read_csv('test2.csv')
    df2 = pd.read_csv('unique_locations_num.csv')
    result = pd.concat([df1, df2], axis=1)
    result.drop(['Q_MARKS_TITLE', 'LOCATION', 'Unnamed: 0'], axis=1, inplace=True)
    return result

def intFromLoc(df, filename):
    dloc = df['LOCATION']
    #print dloc.shape[0]
    #print dloc.shape[1]
    dloc_unique = list(set(dloc))
    #print dloc_unique
    #print len(dloc_unique)
    df1 = pd.DataFrame(dloc_unique, columns=['LOCATION'])
    df1.to_csv('unique_locations.csv')
    dfloc = pd.read_csv('unique_locations.csv')
    dfloc.columns = ['index', 'LOCATION']
    unique_num = []
    for index in xrange(0, len(df)):
        if df['LOCATION'][index] in dloc_unique:
           ind = dfloc[dfloc['LOCATION']== df['LOCATION'][index]].index.tolist()
           #print ind[0]
           unique_num.append(dfloc['index'][ind[0]])
           #print df['LOCATION'][index]
           if (index % 1000) == 0:
               print index
        else:
           print "doesn't work"
           print index
    df2 = pd.DataFrame(unique_num, columns=['LOCATION_NUM'])
    df2.to_csv(filename)
#PrepareData()
#MergeQuestFeatures()
#MergeUserFeatures()
#MergeAll()
#CreateTimeLabel(MED_REAL, DIR + 'TEMP_CL6.csv')
#CreateDataForML('ML')
#addMoreUserActivityFeatures()
df = pd.read_csv(DIR + 'data_for_ML/merged_all.csv')
#df = []
result = prepareForML(df)
print 'next...'
#intFromLoc(df, 'unique_locations_num.csv')
result.to_csv('final.csv', index=False)
'''
df3 = pd.read_csv('final.csv')
df3.drop(['Unnamed: 0.1.1'], axis=1, inplace=True)
'''
#result.to_csv('/mnt/nb254_data/src/data_SO/data_for_ML/final.csv', index=False)
