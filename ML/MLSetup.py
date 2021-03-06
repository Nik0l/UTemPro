__author__ = 'nb254'

import numpy as np
import pandas as pd
import MachineLearning as ml
import time
import OfflineLearning as offlineML
import OnlineLearning as onlineML
import MLPlot as pt

feature_predict = ['TEMP_CL']

def runExperiment(df, feature_sets, times, batch_size):
    tick = time.time()
    outputs = []
    for feature_set in feature_sets:
        classifiers = dict(
            online=onlineML.getOnlineClassifiers(),
            offline=offlineML.getOfflineClassifiers(df.shape[1])
        )
        y, X = ml.getDataForML(df, features=feature_set, feature_predict=feature_predict, sampling=False)
        n_features = X.shape[1]
        print 'total features ', n_features
        print 'total samples ', X.shape[0]
        times['preparing_time'] += time.time() - tick

        cls_stats = offlineML.runOfflineML(y, X, classifiers['online'])
        output = [cls_stats, classifiers['online'], feature_set, '5fold']
        outputs.append(output)

        # online
        cls_stats = onlineML.runOnlineML(y, X, classifiers['online'], batch_size=batch_size)
        output = [cls_stats, classifiers['online'], feature_set, str(batch_size) + 'batch']
        outputs.append(output)
        #cls_name, cls in classifiers.items():

        cls_stats = offlineML.runOfflineML(y, X, classifiers['offline'])
        output = [cls_stats, classifiers['offline'], feature_set, '5fold']
        outputs.append(output)

        cls_stats = onlineML.runOnlineML(y, X, classifiers['offline'], batch_size=batch_size)
        output = [cls_stats, classifiers['offline'], feature_set, str(batch_size) + 'batch']
        outputs.append(output)
        #saveClassificationResults(DIR + 'results/accuracy_ML.csv', output)
        #theanoTest(y,X)
        pt.plotEverything(cls_stats, times, len(X))

    return outputs

def runExpNtimes(df, feature_sets, repetitions):
    times = {'preparing_time':0.0,
             'training_time': 0.0,
             'testing_time': 0.0,
             'another_time': 0.0}
    results = []
    batch_size = 5000
    for index in xrange(0, repetitions):
        outputs = runExperiment(df, feature_sets, times, batch_size)
        results.append(makeResults(outputs))
    table = []
    for result in results:
        for res in result:
            table.append(res)
    dfres = pd.DataFrame(table, columns=['Algorithm', 'Learning_Type', 'Features', 'Accuracy', 'Training_Time', 'Testing_Time'])
    return dfres

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

def makeFirstTable(dfres):
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
    return dfresa

def makeSecondTable(dfres):
    dfresb = dfres[dfres['Learning_Type']=='5fold']
    dfresb = dfresb.groupby(['Algorithm', 'Features'])
    dfresb = dfresb['Accuracy'].agg({'Accuracy_m': np.mean})
    dfresb = dfresb.reset_index()
    dfresb['Accuracy_m'] = 100 * np.round(dfresb['Accuracy_m'], 3)
    return dfresb

