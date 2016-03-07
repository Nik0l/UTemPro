__author__ = 'nb254'

import numpy as np
import pandas as pd
from sklearn import cluster
from sklearn.cluster import KMeans
from sklearn.neighbors import NearestNeighbors
from sklearn.neighbors import kneighbors_graph

import ClusteringPrediction as cp
import ClusteringSaveResults as csr
import DataPreprocessing as dp
import FeatureSelector as ftrs
import Questions as question
from Visualization import ClusteringPlot as plot

from matplotlib import pyplot as plt
import seaborn as sns
from sklearn.preprocessing import normalize
from sklearn.decomposition import PCA

def clusterData(data, clust, results, to_plot):
    plot_sample_size = 6000
    if clust['clustering_type'] == 'kmeans':
        #TODO kmeans works well even on 2.000.000 questions
        kmeans = KMeans(init='k-means++', n_clusters=clust['n_clusters'], n_init=10)
        kmeans.fit(data)
        clust['centers'] = kmeans.cluster_centers_
        results['cluster_labels'] = kmeans.labels_
        if to_plot:
            plot.PlotData(data, kmeans, plot_sample_size, clust['exp'])

    if clust['clustering_type'] == 'spectral':
        spectral = cluster.SpectralClustering(n_clusters=clust['n_clusters'],
                                          eigen_solver='arpack',
                                          affinity="nearest_neighbors")
        spectral.fit(data)
        plot.PlotData(data, spectral, plot_sample_size, clust['exp'])

    if clust['clustering_type'] == 'birch':
        birch = cluster.Birch(n_clusters=results['n_clusters'])
        birch.fit(data)
        results['cluster_labels'] = birch.labels_
        print 'number of entries clustered', len(results['cluster_labels'])
        plot.PlotData(data, birch, plot_sample_size, clust['exp'])

    if clust['clustering_type'] == 'dbscan':
        dbscan = cluster.DBSCAN(eps=.2)
        dbscan.fit(data)
        results['cluster_labels'] = dbscan.labels_
        plot.PlotData(data, dbscan, plot_sample_size, clust['exp'])

    if clust['clustering_type'] == 'affinity_propagation':
        affinity_propagation = cluster.AffinityPropagation(damping=.9, preference=-200)
        affinity_propagation.fit(data)
        plot.PlotData(data, affinity_propagation, plot_sample_size, clust['exp'])

    if clust['clustering_type'] == 'ward':
        # connectivity matrix for structured Ward
        connectivity = kneighbors_graph(data, n_neighbors=10, include_self=False)
        # make connectivity symmetric
        connectivity = 0.5 * (connectivity + connectivity.T)
        ward = cluster.AgglomerativeClustering(n_clusters=clust['n_clusters'], linkage='ward',
                                           connectivity=connectivity)
        ward.fit(data)
        results['cluster_labels'] = ward.labels_
        plot.PlotData(data, ward, plot_sample_size, clust['exp'])

    if clust['clustering_type'] == 'average_linkage':
        # connectivity matrix for structured Ward
        connectivity = kneighbors_graph(data, n_neighbors=10, include_self=False)
        # make connectivity symmetric
        connectivity = 0.5 * (connectivity + connectivity.T)
        average_linkage = cluster.AgglomerativeClustering(
        linkage="average", affinity="cityblock", n_clusters=clust['n_clusters'],
        connectivity=connectivity)
        average_linkage.fit(data)
        results['cluster_labels'] = average_linkage.labels_
        plot.PlotData(data, average_linkage, plot_sample_size, clust['exp'])
    df = csr.clustDfFromRes(results)
    stats = csr.clusterResults(df, clust)
    return df, stats
'''
def firstExperiment(sampled_data, features_all, clust, results, filename_clusters, filename_stats):
    clust['exp']= 1
    for feature in features_all:
        df, stats = runClustering(sampled_data[['SecondsToAcceptedAnswer'] + [feature]], clust, results)
        csr.to_csv(stats, filename_stats)
        df.to_csv(filename_clusters)
        clust['exp'] = clust['exp'] + 1

def secondExperiment(sampled_data, features_variations, clust, results, filename_clusters):
    clust['exp'] = 50
    for features in features_variations:
        df, stats = runClustering(sampled_data[features], clust, results)
        csr.to_csv(stats, filename_stats)
        df.to_csv(filename_clusters)
        clust['exp'] = clust['exp'] + 1

def thirdExperiment(sampled_data, clust, results, filename_clusters, filename_stats):
    features = ftrs.setAllFeatures()
    df, stats = runClustering(sampled_data[features], clust, results)
    csr.to_csv(stats, filename_stats)
    df.to_csv(filename_clusters)
'''
def initClust(exp, n_clusters, sample_size, features_to_use, clustering_type):
    clust = dict(
        exp=exp,
        n_samples=sample_size,
        features=features_to_use,
        n_features=len(features_to_use)+1,
        n_clusters=n_clusters,
        clustering_type=clustering_type,
        centers=np.empty([n_clusters, 2]), #centroids
    )
    return clust

def printQues():
    QuestionIds = [4, 6, 7]
    ques = question.getQuestionsbyId(QuestionIds)
    print '%'*100
    for que in ques:
        print que

def getQuestions(labels, df):
    print df.head()
    df1 = df[df['Cluster'].isin(labels)]
    #df1 = df1.drop('Unnamed: 0', 1)
    return df1

def selectLabels(df, criteria=4):
    #if df['mean_time'] < 5:
        #labels = [0,1,2]
    labels = [0, 1, 2, 3, 4]
    return labels

def mergeTitle(df1, filename2):
    #df1 = pd.read_csv(filename1)
    df4 = pd.read_csv(filename2)
    file_name = 'merged_new.csv'
    result = pd.merge(df1, df4, on='PostId')
    result.to_csv(file_name)

def matchClusters(dir_c, df, dfs, dfc, filename_out):
    labels = selectLabels(dfs)
    # for all labels of interest
    dfq = getQuestions(labels, dfc)
    qlist = dfq['PostId'].tolist()
    print qlist
    df1 = df[df['PostId'].isin(qlist)]
    df1.to_csv(filename_out)
    #for each labels
    for label in labels:
        dfq = getQuestions([label], dfc)
        qlist = dfq['PostId'].tolist()
        dfl = df[df['PostId'].isin(qlist)]
        dfl.to_csv(dir_c + str(label) + '_' + filename_out)
    #dfq.to_csv(filename_out)

def clustering(clust, filenames, saved=False):
    #mergeTitle(df, filename2)
    if saved:
        stats = pd.read_csv(filenames['stats'])
        clusters = pd.read_csv(filenames['clusters'])
    else:
        data, results = dp.getDataForClustering(filenames, clust)
        #TODO divide data into training and testing datasets
        clust['n_samples'] = len(data)
        print 'total instances:', clust['n_samples']
        testing_num = int(clust['n_samples'] * 0.2)
        #testing_num = 1924500
        results['quest_id'] = results['quest_id'][testing_num:clust['n_samples']]
        results['time_row'] = results['time_row'][testing_num:clust['n_samples']]
        print 'testing instances: ', str(testing_num) # 385981
        print 'Started clustering...'
        #clusters, stats = clusterData(data, clust, results, False)
        clusters, stats = clusterData(data[testing_num:clust['n_samples']], clust, results, False)
        print 'Saving the clustering results...'
        csr.to_csv1(stats, filenames['stats'])
        clusters.to_csv(filenames['clusters'])
    return stats, clusters

def clusteringA(clustMeta, dir_c, filenames):
   #os.mkdir(dir_c, 0777)

   stats, dfn = clustering(clustMeta, filenames)
   # match clusters to data
   print 'Opening a file with the data on the questions'
   df = pd.read_csv(filenames['input'])
   print 'Matching the data on the questions with the clusters'
   matchClusters(dir_c, df, stats, dfn, filenames['out'])

   #TODO prediction using clusters n
   dfpca = pd.read_csv(dir_c + 'pca.csv', header=None)
   #print dfpca.shape
   #print dfpca[0:12]
   test = dfpca[0:50]
   print len(test)
   n_neighbors = 3
   dfstats = pd.read_csv(filenames['stats'])
   #dfstats = dfstats[dfstats['questions'].str.contains("questions") == False]
   #print dfstats
   df = pd.read_csv(filenames['clusters'])
   neigh = NearestNeighbors(n_neighbors=n_neighbors)
   neigh.fit(dfstats[['x','y']])
   #print test
   closest = neigh.kneighbors(test) #TODO: dimension mismatching
   data = cp.calcAccuracy(dfstats, closest, df, n_neighbors, test)
   csr.to_csv(data, dir_c + 'predictions.csv')
   for datum in data:
      print datum

def principal_component_analysis(x_train):

    # Extract the variable to be predicted
    y_train = x_train["var"]
    x_train = x_train.drop(labels="var", axis=1)
    classes = np.sort(np.unique(y_train))
    labels = ["class1", "class2"]

    # Run PCA
    x_train_normalized = normalize(x_train)
    pca = PCA(n_components=2)
    x_train_projected = pca.fit_transform(x_train_normalized)

    # Visualize
    fig = plt.figure(figsize=(10, 7))
    ax = fig.add_subplot(1, 1, 1)
    colors = [(0.0, 0.63, 0.69), 'black']
    markers = ["o", "D"]
    for class_ix, marker, color, label in zip(
            classes, markers, colors, labels):
        ax.scatter(x_train_projected[np.where(y_train == class_ix), 0],
                   x_train_projected[np.where(y_train == class_ix), 1],
                   marker=marker, color=color, edgecolor='whitesmoke',
                   linewidth='1', alpha=0.9, label=label)
        ax.legend(loc='best')
    plt.title(
        "Scatter plot of the training data examples projected on the "
        "2 first principal components")
    plt.xlabel("Principal axis 1 - Explains %.1f %% of the variance" % (
        pca.explained_variance_ratio_[0] * 100.0))
    plt.ylabel("Principal axis 2 - Explains %.1f %% of the variance" % (
        pca.explained_variance_ratio_[1] * 100.0))
    plt.show()

    plt.savefig("pca.pdf", format='pdf')
    plt.savefig("pca.png", format='png')
###############################################################################

#x_train = pd.read_csv(DIR + "train.csv", index_col=0, sep=',')
#principal_component_analysis(x_train)

DIR = '/mnt/nb254_data/exp/exp_askubuntu/'
dir_c = '/mnt/nb254_data/exp/exp_askubuntu/clustering/'

filenames = {'input': DIR + "dataMLClust.csv",
            'clustering': dir_c + 'data_file_for_clustering.csv',
            'stats': dir_c + 'stats.csv',
            'clusters': dir_c + 'clustering.csv',
            'pca': dir_c + 'pca.csv',
            'out': 'questions.csv'}

#clusteringA(dir_c, filenames)
clustering_types = ['kmeans', 'spectral', 'birch', 'dbscan', 'affinity_propagation', 'ward', 'average_linkage']
clust = initClust(exp=1319,
                  n_clusters=50,
                  sample_size=1929906,
                  features_to_use=ftrs.setFeaturesToUseAll() + ['PostId'] + ['SecondsToAcceptedAnswer'],
                  clustering_type=clustering_types[0])

#data, results = dp.getDataForClustering(filenames, clust)

clusteringA(clust, dir_c, filenames)
