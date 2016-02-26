# Aggregated features on users' activity as well as temporal patterns of user behavior are calculated here.
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

def MakePostsOld(data):
   posts = []
   i = 0
   for row in data:
       if i>0:#ignore the header
          sq = row[TIME_POSTED_INDEX].replace("T", " ")
          sq = sq[1:20]
          time_posted  = time.strptime(sq, "%Y-%m-%d %H:%M:%S")
          #year_posted  = time.strftime("%Y", time_posted)
          month_posted = time.strftime("%m", time_posted)
          #day_posted   = time.strftime("%d", time_posted)
          hour_posted  = time.strftime("%H", time_posted)
          min_posted   = time.strftime("%M", time_posted)
          #print hour_posted
          if row[USERID_INDEX] <> '':
             posts.append([row[USERID_INDEX], row[POST_TYPE_INDEX], month_posted, hour_posted, min_posted])
          #else:
             #print ("No User's ID")
       i = i + 1
   #print posts[2]
   #print i
   return posts

def MakePosts(data):
    #print data['TimePosted']
    #print data.head()
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
   activities = []
   act_time = dict(
       daytime_q   = [0]*24,
       daytime_a   = [0]*24,
       monthtime_q = [0]*12,
       monthtime_a = [0]*12,
   )
   num = 0
   print posts.head()
   for index in xrange(0, len(posts)-1):
       updateActivity(posts, index, act_time)
       if posts['UserId'][index] != posts['UserId'][index+1]:
           activities.append([posts['UserId'][index], act_time['daytime_q'],
                              act_time['daytime_a'], act_time['monthtime_q'], act_time['monthtime_a']])
           resetActivity(act_time)
           print ('new user:', posts['UserId'][index+1])
       else:
           updateActivity(posts, index, act_time)
           print ('same user:', posts['UserId'][index+1])
       num = num + 1
       print ('number: ', num)
   return activities

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
