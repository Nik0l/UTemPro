__author__ = 'nb254'
import numpy as np
import pandas as pd
from patsy import dmatrices
import FeatureSelector as cf

def getDataForML(df, features, feature_predict, sampling, sample_size=100000):
   if sampling:
        rows = np.random.choice(df.index.values, sample_size)
        df = df.ix[rows]
   # create dataframes
   print 'samples', df.shape[0]
   print 'feature dimension ', df.shape[1]
   y, X = dmatrices(cf.selectFeatures(features, feature_predict), df, return_type="dataframe")
   print y
   # flatten y into a 1-D array
   y = np.ravel(y)
   # balance of the classes
   print 'mean value of the predicted variable', y.mean()
   return y, X
