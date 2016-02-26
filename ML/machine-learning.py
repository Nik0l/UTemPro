# prediction using ML algorithms
# LR, DT, SVM, DBN, k-NN
__author__ = 'nb254'
import numpy as np
import pandas as pd
from patsy import dmatrices
import time
from Features import features
import FeatureSelector as cf
import OfflineLearning as offlineML
import OnlineLearning as onlineML
import csv
from sklearn.cross_validation import train_test_split
import DeepLearning as dl
from sklearn import metrics
import NLPFeaturesAdvanced as nlp
from sklearn.feature_selection import SelectKBest
from sklearn.feature_selection import chi2
from sklearn.ensemble import RandomForestClassifier
import MLPlot as pt
feature_predict = ['TEMP_CL']

DIR = '/mnt/nb254_data/learning/data/'

def getDataForML(df, features, feature_predict, sampling, sample_size=100000):
   if sampling:
        rows = np.random.choice(df.index.values, sample_size)
        df = df.ix[rows]
   # create dataframes
   print 'size of the file', df.shape[0]
   print 'size of the file1', df.shape[1]
   y, X = dmatrices(cf.selectFeatures(features, feature_predict), df, return_type="dataframe")
   print y
   # flatten y into a 1-D array
   y = np.ravel(y)
   # balance of the classes
   print 'mean value of the predicted variable', y.mean()
   return y, X

def saveClassificationResults(filename, output):
    cls_stats = output[0]
    classifiers = output[1]
    feature_set = output[2]
    myfile = open(filename, 'a')
    wr = csv.writer(myfile)
    for cls_name, cls in classifiers.items():
        row = [cls_name,
               feature_set,
               cls_stats[cls_name]['n_train'],
               cls_stats[cls_name]['n_test'],
               cls_stats[cls_name]['n_features'],
               cls_stats[cls_name]['t0'],
               cls_stats[cls_name]['accuracy'],
               cls_stats[cls_name]['conf_matrix'],
               cls_stats[cls_name]['precision'],
               cls_stats[cls_name]['recall'],
               cls_stats[cls_name]['fscore'],
               cls_stats[cls_name]['support'],
               cls_stats[cls_name]['training_time'],
               cls_stats[cls_name]['testing_time'],
               cls_stats[cls_name]['another_time'],
               [cls_stats[cls_name]['n_train_pos']],
               [cls_stats[cls_name]['accuracy_history']],
               [cls_stats[cls_name]['runtime_history']]]
        wr.writerow(row)

def theanoTest(y,X):
    X_train, X_test, y_train, y_test = train_test_split(X, y.astype("int0"), test_size=0.20, random_state=0)
    data = dict(
            x_train=X_train,
            x_test=X_test,
            y_train=y_train,
            y_test=y_test
        )
    model = dl.DeepLearningModel()
    X_train = np.array(X_train)
    y_train = np.array(y_train)
    X_test = np.array(X_test)
    y_test = np.array(y_test)

    model.fit(X_train, y_train, nb_epoch=2, batch_size=32)
    objective_score = model.evaluate(X_test, y_test, batch_size=32)
    predicted = model.predict(X_test)
    for pred in predicted:
        if pred > 0.4:
            print pred
    #acc = metrics.accuracy_score(y_test, predicted)
    #print objective_score
    classes = model.predict_classes(X_test, batch_size=32)
    proba = model.predict_proba(X_test, batch_size=32)

def runExperiment(df, feature_sets, times, batch_size=5000):
    tick = time.time()
    outputs = []
    for feature_set in feature_sets:
        y, X = getDataForML(df, features=feature_set, feature_predict=feature_predict, sampling=False)
        n_features = X.shape[1]
        print 'total features ', n_features
        print 'total samples ', X.shape[0]
        #y1, X1 = getDataForML(df, sampling=True)
        times['preparing_time'] += time.time() - tick

        #classifiers = offlineML.getOfflineClassifiers(n_features)
        classifiers = onlineML.getOnlineClassifiers()
        cls_stats = offlineML.runOfflineML(y, X, classifiers)
        output = [cls_stats, classifiers, feature_set, '5fold']
        outputs.append(output)

        cls_stats = onlineML.runOnlineML(y, X, classifiers, batch_size=batch_size)
        output = [cls_stats, classifiers, feature_set, '5000batch']
        outputs.append(output)
        #saveClassificationResults(DIR + 'results/accuracy_ML.csv', output)
        #print cls_name, cls_stats[cls_name]
        #times1 = {'total_norm_time': 0.0, 'preparing_time':0.0, 'another_time':0.0}

        #classifiers = onlineML.getOnlineClassifiers()
        classifiers = offlineML.getOfflineClassifiers(n_features)
        cls_stats = offlineML.runOfflineML(y, X, classifiers)
        output = [cls_stats, classifiers, feature_set, '5fold']
        outputs.append(output)

        cls_stats = onlineML.runOnlineML(y, X, classifiers, batch_size=batch_size)
        output = [cls_stats, classifiers, feature_set, '5000batch']
        outputs.append(output)
        #cls_stats = onlineML.runOnlineML(y, X, classifiers, batch_size=10)
        #output = [cls_stats, classifiers, feature_set]
        #saveClassificationResults(DIR + 'results/accuracy_ML.csv', output)
        #outputs.append(output)
        #onlineML.printStats(times1, cls_stats)
        #theanoTest(y,X)
    return outputs

def makeResults(outputs):
    results = []
    for output in outputs:
        cls_stats = output[0]
        classifiers = output[1]
        feature_set = output[2]
        learning_type = output[3]
        for cls_name, cls in classifiers.items():
            results.append([cls_name, learning_type, feature_set, cls_stats[cls_name]['accuracy'],
                            cls_stats[cls_name]['training_time'], cls_stats[cls_name]['testing_time']])
    return results

def runExpNtimes(df, feature_sets, repetitions):
    times = {'preparing_time':0.0, 'training_time': 0.0, 'testing_time': 0.0, 'another_time': 0.0}
    results = []
    for index in xrange(0, repetitions):
        outputs = runExperiment(df, feature_sets, times)
        results.append(makeResults(outputs))
    table = []
    for result in results:
        for res in result:
            table.append(res)
    dfres = pd.DataFrame(table, columns=['Algorithm', 'Learning_Type', 'Features', 'Accuracy', 'Training_Time', 'Testing_Time'])
    return dfres

DIRR = '/mnt/nb254_data/src/data/data_online_learning/'
DIR = '/mnt/nb254_data/src/data_SO/data_for_ML/'
filename = 'normMLa.csv'
#filename = 'normML1.csv'
#filename = 'normtoyML.csv'
#df = pd.read_csv(DIR + filename)
#df1 = df[2:1000]
#df1.to_csv(DIR + 'testing.csv', index=False)
df = pd.read_csv(DIR + 'testing.csv')
feature_sets = ['RL', 'NOTAGS', 'NOSTEMP', 'all']
dfres = runExpNtimes(df, feature_sets, repetitions=10)
dfres = dfres.sort(['Learning_Type', 'Algorithm', 'Features'], ascending=False)

dfresa = dfres[dfres['Features']=='all']
dfresa = dfresa.groupby(['Learning_Type', 'Algorithm', 'Features'])
#print dfres
dfres1 = dfresa['Accuracy'].agg({'Accuracy_m': np.mean, 'Accuracy_std': np.std})
dfres2 = dfresa['Training_Time'].agg({'Training_Time_m': np.mean})
dfres3 = dfresa['Testing_Time'].agg({'Testing_Time_m': np.mean})
dfresa = pd.concat([dfres1, dfres2, dfres3], axis=1)
dfresa = dfresa.reset_index()
dfresa['Accuracy_m'] = 100 * np.round(dfresa['Accuracy_m'], 3)
dfresa['Accuracy_std'] = np.round(dfresa['Accuracy_std'], 2)
dfresa['Training_Time_m'] = np.round(dfresa['Training_Time_m'], 1)
dfresa['Testing_Time_m'] = np.round(dfresa['Testing_Time_m'], 3)
#print dfresa
dfresa.to_csv('results1.csv')

dfresb = dfres[dfres['Learning_Type']=='5fold']
dfresb = dfresb.groupby(['Algorithm', 'Features'])
dfresb = dfresb['Accuracy'].agg({'Accuracy_m': np.mean})
dfresb = dfresb.reset_index()
dfresb['Accuracy_m'] = 100 * np.round(dfresb['Accuracy_m'], 3)
dfresb.to_csv('results2.csv', index=False)
print dfresb

'''
DIR1 = '/mnt/nb254_data/src/data_SO/NLP/'
filename1 = 'post_data_text.csv'
#filename1 = 'testing.csv'
#filename = 'testNLP.csv'
dataset = pd.read_csv(DIR1 + filename1)

#testset = trainset.ix[90000:100000]
#dataset = dataset.ix[0:1999]

df = nlp.preprocessing(DIR1, dataset)
y, X = getDataForML(df, features='NLP', feature_predict=feature_predict, sampling=False)
n_features_to_leave=100
X_new = SelectKBest(chi2, k=n_features_to_leave).fit_transform(X, y)
#print X_new.shape
classifiers = {'Random Forest': RandomForestClassifier(n_estimators = 100),}
cls_stats = offlineML.runOfflineML(y, X_new, classifiers)
saveClassificationResults('NLP_accuracy_ML.csv', cls_stats, classifiers)
'''
#pt.plotEverything(cls_stats, times, len(X))
