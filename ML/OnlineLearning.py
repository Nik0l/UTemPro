from __future__ import print_function
__author__ = 'root'

import time

import numpy as np
from sklearn.linear_model import SGDClassifier
from sklearn.linear_model import PassiveAggressiveClassifier
from sklearn.linear_model import Perceptron
from sklearn.naive_bayes import MultinomialNB
import MLPlot as pt
import ReutersDataset as rds
import FeatureSelector as cf
import pandas as pd
from patsy import dmatrices
from sklearn.cross_validation import train_test_split
from Features import features
import DataPreprocessing as dpp
import ClusteringSaveResults as csr
from sklearn import preprocessing
from nolearn.dbn import DBN
import csv as csv
###############################################################################
# Main
###############################################################################
def iter_sample(X, y, size):
    i = 0
    while ((i+1)*size < len(X)):
       #print (df.iloc[i*size:(i+1)*size])
       i = i + 1
       yield X.iloc[i*size:(i+1)*size], y[i*size:(i+1)*size]

def progress(cls_name, stats, test_stats):
    """Report progress information, return a string."""
    duration = time.time() - stats['t0']
    s = "%20s classifier : \t" % cls_name
    s += "%(n_train)6d train ques (%(n_train_pos)6d positive) " % stats
    s += "%(n_test)6d test ques (%(n_test_pos)6d positive) " % test_stats
    s += "accuracy: %(accuracy).3f " % stats
    s += "in %.2fs (%5d ques/s)" % (duration, stats['n_train'] / duration)
    return s

def initClsStats(classifiers):
    cls_stats = {}
    for cls_name in classifiers:
        stats = {'n_train': 0, 'n_test': 0, 'n_features': 0.0, 't0': time.time(),
                 'accuracy': 0.0, 'conf_matrix': [[0,0],[0,0]], 'precision':[0,0],
                 'recall': [0,0], 'fscore': [0,0], 'support': [0,0],
                 'training_time': 0.0, 'testing_time': 0.0, 'another_time': 0.0,
                 'n_train_pos': 0, 'accuracy_history': [(0, 0)], 'runtime_history': [(0, 0)]}
        cls_stats[cls_name] = stats

    return cls_stats

# Create the vectorizer and limit the number of features to a reasonable
# maximum
def getOnlineClassifiers():
    classifiers = {
        'SGD': SGDClassifier(),
        'Perceptron': Perceptron(),
        #'NB Multinomial': MultinomialNB(alpha=0.01),
        'Passive-Aggressive': PassiveAggressiveClassifier(),
    }
    return classifiers

def normaliseDataToFile(file_name_input, file_name_output, times):
    df = pd.read_csv(file_name_input)
    df = df.drop(['LOCATION', 'TIME_ZONE', 'COUNTRY', 'LOCATION.1', 'ADMIN_REGION', 'TimeAsked', 'TAG_SPECIFICITY'], 1)
    print (df.head())
    #TODO normalising large files takes time so better save them in advance
    tick = time.time()
    print ('Normalising the data... ')
    df = df.dropna() # drop NaN values
    min_max_scaler = preprocessing.MinMaxScaler()
    df_norm = min_max_scaler.fit_transform(df)
    header = ",".join(list(df.columns.values))
    #df_norm = (df - df.mean()) / (df.max() - df.min())
    #df_norm = df_norm + 1
    #print ('max', df_norm.max())
    #print ('min', df_norm.min())
    #df_norm.to_csv(file_name_output)
    np.savetxt(file_name_output, df_norm, header=header, delimiter=",")
    times['total_norm_time'] += time.time() - tick
    print ('normalisation time:', times['total_norm_time'])
    return df_norm

def normaliseDataToFile1(file_name_input, file_name_output, times):
    df = pd.read_csv(file_name_input)
    df = df.drop(['LOCATION', 'TIME_ZONE', 'COUNTRY', 'LOCATION.1', 'ADMIN_REGION', 'TimeAsked',
                  'TimeAnswered', 'Tags_x', 'Tags_y', 'TAG_SPECIFICITY'], 1)
    #print (df['NUM_SUBS_ANS'])
    #for item in df['NUM_SUBS_ANS']:
        #print (item)
    #df.to_csv(file_name_output)
    #TODO normalising large files takes time so better save them in advance
    tick = time.time()
    print ('Normalising the data... ')
    #df = df[np.isfinite(df['NUM_SUBS_ANS'])]
    df = df.dropna() # drop NaN values
    #df.to_csv(file_name_output)
    min_max_scaler = preprocessing.MinMaxScaler()
    df_norm = min_max_scaler.fit_transform(df)
    header = ",".join(list(df.columns.values))
    #df_norm = (df - df.mean()) / (df.max() - df.min())
    #df_norm = df_norm + 1
    #print ('max', df_norm.max())
    #print ('min', df_norm.min())
    #df_norm.to_csv(file_name_output)
    np.savetxt(file_name_output, df_norm, header=header, delimiter=",")
    times['total_norm_time'] += time.time() - tick
    print ('normalisation time:', times['total_norm_time'])
    return df_norm

def accStats(tick, cls, cls_stats, cls_name, data):
    # accumulate test accuracy stats
    cls_stats[cls_name]['n_features'] = data['x_train'].shape[1]
    cls_stats[cls_name]['training_time'] += time.time() - tick
    cls_stats[cls_name]['n_train'] += data['x_train'].shape[0]
    cls_stats[cls_name]['n_test'] += data['x_test'].shape[0]
    cls_stats[cls_name]['n_train_pos'] += sum(data['y_train'])
    tick = time.time()
    cls_stats[cls_name]['accuracy'] = cls.score(data['x_test'], data['y_test'])
    cls_stats[cls_name]['testing_time'] += time.time() - tick
    acc_history = (cls_stats[cls_name]['accuracy'],
                    cls_stats[cls_name]['n_train'])
    cls_stats[cls_name]['accuracy_history'].append(acc_history)
    run_history = (cls_stats[cls_name]['accuracy'],
                    cls_stats[cls_name]['training_time'] + cls_stats[cls_name]['testing_time'])
    cls_stats[cls_name]['runtime_history'].append(run_history)

def testStats(y_test):
    test_stats = {'n_test': 0, 'n_test_pos': 0}
    test_stats['n_test'] += len(y_test)
    test_stats['n_test_pos'] += sum(y_test)
    print("Test set is %d questions (%d positive)" % (len(y_test), sum(y_test)))
    return test_stats

def dataNormalise(data):
    min_max_scaler = preprocessing.MinMaxScaler()
    data['x_train'] = min_max_scaler.fit_transform(data['x_train'])
    data['x_test'] = min_max_scaler.fit_transform(data['x_test'])
    data['y_test'] = min_max_scaler.fit_transform(data['y_test'])
    return data

def runMinibatch(minibatch, cls_stats, classifiers, all_classes, losses1, losses2, x1, x2):

    for i, (df_small, y_small) in enumerate(minibatch):
        tick = time.time()
        #TODO calcualte features for df_small
        X_train, X_test, y_train, y_test = train_test_split(df_small, y_small.astype("int0"), test_size=0.20, random_state=0)
        data = dict(
            x_train=X_train,
            x_test=X_test,
            y_train=y_train,
            y_test=y_test
        )
        for cls_name, cls in classifiers.items():
            cls_stats[cls_name]['another_time'] += time.time() - tick
            tick = time.time()
            # update estimator with examples in the current mini-batch
            #cls.partial_fit(data['x_train'], data['y_train'], classes=all_classes)
            #print ("total number of samples for update: ", data['x_train'].shape[0])
            #for i in range(0, len(data['x_train'])):
                #a1 = data['x_train'].iloc[i]
                #a2 = data['x_train'].iloc[i+1]
                #b1 = data['y_train'][i]
                #b2 = data['y_train'][i+1]
                #a = [a1.as_matrix(columns=None), a2.as_matrix(columns=None)]
                #b = [b1, b2]
                #print (a)
                #print (b)
                #clf = classifiers[cls_name].fit(a, b)
                #a = np.dot(cls.coef_ , data['x_train'].iloc[i+1].as_matrix(columns=None))
                #print (a)
            #print ("y for training: ", data['y_train'].shape[0])
            if cls_name == 'DBN':
                data = dataNormalise(data)
                clf = DBN([data['x_train'].shape[1], 300, 2],learn_rates = 0.3,learn_rate_decays = 0.9,epochs = 10,verbose = 1)
                clf.fit(data['x_train'], data['y_train'])
            else:
                #print (data['x_train'])
                #print (data['y_train'])
                clf = classifiers[cls_name].fit(data['x_train'], data['y_train'])
                #clf = classifiers[cls_name].partial_fit(data['x_train'], data['y_train'], classes=[0,1])
            #print ("coefficients")
            #print (cls.coef_)
            #print ("test point")
            #print (data['x_test'])
            #print (data['x_test'].iloc[1].as_matrix(columns=None))
            #print ("dot product x*w")
            #print (cls.coef_ * data['x_test'].iloc[1].as_matrix(columns=None) )
            #print ("dot product1 x*w")
            # cls.coef_ is the vector with weights of coefficients
            #print ("total number of samples for testing: ", data['x_test'].shape[0])
            #a1 = np.dot(cls.coef_ , data['x_test'].iloc[0].as_matrix(columns=None))
            #a2 = np.dot(cls.coef_ , data['x_test'].iloc[1].as_matrix(columns=None))
            #x1.append(data['x_test'].iloc[0].as_matrix(columns=None))
            #x2.append(data['x_test'].iloc[1].as_matrix(columns=None))
            '''
            if cls_name == 'SGD':
                losses1['SGD'].append(a1)
                losses2['SGD'].append(a2)
            elif cls_name == 'Perceptron':
                losses1['Perceptron'].append(a1)
                losses2['Perceptron'].append(a2)
            elif cls_name == 'NB Multinomial':
                losses1['NB'].append(a1)
                losses2['NB'].append(a2)
            elif cls_name == 'Passive-Aggressive':
                losses1['PA'].append(a1)
                losses2['PA'].append(a2)
            '''
            #print (a)
            # accumulate statistics
            #accStats(tick, cls, cls_stats, cls_name, data)
            accStats(tick, clf, cls_stats, cls_name, data)
    #print (losses)
    #csr.to_csv(losses1['SGD'], 'lossesSGDx1.csv')
    #csr.to_csv(losses2['SGD'], 'lossesSGDx2.csv')
    #csr.to_csv(losses1['Perceptron'], 'lossesPerceptronx1.csv')
    #csr.to_csv(losses2['Perceptron'], 'lossesPerceptronx2.csv')
    #csr.to_csv(losses1['NB'], 'lossesNBx1.csv')
    #csr.to_csv(losses2['NB'], 'lossesNBx2.csv')
    #csr.to_csv(losses1['PA'], 'lossesPAx1.csv')
    #csr.to_csv(losses2['PA'], 'lossesPAx2.csv')
    #csr.to_csv(x1, 'x1.csv')
    #csr.to_csv(x1, 'x2.csv')

    for cls_name, cls in classifiers.items():
        stats = []
        for iter, point in enumerate(cls_stats[cls_name]['accuracy_history']):
            stats.append([cls_name, iter, point[0], point[1]])
            #print ([cls_name, iter, batch_size, point[0], point[1]])
        csr.to_csv(stats, 'online_learning_accuracy.csv')

# binary classification between the "response time" class and all the others.
def runOnlineML(y, X, classifiers, batch_size):
    all_classes = np.array([0, 1])
    x1 = []
    x2 = []
    losses1 = dict(
        SGD=[],
        Perceptron=[],
        NB=[],
        PA=[],
    )
    losses2 = dict(
        SGD=[],
        Perceptron=[],
        NB=[],
        PA=[],
    )
    cls_stats = initClsStats(classifiers)
    minibatch = iter_sample(X, y, batch_size)
    #TODO check whether it's correct or not - first batch
    for cls_name, cls in classifiers.items():
        cls_stats[cls_name]['n_train'] += batch_size * 0.8
        cls_stats[cls_name]['n_test'] += batch_size * 0.2
    runMinibatch(minibatch, cls_stats, classifiers, all_classes, losses1, losses2, x1 ,x2)
    return cls_stats

def printStats(times, cls_stats):
    print ('preparing time: ', times['preparing_time'])
    for point in cls_stats:
        print (point, ' training time: ', cls_stats[point]['training_time'])
        print (point, ' testing time: ', cls_stats[point]['testing_time'])
        print (point, ' another time: ', cls_stats[point]['another_time'])

#TODO times
#times = {'total_norm_time': 0.0}
#normaliseDataToFile('test_ML.csv', 'normML.csv', times)
#file_name_input = '/mnt/nb254_data/src/data/data_online_learning/test_ML.csv'
#file_name_input = '/mnt/nb254_data/src/data_SO/data_for_ML/merged.csv'
#file_name_output = '/mnt/nb254_data/src/data_SO/data_for_ML/normML1.csv'
#normaliseDataToFile1(file_name_input, file_name_output, times)
###############################################################################
# Plot results
###############################################################################
#pt.plotEverything(cls_stats, times, len(X))
