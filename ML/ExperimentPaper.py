import MLSetup as ml
import pandas as pd
import MergeFeatures as mf
import os
import FeatureExtractor as extractor
import DataPreprocessing as dp

# the path to the file with data
FeaturePredict = ['TEMP_CL']

def extractFeaturesML(db_name, DIR):
    key_users = ['UserId']
    key_posts = ['PostId']
    # extracts all features
    extractor.extractForML(db_name, DIR)
    dfML = mf.mergeAll(DIR, key_users, key_posts, FeaturePredict)
    dfML.to_csv(DIR + 'dataML.csv', index=False)
    dfnorm = dp.normalize(dfML)
    return dfnorm

def run_ML(df):
    feature_sets = ['RL', 'NOTAGS', 'NOSTEMP', 'all']
    #feature_sets = ['all']
    dfres = ml.runExpNtimes(df, feature_sets, repetitions=10)
    dfres = dfres.sort(['Learning_Type', 'Algorithm', 'Features'], ascending=False)
    dfresa = ml.makeFirstTable(dfres)
    if not os.path.exists(DIR + 'results/'):
        os.makedirs(DIR + 'results/')
    dfresa.to_csv(DIR + 'results/results_algorithms.csv', index=False)
    dfresb = ml.makeSecondTable(dfres)
    dfresb.to_csv(DIR + 'results/results_features.csv', index=False)
    print dfresb

def resample(df, column, method):
    num = [len(df[df[column] == 1.0]),
           len(df[df[column] == 0.0])]
    print 'classes:', num
    min_num = min(num[0], num[1])
    if method == 'downsample':
        print 'downsample both classes to ' + str(min_num)
        df1 = df[df[column] == 1.0].sample(n=min_num)
        df2 = df[df[column] == 0.0].sample(n=min_num)
        df = pd.concat([df1, df2])
        print len(df)
        return df
    else:
        return None

#DIR = '/mnt/nb254_data/src/data_SO/data_for_ML/'
#db_name = 'askubuntu'
db_name = 'stackoverflow'
DIR = '/mnt/nb254_data/exp/'
subdir = 'exp_' + db_name
if not os.path.exists(DIR + subdir):
        os.makedirs(DIR + subdir)
DIR = DIR + subdir + '/'

df = extractFeaturesML(db_name, DIR)
df.to_csv(DIR + 'normMLa.csv', index=False)
filename = 'normMLa.csv'
df = pd.read_csv(DIR + filename)
print df['TEMP_CL'].mean()
df = resample(df, 'TEMP_CL', 'downsample')
print df['TEMP_CL'].mean() #only 1s and 0s
run_ML(df)
