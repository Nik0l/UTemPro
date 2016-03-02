
__author__ = 'nb254'
# makeplot.py
import matplotlib.pyplot as plt
import matplotlib.pylab as pylab
# import pandas as pd
import Features as features
import Variables as var
def NumAnswers(data):
    MAX_ANSWERS = 99
    plt.figure(1, figsize=(12, 8))
    plt.bar(data['Answers'][0:MAX_ANSWERS], data['Count'][0:MAX_ANSWERS], log=True, linewidth=None, edgecolor=None)
    plt.title('Number of answers and questions')
    plt.xlabel('Number of answers')
    plt.ylabel('Number of questions')
    plt.savefig(var.DIR_DATA + 'Plots/num_of_posts_per_user.png')
    plt.show()

def PostOwners(posts, MODE, FEATURE):
    if MODE == 'PERUSER':
        plt.figure(1, figsize=(12, 8))
        plt.hist(posts[FEATURE], bins=range(1, 2000, 2), log=True, linewidth=1.00, color="#cccccc")
        plt.xlabel("Number of Posts")
        plt.ylabel("Number of Users")
        plt.yticks([1, 10, 100, 1000, 10000, 100000])
        plt.title("Users' activity")
        plt.savefig(var.DIR_DATA + 'Plots/posts_per_user_activity.png')
        plt.show()
    elif MODE == 'RANK':
        plt.figure(2, figsize=(12, 8))
        plt.plot(range(1, len(posts[FEATURE]) + 1), posts[FEATURE])
        plt.yscale("log")
        plt.yticks([0.1, 1, 10, 100, 1000])
        plt.xlabel("User's rank")
        plt.ylabel("Number of Posts")
        plt.title("Rank of User's activity")
        plt.savefig(var.DIR_DATA + 'Plots/user_activity_rank.png')
        plt.draw()
        plt.show()


def QuestPerUser(posts_stats):
    fig = plt.figure(1, figsize=(12, 8))
    plt.bar(range(len(posts_stats)), posts_stats.values(), log=True, linewidth=1.00, edgecolor='grey')
    plt.xlabel("Questions per user")
    plt.ylabel("Number of users")
    plt.title("Distribution of Questions per User")
    plt.savefig(var.DIR_DATA + 'Plots/ques_per_user.png')
    plt.show()


def QAbyTime(data):
    fig = plt.figure(1, figsize=(12, 8))
    #ax2 = fig.add_subplot(2, 1, 2) #bottom plot
    plt.xticks(range(len(data['answers'])), data['labels'], rotation='vertical', size='x-small')
    p1 = plt.bar(range(len(data['questions'])), data['questions'], color='#67A9CF', label="number of questions",
                 align="center")
    p2 = plt.bar(range(len(data['answers'])), data['answers'], color='#EF8A62', label="number of answers",
                 bottom=data['questions'], align="center")
    plt.legend((p1[0], p2[0]), ("number of questions", "number of answers"), loc=(0.05, 0.65))
    plt.xlabel("Date")
    plt.ylabel("Number of New Questions and Answers")
    plt.title("Evolution of New Question and Answer Counts by Month")
    plt.savefig(var.DIR_DATA + 'Plots/q_a_by_month.png')
    plt.show()


def PlotDistrFeature(data, FEATURE):
    fig = plt.figure(1, figsize=(12, 8))
    for feature in features.FEATURE_LIST:
        if feature['name'] == FEATURE:
            title = feature['title']
            plt.loglog(data[FEATURE], data['USERS_NUM'], linestyle='None', marker='.', nonposx='clip', color='#2D2C37')
            plt.title("Distribution of " + title)
            plt.xlabel(title)
            plt.ylabel("Number of Users")
            plt.savefig(var.DIR_DATA + 'Plots/distribution_' + title + '.png')
            plt.show()


def Plot2Features(data, FEATURE_X, FEATURE_Y):
    #TODO aggregate data for dublicated response times
    fig = plt.figure(1, figsize=(12, 8))
    featurex_in_alist = False
    featurey_in_alist = False
    for feature in features.FEATURE_LIST:
        if feature['name'] == FEATURE_Y:
            featurey_in_alist = True
            y_from = feature['x_from']
            y_to = feature['x_to']
            plt.ylabel(feature['title'])
    for feature in features.FEATURE_LIST:
        if feature['name'] == FEATURE_X:
            featurex_in_alist = True
            x_from = feature['x_from']
            x_to = feature['x_to']
            plt.xlabel(feature['title'])
    if featurex_in_alist == True and featurey_in_alist == True:
        #plt.title("Distribution of User Reputation Points")
        #plt.scatter(data[FEATURE_X], data[FEATURE_Y])
        plt.plot(data[FEATURE_X], data[FEATURE_Y], 'ro')
        plt.axis([x_from, x_to, y_from, y_to])
        plt.savefig(var.DIR_DATA + 'Plots/' + FEATURE_X + '_' + FEATURE_Y + '.png')
        plt.show()
    else:
        print "The features are not in the list, can't plot it"


def AnswerTimes(data, TIME):
    ws = [1.0 / data['questions'] for x in data['mins']]

    if TIME == 'MINUTE':
        plt.figure(1, figsize=(12, 8))
        plt.hist(data['mins'], bins=range(0, 24 * 60, 1), weights=ws, cumulative=True,
                 color='#cccccc')  # ,histtype='step')
        plt.yticks([x / 10.0 for x in range(0, 11)])
        plt.xmax = 24 * 60
        plt.xticks(range(0, 24 * 60, 120))
        plt.xlim(0, 24 * 60)
        plt.draw()
        plt.xlabel("Minutes elapsed after question is posted")
        plt.ylabel("Percentage of all questions with accepted answer")
        plt.title("Cumulative histogram: time elapsed \nbefore questions receive accepted answers (first day)")
        plt.axvline(x=1 * 60, color='#aaaaaa', label="1 hour")
        plt.axvline(x=2 * 60, color='#aaaaaa', label="2 hours")
        plt.axvline(x=6 * 60, color='#aaaaaa', label="6 hours")
        plt.axvline(x=12 * 60, color='#aaaaaa', label="12 hours")
        plt.savefig(var.DIR_DATA + 'Plots/minutes_passed_before_q_answered.png')
        plt.show()
    elif TIME == 'HOUR':
        plt.figure(2, figsize=(12, 8))
        plt.hist(data['hours'], bins=range(0, 24 * 30, 1), weights=ws, cumulative=True,
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
        plt.savefig(var.DIR_DATA + 'Plots/hours_passed_before_q_answered.png')
        plt.show()
    elif TIME == 'DAY':
        plt.figure(3, figsize=(12, 8))
        plt.hist(data['days'], bins=range(0, 365, 1), weights=ws, cumulative=True, color='#cccccc')  # ,histtype='step')
        plt.yticks([x / 10.0 for x in range(0, 11)])
        plt.xmax = 365
        plt.xticks(range(0, 365, 30))
        plt.xlim(0, 365)
        plt.draw()
        plt.xlabel("Days elapsed after question is posted")
        plt.ylabel("Percentage of all questions with accepted answer")
        plt.title("Cumulative histogram: \n time elapsed before questions receive accepted answers (1 year)")
        plt.savefig(var.DIR_DATA + 'Plots/days_passed_before_q_answered.png')
        plt.show()

#
def PostsStats(dataplot):
    MAX_POSTS = 500
    STEPS = 5
    plt.figure(1, figsize=(12, 8))
    p1 = plt.bar(range(MAX_POSTS), dataplot[0]['number_of_posts'][:MAX_POSTS], color='#1f78b4', linewidth=0, width=0.4)
    p3 = plt.bar(range(MAX_POSTS), dataplot[2]['number_of_posts'][:MAX_POSTS], color='red', linewidth=0, width=0.4)
    p2 = plt.bar(range(MAX_POSTS), dataplot[1]['number_of_posts'][:MAX_POSTS], color='darkgreen', linewidth=0,
                 width=0.4)

    ticks = [x * MAX_POSTS / STEPS for x in range(0, STEPS + 1)]
    plt.legend((p1[0], p2[0], p3[0]), ('Posts', 'Questions', 'Answers'))
    plt.title('Histogram: Thread Lengths for posts, qestions and answers')
    plt.xlabel('Thread Length')
    #plt.xlabel('Answers')
    plt.ylabel('Number of Posts / Questions / Answers')
    plt.savefig(var.DIR_DATA + 'Plots/q_a_posts_length.png')
    plt.show()


def TitleStats(dataplot):
    MAX_POSTS = 30
    STEPS = 5
    plt.figure(1, figsize=(12, 8))
    p1 = plt.bar(range(MAX_POSTS), dataplot['number_of_posts'][:MAX_POSTS], color='#1f78b4', linewidth=0, width=0.4)

    ticks = [x * MAX_POSTS / STEPS for x in range(0, STEPS + 1)]
    plt.title('Histogram: Question title lengths')
    plt.xlabel('Title Length')
    #plt.xlabel('Answers')
    plt.ylabel('Number of questions')
    plt.savefig(var.DIR_DATA + 'Plots/title_length.png')
    plt.show()


def StatsBySite(data):
    plt.figure(1, figsize=(12, 8))
    p1 = plt.bar(range(len(data['users'])), data['users'], color='#1f78b4', linewidth=0, width=0.4)
    plt.title('Histogram: Number of users per website')
    plt.xlabel('Websites')
    #plt.xlabel('Answers')
    plt.ylabel('Number of users')
    plt.savefig(var.DIR_DATA + 'Plots/websites_stats.png')
    plt.show()


def Plot2SemiLogs(data_x, data_y):
    plt.figure(1, figsize=(12, 8))
    plt.semilogx(data_x, data_y)
    plt.title('Rank-ordered users vs. answers')
    plt.ylabel("Percent of all answers")
    plt.xlabel("Number of users rank-ordered by reputation")
    plt.show()


def PlotTags(data, MODE):
    fig = plt.figure(1, figsize=(12, 8))
    ax = fig.add_subplot(1, 1, 1)
    if MODE == 'RANK':
        #calculate how many bars there will be
        N = len(data['ys'])
        #generate list of numbers from 0 to N
        ind = range(N)
        plt.bar(range(0, (len(data['ys']))), data['ys'], log=True, linewidth=1.00, edgecolor='blue')
        plt.title('Histogram of Tag Frequency')
        plt.ylabel('Number of times used')
        plt.xlabel('rank ordering of unique tags')
        plt.savefig(var.DIR_DATA + 'Plots/allTags.png')
        plt.show()

    elif MODE == '50TAGS':
        #calculate how many bars there will be
        N = len(data['ys_short'])
        #generate list of numbers from 0 to N
        ind = range(N)
        #set ticks
        ax.set_xticks(ind)
        #plt.bar(range(0,len(ys)),ys, log=True, linewidth=1.00, edgecolor='blue')
        plt.bar(ind, data['ys_short'], linewidth=0, color='gray')
        #yticks(range(0, 100,000))
        plt.title('Histogram of Tag Frequency (Top 50)')
        plt.ylabel('Number of times used')
        plt.xlabel('tag name')
        #labels for the ticks on the x asis, one label for each bar
        group_labels = data['labels_short']
        ax.set_xticklabels(group_labels)
        #auto rotate the x axis labels
        fig.autofmt_xdate()
        plt.savefig(var.DIR_DATA + 'Plots/top50tags.png')
        plt.show()


def TagSpeed(data):
    fig = plt.figure(1, figsize=(16, 12))
    ax = fig.add_subplot(1, 1, 1)
    plt.bar(range(1, len(data['ys']) + 1), data['ys'])
    #plt.bar(labels[0:10],ys[0:10], linewidth=None, edgecolor=None)

    #calculate how many bars there will be
    N = len(data['ys'])
    #generate list of numbers from 0 to N
    ind = range(N)
    #set ticks
    #ax.set_xticks(ind)
    plt.xticks(range(1, len(data['ys']) + 1), data['labels'], rotation='vertical', size='x-small')

    #plt.bar(ind , ys,linewidth=0, color='gray')
    #plt.bar(range(0,(len(ys))), ys, log=True, linewidth=1.00, edgecolor='blue')
    # want labels/dates to be on x axis
    #nf,bins,patches = plt.hist(speed, bins= ind, linewidth=1.00, log = True, cumulative=False,color='#66C2A5',    label='label')
    #plt.hist(speed, bins= ind, linewidth=1.00, log = False, cumulative=False, histtype='bar', color='#66C2A5', label='label')
    plt.xlabel("Tag Name")
    plt.ylabel("Answer Time")
    plt.title("Median Answer Time for Tag")
    plt.savefig(var.DIR_DATA + 'Plots/questionTimeforTag.png')
    plt.show()


def TagSpeed2(data):
    plt.figure(1, figsize=(12, 12))
    plt.title("Tags as indicators of fast (median < 10min) and slow (median > 1 day) answers to questions")
    plt.boxplot(data['ys'], sym='', vert=1, notch=1)
    plt.ylabel('answer time (seconds)')
    plt.xlabel('question tag name')
    plt.xticks(range(1, len(data['ys']) + 1), data['labels'], rotation='vertical', size='x-small')
    plt.yscale('log')

    #lines at 10min 1hr 1d 1wk
    plt.axhline(y=60 * 60 * 24 * 7, color='#7FCDBB', linestyle=':', label="1 week")
    plt.axhline(y=60 * 60 * 24, color='#2c7fb8', linestyle='dashed', label="1 day")
    plt.axhline(y=60 * 60, color='#2c7fb8', linestyle='-.', label="1 hr")
    plt.axhline(y=60 * 10, color='#2c7fb8', linestyle=':', label="10 min")
    plt.axvline(x=25.5, color='#808080', linestyle="-")

    plt.legend(loc='upper left')

    plt.subplots_adjust(bottom=0.30)
    plt.savefig(var.DIR_DATA + 'Plots/tagspeed2.png')
    plt.show()


def UsersBehaviour(data):
    fig = plt.figure(1, figsize=(12, 12))
    print data['nothing']
    print data['questions_only']
    plt.barh(range(8),
             [data['nothing'], data['questions_only'], data['answers_only'], data['votes_only'], data['qanda'],
              data['qandv'], data['vanda'], data['all']], align='center', color='#cccccc')
    plt.yticks(range(8),
               ['Does nothing', 'Asks', 'Answers', 'Votes', 'Asks & answers', 'Asks and votes', 'Answers and votes',
                'Asks, answers & votes'])
    plt.xlabel("Percentage")
    plt.title("User Behaviour")
    plt.savefig(var.DIR_DATA + 'Plots/users_behaviour.png')
    plt.show()


def NumofViews(data):
    colors = ['#addd8e', '#78c679', '#41ab5d', '#238443', '#005a32']  #run the query: # answers to questions
    #hack to get 0 point
    plt.bone()
    plt.figure(1, figsize=(8, 4))

    plots = []
    # alternative: draw a bar chart of first 100 values
    #+[sum(ys[249:])]
    for i in range(len(data)):
        plots.append(plt.loglog(data[i]['allxs'], data[i]['allys'], color=colors[i], linestyle='None', marker='.'))
        label = 'mode: %d' % data[i]['modex']
        plt.annotate(label, (data[i]['modex'], data[i]['modey']), xycoords='data', xytext=(5, 1),
                     textcoords='offset   points', arrowprops=dict(arrowstyle="->"))
    plt.title('Number of Views per Question (log-log)')
    plt.ylabel('Number of Questions')
    plt.xlabel('Number of Views')
    leg = plt.legend((plots[0][0], plots[1][0], plots[2][0], plots[3][0], plots[4][0]), (
        'Qs posted in last week', 'Qs posted in last month', 'Qs posted in last 6 months', 'Qs posted in last year',
        'All Questions'))
    for t in leg.get_texts():
        t.set_fontsize('x-small')  # the legend text fontsize
    plt.savefig(var.DIR_DATA + 'Plots/num_of_views.png')
    plt.ylim(ymin=0.8)
    plt.show()


def QuestsLength(data):
    fig = plt.figure(1, figsize=(12, 12))
    ax = fig.add_subplot(1, 1, 1)  #top plot

    #plot # of answers on x axis, title length on y axis
    colors = ['#B2182B', '#41ab5d']  #,'#238443','#0571B0']
    #plt.scatter(answers, titles, label='title lengths', color='#B2182B') #titles red, questions green
    #plt.scatter(answers, questions,label='question lengths', color='#41ab5d')

    #plt.loglog(answers,titles,label='title lengths', color='#B2182B',linestyle='None',marker='.')
    ax.hexbin(data['answers'], data['questions'], bins='log', yscale='log', gridsize=20,
              label='question lengths')  #color='#41ab5d',linestyle='None',marker='.')
    ax.axis([0, 13, 20, 140])
    #ax.set_yscale('log')
    #ax.set_xscale('log')
    #plt.legend(loc= (0.05, 0.85))
    #plt.legend(('title length','question post length'), loc= (0.05, 0.85))
    #plt.legend()

    ## legend
    # pylab.legend(('title length', 'question post length'), shadow = True, loc = (0.01, 0.55))
    # ltext = ["title length","question post length"]
    # pylab.setp(ltext[0], fontsize = 20, color = 'b')
    # pylab.setp(ltext[1], fontsize = 20, color = 'g')

    plt.xlabel("Number of Answers")
    plt.ylabel("Question length")
    plt.title("Comparison of Question length to Number of Answers Received")

    plt.savefig(var.DIR_DATA + 'Plots/questionLength.png')
    plt.show()
