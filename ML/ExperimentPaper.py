import MLSetup as ml
import OfflineLearning as offlineML
import OnlineLearning as onlineML
import pandas as pd
import MergeFeatures as mf
import os
import FeatureExtractor as extractor
# the path to the file with data

def extractFeaturesML(db_name, DIR):
    key_users = ['UserId']
    key_posts = ['PostId']
    # extracts all features
    extractor.extractForML(db_name, DIR)
    dfML = mf.mergeAll(DIR, key_users, key_posts, mf.FeaturePredict)
    dfML.to_csv(DIR + 'dataML.csv', index=False)
    dfnorm = mf.normalize(dfML)
    return dfnorm

def run_ML(df):
    feature_sets = ['RL', 'NOTAGS', 'NOSTEMP', 'all']

    classifiers = dict(
        online=onlineML.getOnlineClassifiers(),
        offline=offlineML.getOfflineClassifiers(df.shape[1])
    )

    dfres = ml.runExpNtimes(df, feature_sets, classifiers, repetitions=2)
    dfres = dfres.sort(['Learning_Type', 'Algorithm', 'Features'], ascending=False)
    dfresa = ml.makeFirstTable(dfres)
    os.makedirs(DIR + 'results/')
    dfresa.to_csv(DIR + 'results/results_algorithms.csv')
    dfresb = ml.makeSecondTable(dfres)
    dfresb.to_csv(DIR + 'results/results_features.csv', index=False)
    print dfresb

#DIR = '/mnt/nb254_data/src/data_SO/data_for_ML/'
#db_name = 'beer'
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
run_ML(df)
