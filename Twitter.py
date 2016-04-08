import pandas as pd
from collections import Counter

import pandas as pd
from sklearn import metrics
import xgboost as xgb
import matplotlib.pyplot as plt

def modelfit(alg, data, predictors, useTrainCV=True, cv_folds=5, early_stopping_rounds=50):
    '''
    a variation of:
    http://www.analyticsvidhya.com/blog/2016/03/complete-guide-parameter-tuning-xgboost-with-codes-python/
    '''
    if useTrainCV:
        xgb_param = alg.get_xgb_params()
        xgtrain = xgb.DMatrix(data['x_train'][predictors], label=data['y_train'])
        cvresult = xgb.cv(xgb_param,
                          xgtrain,
                          num_boost_round=alg.get_params()['n_estimators'],
                          nfold=cv_folds,
                          metrics='auc',
                          early_stopping_rounds=early_stopping_rounds)
        alg.set_params(n_estimators=cvresult.shape[0])
    #Fit the algorithm on the data
    alg.fit(data['x_train'][predictors], data['y_train'], eval_metric='auc')
    #Predict training set:
    dtrain_predictions = alg.predict(data['x_train'][predictors])
    dtrain_predprob = alg.predict_proba(data['x_train'][predictors])[:,1]
    #Print model report:
    print ("\nModel Report")
    print ("Accuracy : %.4g" % metrics.accuracy_score(data['y_train'].values, dtrain_predictions))
    print ("AUC Score (Train): %f" % metrics.roc_auc_score(data['y_train'], dtrain_predprob))
    feat_imp = pd.Series(alg.booster().get_fscore()).sort_values(ascending=False)
    feat_imp[0:20].plot(kind='bar', title='Feature Importances')
    plt.ylabel('Feature Importance Score')
    plt.show()
    return alg

def openFriendDf(path):
	df = pd.read_csv(path, delimiter=r"\s+", header=None)
	df.columns = ['UserIdFrom', 'UserIdTo']
	#df.columns = ['UserId', 'UserIdTo','Timestamp','Type']
	return df

def openActivityDf(path):
	df = pd.read_csv(path, delimiter=r"\s+", header=None)
	df.columns = ['UserId', 'UserIdTo','Timestamp','Type']
	df['TweetId'] = df.index
	df['Timestamp'] = pd.to_datetime(df['Timestamp'], unit='s')
	#print df['Timestamp']
	print df.shape
	return df

def extractTempFeatures(df):
	temp_f = []
	for index, row in df.iterrows():
		t = row['Timestamp']
		temp_f.append([t.day, t.hour, t.minute, t.second])
	temp_df = pd.DataFrame(temp_f, columns=['day', 'hour', 'minute', 'second'])
	temp_df = pd.concat([df['TweetId'], temp_df], axis=1)
	print temp_df
	return temp_df
	
def extractNumTweets(df):
	freqs_sent = Counter(df['UserId'])
	freqs_received = Counter(df['UserIdTo'])
	#print freqs
	fr_s = pd.DataFrame(freqs_sent.items(), columns=['UserId', 'Tweets_Sent'])
	fr_r = pd.DataFrame(freqs_received.items(), columns=['UserId', 'Tweets_Received'])
	#print fr_s
	#print fr_r
	result = pd.merge(fr_s, fr_r, on='UserId', how='outer')
	result = result.fillna(0)
	#print result
	#print result.shape
	return result

def extractNumRe(df, a):
	freqs_sent = Counter(df['UserId'])
	freqs_received = Counter(df['UserIdTo'])
	#print freqs
	fr_s = pd.DataFrame(freqs_sent.items(), columns=['UserId', a[0]])
	fr_r = pd.DataFrame(freqs_received.items(), columns=['UserId', a[1]])
	#print fr_s
	#print fr_r
	result = pd.merge(fr_s, fr_r, on='UserId', how='outer')
	result = result.fillna(0)
	#print result
	#print result.shape
	return result

def extractNumFriends(df):
    	freqs_sent = Counter(df['UserIdFrom'])
	freqs_received = Counter(df['UserIdTo'])
	#print freqs
	fr_s = pd.DataFrame(freqs_sent.items(), columns=['UserId', 'Following'])
	fr_r = pd.DataFrame(freqs_received.items(), columns=['UserId', 'Followers'])
	#print fr_s
	#print fr_r
	result = pd.merge(fr_s, fr_r, on='UserId', how='outer')
	result = result.fillna(0)
	#print result
	#print result.shape
	return result

def tweetsAggregate(df):
	dfa = df[df['Type']=='RE']
	a = ['Tweets_Re', 'Tweets_Red']
	num_re = extractNumRe(dfa, a)
	dfb = df[df['Type']=='RT']
	b = ['Tweets_Rt', 'Tweets_Rtd']
	num_rt = extractNumRe(dfb, b)
	dfc = df[df['Type']=='MT']
	c = ['Tweets_Mt', 'Tweets_Mtd']
	num_mt = extractNumRe(dfc, c)
	result = pd.merge(num_re, num_rt, on='UserId', how='outer')
	result = pd.merge(result, num_mt, on='UserId', how='outer')
	result = result.fillna(0)
	#print result
	return result

def makeLabel(df):
        label = []
	for index, row in df.iterrows():
		if row['Type'] == 'RE':
			label.append(1)
		else:
			label.append(0)
	labdf = pd.DataFrame(label, columns=['isRetweet'])
	labdf = pd.concat([df['TweetId'], labdf], axis=1)
	return labdf

def extractFeatures(df1, df2):
	#calculate interaction graph features
	temp_df = extractTempFeatures(df1)
	tweets = tweetsAggregate(df1)
	num_mes = extractNumTweets(df1)
	interact = pd.merge(tweets, num_mes, on='UserId', how='outer')
	print interact
	#add temporal features
	df1 = pd.merge(df1, temp_df, on='TweetId', how='left')
	#calculate friendship graph features
	friendship = extractNumFriends(df2)
	print friendship
	#add interaction graph features
	df1 = pd.merge(df1, interact, on='UserId', how='left')
	#print interact
	#add friendship graph features
	result = pd.merge(df1, friendship, on='UserId', how='left')
	result = result.fillna(0)
	return result

def getDataforML():
	filename_activity = 'higgs-activity_time.txt'
	filename_social = 'higgs-social_network.edgelist'
	#open activity graph
	df1 = openActivityDf(filename_activity)
	#open a friendship graph
	df2 = openFriendDf(filename_social)
	#make a label
	label = makeLabel(df1)
	print label.mean()
	#extract features, merge them
	result = extractFeatures(df1, df2)
	#add label
	result = pd.merge(result, label, on='TweetId', how='outer')
	#print result

	y = result['isRetweet']
	X = result.drop('isRetweet', 1)
	X = X.drop('Type', 1)
	X = X.drop('Timestamp', 1)

	print X

	ratio = y.value_counts() / float(y.size)
	print ('ratio of y: ', ratio)

	data = dict(
        	x_train=X[0:500000],
        	x_test=X[500001:563068],
        	y_train=y[0:500000],
        	y_test=y[500001:563068]
    	)

	print data['y_test'].mean()

	data['y_test'].to_csv('test_real.csv')
	return data

def predict(data):
	xgbm = xgb.XGBClassifier(
   		learning_rate=0.02,
   		n_estimators=1500,
   		max_depth=6,
   		min_child_weight=1,
   		gamma=0,
   		subsample=0.9,
   		colsample_bytree=0.85,
  	 	objective= 'binary:logistic',
   		nthread=4,
   		scale_pos_weight=1,
   		seed=27)

	features = [x for x in data['x_train'].columns if x not in ['ID']]
	alg = modelfit(xgbm, data, features)
	dtrain_predprob = alg.predict_proba(data['x_test'][features])[:, 1]

	df = pd.DataFrame(dtrain_predprob, columns=['TARGET'])
	print (df['TARGET'].mean())
	df_res = pd.concat([data['y_test'].astype(int), df], axis=1)
	df_res.to_csv('results.csv', index=False)

def mergeFiles():
	filename1 = 'test_real.csv'
	filename2 = 'results.csv'

	df1 = pd.read_csv(filename1)
	df1.columns = ['TweetId', 'isRetweet']
	df2 = pd.read_csv(filename2)
	df2 = df2[0:len(df1)]
	df2 = df2.drop('isRetweet',1)

	print df1.head()
	print df2.head()
	print df1.shape
	print df2.shape

	df = pd.concat([df1, df2],  axis=1)
	print df.head()
	print df.shape

	df = df.sort(['TARGET'], ascending=0)

	df.to_csv('final.csv')
#data = getDataforML()
#predict(data)
#mergeFiles()

filename_activity = 'higgs-activity_time.txt'
df = pd.read_csv(filename_activity, delimiter=r"\s+", header=None)
df.columns = ['UserId', 'UserIdTo','Timestamp','Type']
df['TweetId'] = df.index
df = df.sort(['Timestamp', 'Type'], ascending=[1,0])
df = df.reset_index(drop=True)
print df
#TODO: remove dublicated rows where RE, RT, or MT at the same time
#freqs = Counter(df['Timestamp'])
#repeated = []
#for freq in freqs:
	#if freqs[freq] > 1:
		#repeated.append(freq)
#print len(repeated)

#df_dropped = df[df['Timestamp'] != repeated]
#print df_dropped
list_del = []
for index, row in df.iterrows():
	if index > 0 and df.ix['Timestamp'][index] == df.ix['Timestamp'][prev_index] and df.ix['Type'] <> 'RE':
		list_del.append(index)
		prev_index = index
df = df.drop(df.index[list_del])
			#print 'need to drop'
print df
