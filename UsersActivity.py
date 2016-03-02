__author__ = 'nb254'
from collections import Counter
import csv, time
import pandas as pd


POSTID_INDEX      = 0
USERID_INDEX      = 1
TIME_POSTED_INDEX = 2
POST_TYPE_INDEX   = 3

def SaveStatToCSV(file_name, data, header):
    with open(file_name, 'wb') as myfile:
        wr = csv.writer(myfile)
        wr.writerow(header)
        wr.writerows(data)
    return


def UniqueUsers(data):
   unique_users = list(Counter(data['UserId']))
   #print unique_users
   return unique_users

def makePosts(data):
    posts = []
    for time_stamp in data['TimePosted']:
        #print time_stamp
        sq = time_stamp.replace("T", " ")
        sq = sq[0:19]
        time_posted  = time.strptime(sq, "%Y-%m-%d %H:%M:%S")
        year_posted  = time.strftime("%Y", time_posted)
        month_posted = time.strftime("%m", time_posted)
        day_posted   = time.strftime("%d", time_posted)
        hour_posted  = time.strftime("%H", time_posted)
        min_posted   = time.strftime("%M", time_posted)
        posts.append([year_posted, month_posted, day_posted, hour_posted, min_posted])
    df = pd.DataFrame(posts, columns=['year', 'month', 'day', 'hour', 'min'])
    result = pd.concat([data, df], axis=1)
    return result

def UsersActivity(users, posts):
   activities = []
   daytime_q   = [0]*24
   daytime_a   = [0]*24
   monthtime_q = [0]*12
   monthtime_a = [0]*12
   index = 0
   num = 0
   print posts.head()
   #print "users: ", len(users)
   for user in users:
      for index in xrange(0, len(posts)):
         hour_posted  = posts['hour'][index]
         month_posted = posts['month'][index]
         if posts['UserId'][index] == user:# if the post belongs to a user
            if posts['PostType'][index] == 1:# question
               daytime_q[int(hour_posted)]      = daytime_q[int(hour_posted)] + 1
               monthtime_q[int(month_posted)-1] = monthtime_q[int(month_posted)-1] + 1
            elif posts['PostType'][index] == 2:# answer
               daytime_a[int(hour_posted)]      = daytime_a[int(hour_posted)] + 1
               monthtime_a[int(month_posted)-1] = monthtime_a[int(month_posted)-1] + 1
      activities.append([user, monthtime_q, daytime_q, monthtime_a, daytime_a])
      print ('user:', user)
      num = num + 1
      print ('number: ', num)
      #print daytime
      daytime_q   = [0]*24
      daytime_a   = [0]*24
      monthtime_q = [0]*12
      monthtime_a = [0]*12
   return activities

def usersActivityFast(posts):

   posts = posts.sort(['UserId'], ascending=True)
   posts = posts[posts['UserId'] != -1]
   posts = posts[['UserId','PostType', 'year', 'month', 'day', 'hour', 'min']]
   posts = posts.reset_index()
   activities = []
   act_time = dict(
       daytime_q   = [0]*24,
       daytime_a   = [0]*24,
       monthtime_q = [0]*12,
       monthtime_a = [0]*12,
   )
   num = 0
   #print posts.head()
   for index in xrange(0, len(posts)-1):
       updateActivity(posts, index, act_time)
       if posts['UserId'][index] != posts['UserId'][index+1]:
           activities.append([posts['UserId'][index], act_time['daytime_q'],
                              act_time['daytime_a'], act_time['monthtime_q'], act_time['monthtime_a']])
           resetActivity(act_time)
           #print 'new user:', posts['UserId'][index+1]
       else:
           updateActivity(posts, index, act_time)
           #print ('same user:', posts['UserId'][index+1])
       num = num + 1
       #print 'number: ', num
   df_act = pd.DataFrame(activities, columns =['UserId','Q_HOUR', 'A_HOUR', 'Q_MONTH', 'A_MONTH'])
   return df_act

def updateActivity(posts, index, act_time):
    hour_posted  = posts['hour'][index]
    month_posted = posts['month'][index]
    if posts['PostType'][index] == 1:# question
         act_time['daytime_q'][int(hour_posted)]      = act_time['daytime_q'][int(hour_posted)] + 1
         act_time['monthtime_q'][int(month_posted)-1] = act_time['monthtime_q'][int(month_posted)-1] + 1
    elif posts['PostType'][index] == 2:# answer
         act_time['daytime_a'][int(hour_posted)]      = act_time['daytime_a'][int(hour_posted)] + 1
         act_time['monthtime_a'][int(month_posted)-1] = act_time['monthtime_a'][int(month_posted)-1] + 1

def resetActivity(act_time):
    act_time['daytime_q']   = [0]*24
    act_time['daytime_a']   = [0]*24
    act_time['monthtime_q'] = [0]*12
    act_time['monthtime_a'] = [0]*12

def HourActivity(daytime, hour_posted):
  #hour_posted = time.strftime("%H", time_posted)
  ## 7am - 12pm, 12pm - 6 pm, 6pm - 12am, 0am - 7 am
  #daytime = [0, 0, 0, 0]
  if int(hour_posted) < 7:
     daytime[0] = daytime[0] + 1
  elif int(hour_posted) < 12:
     daytime[1] = daytime[1] + 1
  elif int(hour_posted) < 18:
     daytime[2] = daytime[2] + 1
  elif int(hour_posted) < 24:
     daytime[3] = daytime[3] + 1

def MonthActivity(monthtime, month_posted):
  #hour_posted = time.strftime("%H", time_posted)
  ## 7am - 12pm, 12pm - 6 pm, 6pm - 12am, 0am - 7 am
  monthtime = [0]*12
  monthtime[month_posted-1] = monthtime[month_posted-1] + 1

def GetUserActivity(filename):
  f = open(filename)
  users_activity = csv.reader(f, delimiter=',', quotechar='|')
  return users_activity

def userActivityTransform(df):

    dfq_hour = pd.DataFrame(list(df['Q_HOUR']), columns=['qh1','qh2','qh3','qh4','qh5','qh6','qh7','qh8','qh9','qh10','qh11','qh12',
                                               'qh13','qh14','qh15','qh16','qh17','qh18','qh19','qh20','qh21','qh22','qh23','qh24'])
    dfa_hour = pd.DataFrame(list(df['A_HOUR']), columns=['ah1','ah2','ah3','ah4','ah5','ah6','ah7','ah8','ah9','ah10','ah11','ah12',
                                               'ah13','ah14','ah15','ah16','ah17','ah18','ah19','ah20','ah21','ah22','ah23','ah24'])

    dfq_month = pd.DataFrame(list(df['Q_MONTH']), columns=['qm1', 'qm2', 'qm3', 'qm4', 'qm5', 'qm6',
                                                      'qm7', 'qm8', 'qm9', 'qm10', 'qm11', 'qm12'])
    dfa_month = pd.DataFrame(list(df['A_MONTH']), columns=['am1', 'am2', 'am3', 'am4', 'am5', 'am6',
                                                      'am7', 'am8', 'am9', 'am10', 'am11', 'am12'])
    result = pd.concat([df['UserId'], dfq_hour, dfa_hour, dfq_month, dfa_month], axis=1)
    return result

def transformString(items):
    items = items.replace(",", "")
    items = items.replace("[", "")
    items = items.replace("]", "")
    items = items.split()
    return items

def extractDayWeekActivity(posts, year, month, day):
    #print year
    #print len(posts)
    posts = posts.loc[posts['year'].astype(int) == year]
    #print posts
    posts = posts.loc[posts['month'].astype(int) == month]
    #print posts
    #print 'this month', len(posts)
    #posts_week = posts_week[['UserId','PostType', 'year', 'month', 'day', 'hour', 'min']]
    posts_week = posts[posts['day'].astype(int) > day]
    posts_week = posts_week.sort(['UserId'], ascending=False)
    posts_week = posts_week.reset_index()
    #print posts_week
    #TODO if not saved, then indices must be put in order
    posts_day = posts_week[posts_week['day'] > 12]
    posts_day = posts_day[['UserId','PostType', 'year', 'month', 'day', 'hour', 'min']]
    posts_day = posts_day.sort(['UserId'], ascending=False)
    posts_day = posts_day.reset_index()
    #print 'this day', len(posts_day)
    #print posts_day
    return posts_week, posts_day

def extractTimeIntervalFeatures(posts_week, posts_day):
    activities_day = activityDay(posts_day)
    df_day = pd.DataFrame(activities_day, columns=['UserId', 'P_NUM_LAST_DAY'])
    #print df_day
    #activities last week
    activities = activityWeek(posts_week)
    df_week = pd.DataFrame(activities, columns=['UserId', 'Q_LAST_WEEK', 'A_LAST_WEEK'])
    #print df_week
    df_result = pd.merge(df_week, df_day, how='left', on='UserId')
    df_result = df_result.fillna(0)
    df_result['P_NUM_LAST_DAY'] = df_result['P_NUM_LAST_DAY'].astype(int)
    return df_result

def activityDay(posts):
    activities_day = []
    comments = 0
    #activities last day
    for index in xrange(0, len(posts)-1):
        comments = comments + 1
        if posts['UserId'][index] != posts['UserId'][index+1]:
            activities_day.append([posts['UserId'][index], comments])
            comments = 0
    return activities_day

def activityWeek(posts):
    activities = []
    act = dict(
        questions = 0,
        answers = 0,
    )
    for index in xrange(0, len(posts)-1):
        updateActivities(posts, act, index)
        if posts['UserId'][index] != posts['UserId'][index+1]:
            activities.append([posts['UserId'][index], act['questions'], act['answers']])
            act['questions'] = 0
            act['answers']= 0
    return activities


def updateActivities(posts, act, index):
    if posts['PostType'][index] == 1: # question
        act['questions'] = act['questions'] + 1
    elif posts['PostType'][index] == 2: # answer
        act['answers'] = act['answers'] + 1

def theLatestPostTime(posts):
    #TODO hardcoded for now - update
    year = 2014
    month = 7
    day = 7
    return year, month, day

def oneDayFromNow(year, day, month):
    #TODO hardcoded for now - update
    year = 2014
    month = 12
    day = 14
    return year, month, day
