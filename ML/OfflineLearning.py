__author__ = 'root'

import numpy as np
import pandas as pd
import statsmodels.api as sm
import matplotlib.pyplot as plt
from patsy import dmatrices
from sklearn.cross_validation import cross_val_score
from sklearn.linear_model import LogisticRegression
from sklearn.cross_validation import train_test_split
from sklearn import metrics
from sklearn.cross_validation import cross_val_score
from sklearn import svm
from sklearn import tree
from sklearn import preprocessing
from sklearn.ensemble import RandomForestClassifier, AdaBoostClassifier
from sklearn.neighbors import KNeighborsClassifier
from nolearn.dbn import DBN
import time
import pickle
import FeatureSelector as cf

def FiveFoldValid(clf, X1, y1):
   # evaluate the model using 5-fold cross-validation
   scores1 = cross_val_score(clf, X1, y1, scoring='accuracy', cv=5)
   print scores1
   print scores1.mean()

def getPredictedCorrectly(predicted, original):
    for prediction in predicted:
        if original['TEMP_CL']==prediction:
            print 'predicted correctly'
        else:
            print 'predicted not correctly'

def dataNormalise(data):
    min_max_scaler = preprocessing.MinMaxScaler()
    data['x_train'] = min_max_scaler.fit_transform(data['x_train'])
    data['x_test'] = min_max_scaler.fit_transform(data['x_test'])
    data['y_test'] = min_max_scaler.fit_transform(data['y_test'])
    return data

def DrawTree(clfDT):
   with open("StackOverflow.dot", 'w') as f:
      f = tree.export_graphviz(clfDT, out_file=f)

def getOfflineClassifiers(param):
    batch_classifiers = {
        'SVM': svm.SVC(gamma=0.001, C=10., class_weight="auto"),
        #'Random Forest': RandomForestClassifier(max_depth=5, n_estimators=10, max_features=1),
        'LR': LogisticRegression(class_weight="auto"),
        'KNN': KNeighborsClassifier(n_neighbors=3),
        'DT': tree.DecisionTreeClassifier(),
        'DBN': DBN([param, 300, 2],learn_rates = 0.3,learn_rate_decays = 0.9,epochs = 2,verbose = 1),
    }
    return batch_classifiers

def initClsStats(classifiers):
    cls_stats = {}
    for cls_name in classifiers:
        stats = {'n_train': 0,
                 'n_test': 0,
                 'n_features': 0.0,
                 't0': time.time(),
                 'accuracy': 0.0,
                 'conf_matrix': [[0,0],[0,0]],
                 'precision':[0,0],
                 'recall': [0,0],
                 'fscore': [0,0],
                 'support': [0,0],
                 'training_time': 0.0,
                 'testing_time': 0.0,
                 'another_time': 0.0,
                 'n_train_pos': 0,
                 'accuracy_history': [(0, 0)],
                 'runtime_history': [(0, 0)]}
        cls_stats[cls_name] = stats
    return cls_stats

def runOfflineML(y, X, classifiers, savemodel=False):
    X_train, X_test, y_train, y_test = train_test_split(X, y.astype("int0"), test_size=0.20, random_state=0)
    data = dict(
            x_train=X_train,
            x_test=X_test,
            y_train=y_train,
            y_test=y_test
        )
    cls_stats = initClsStats(classifiers)
    for cls_name, cls in classifiers.items():
        cls_stats[cls_name]['n_train'] = data['x_train'].shape[0]
        cls_stats[cls_name]['n_test'] = data['x_test'].shape[0]
        cls_stats[cls_name]['n_features'] = data['x_train'].shape[1]
        tick = time.time()
        if cls_name == 'DBN':
            data = dataNormalise(data)
            clf = DBN([data['x_train'].shape[1], 300, 2],learn_rates = 0.3,learn_rate_decays = 0.9,epochs = 10,verbose = 1)
            clf.fit(data['x_train'], data['y_train'])
        else:
            clf = classifiers[cls_name].fit(data['x_train'], data['y_train'])
        if savemodel:
            pickle.dump(clf, open(cls_name + '.dat', 'w'))
            clf = pickle.load(open(cls_name + '.dat', 'r'))
        cls_stats[cls_name]['training_time'] += time.time() - tick
        # check the accuracy on the training set
        tick = time.time()
        predicted = clf.predict(data['x_test'])
        cls_stats[cls_name]['testing_time'] += time.time() - tick
        acc = metrics.accuracy_score(data['y_test'], predicted)
        cls_stats[cls_name]['accuracy'] = acc
        print cls_name, "accuracy is: " + str(acc)
        #auc = metrics.roc_auc_score(data['y_test'], probs[:, 1])
        conf_matrix = metrics.confusion_matrix(data['y_test'], predicted)
        cls_stats[cls_name]['conf_matrix'] = conf_matrix
        #print conf_matrix
        precision, recall, fscore, support = metrics.precision_recall_fscore_support(data['y_test'], predicted)
        cls_stats[cls_name]['precision'] = precision
        cls_stats[cls_name]['recall'] = recall
        cls_stats[cls_name]['fscore'] = fscore
        cls_stats[cls_name]['support'] = support
    return cls_stats
