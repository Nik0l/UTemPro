__author__ = 'root'

import matplotlib.pyplot as plt
import numpy as np

def PlotData(data, algorithm, sample_size, exp):
    h = 0.02
    val = setValues(data)
    #print type(data)
    #print data
    xx, yy = np.meshgrid(np.arange(val['x_min'], val['x_max'], h), np.arange(val['y_min'], val['y_max'], h))
    #print_minmax1(xx, yy)
    # Obtain labels for each point in mesh. Use last trained model.
    #Z = algorithm.predict(np.c_[xx.ravel(), yy.ravel()])
    if hasattr(algorithm, 'labels_'):
        Z = algorithm.labels_.astype(np.int)
    else:
        Z = algorithm.predict(np.c_[xx.ravel(), yy.ravel()])
    #print Z
    #print 'Z size', len(Z)
    #print 'xx size', len(xx)
    #print 'xx shape', xx.shape
    # Put the result into a colour plot
    #Z = Z.reshape(xx.shape)
    #print Z
    plt.figure(1)
    plt.clf()
    #plt.imshow(Z, interpolation='nearest',
           #extent=(xx.min(), xx.max(), yy.min(), yy.max()),
           #cmap=plt.cm.Paired,
           #aspect='auto', origin='lower')
    total_num_questions = len(data)
    #sample_size = total_num_questions
    B = np.random.choice(total_num_questions, sample_size, replace=False)
    data_sample = data[B,:]
    colors = np.array([x for x in 'brcmykbgrcmykbgrcmykbgrcmyk'])
    colors = np.hstack([colors] * 20)
    #plt.plot(reduced_data[:, 0], reduced_data[:, 1], 'k.', markersize=1)
    plt.plot(data_sample[:, 0], data_sample[:, 1], 'k.', markersize=1)
    plt.scatter(data_sample[:, 0], data_sample[:, 1], color=colors[Z].tolist(), s=1)
    # Plot the centroids as a white X
    if hasattr(algorithm, 'cluster_centers_'):
        centroids = algorithm.cluster_centers_
        plt.scatter(centroids[:, 0], centroids[:, 1],
            marker='x', s=169, linewidths=3,
            color='w', zorder=10)
    plt.title('K-means clustering on the dataset (PCA-reduced data)\n'
          'Centroids are marked with white cross')
    plt.xlim(val['x_min'], val['x_max'])
    plt.ylim(val['y_min'], val['y_max'])
    plt.xticks(())
    plt.yticks(())
    plt.savefig('clustering_' + str(exp) + '.png')
    #plt.show()

def PlotTime(df_new):
    ws = [1.0 / len(df_new) for x in df_new['ResponseTimeSec']]
    plt.figure(2, figsize=(12, 8))
    plt.hist(df_new['ResponseTimeSec'], bins=range(0, 24 * 30, 1), weights=ws, cumulative=True,
                 color='#cccccc')  # ,histtype='step')
    plt.yticks([x / 10.0 for x in range(0, 11)])
    plt.xmax = 24 * 30
    plt.xticks(range(0, 24 * 30, 24 * 7))
    plt.xlim(0, 24 * 30)
    plt.draw()
    plt.xlabel("Hours elapsed after question is posted")
    plt.ylabel("Percentage of all questions with accepted answer")
    plt.title("Cumulative histogram: \n time elapsed before questions receive accepted answers (1 month)")
    plt.axvline(x=1 * 24, color='#aaaaaa', label="1 day")
    plt.axvline(x=7 * 24, color='#aaaaaa', label="1 week")
    plt.axvline(x=14 * 24, color='#aaaaaa', label="2 weeks")
    plt.axvline(x=21 * 24, color='#aaaaaa', label="3 weeks")
    #plt.savefig(var.DIR_DATA + 'Plots/hours_passed_before_q_answered.png')
    plt.show()

def setValues(data):
    # Plot the decision boundary. For that, we will assign a color to each
    delta = 1
    val = {'x_min': 0, 'x_max': 0, 'y_min': 0, 'y_max': 0}
    val['x_min'] = data[:, 0].min() - delta
    val['x_max'] = data[:, 0].max() + delta
    val['y_min'] = data[:, 1].min() - delta
    val['y_max'] = data[:, 1].max() + delta
    #print_minmax(val)
    return val

def print_minmax(val):
    print 'x_min', val['x_min']
    print 'y_min', val['y_min']
    print 'x_max', val['x_max']
    print 'y_max', val['y_max']

def print_minmax1(xx, yy):
    print 'xx_min', xx.min()
    print 'yy_min', yy.min()
    print 'xx_max', xx.max()
    print 'yy_max', yy.max()
