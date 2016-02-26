# A set of database queries to run from Python. Since the size of databases is large, these queries are saved in 1) shelve files 2) the results - in a csv format
__author__ = 'nb254'
import sqlite3
import numpy
import csv
import sys
sys.path.append("/mnt/nb254_data/src/utils/")
#import pandas as pd
from once import once, oncecleardb, onceprintdb, onceinit

DIR = '/mnt/nb254_data/db/'

def runquery(c,query,parameters=()):
    c.execute(query,parameters)
    return c.fetchall()

def DBConnect(dbname):
   onceinit(__file__)
   #run the query
   conn = sqlite3.connect(DIR + dbname + '.db')
   c = conn.cursor()
   c.execute('PRAGMA temp_store=MEMORY')
   c.execute('PRAGMA cache_size=500000')
   return c

def Test():
   onceinit(__file__)
   #run the query
   conn = sqlite3.connect('/mnt/nb254_data/db/stackoverflow.db')
   c = conn.cursor()
   c.execute('PRAGMA temp_store=MEMORY')
   c.execute('PRAGMA cache_size=500000')
   result = once(lambda x: runquery(c,x),'''SELECT q.Tags as Tags, MIN(strftime('%s', a.CreationDate)-strftime('%s',q.CreationDate)) as SecondsToFirstAnswer FROM posts as q, posts as a WHERE q.PostTypeId = 1;''') # LIMIT 100000

def PostsPerUser(connector):
   result = once(lambda x: runquery(connector, x),'''SELECT users.Id as UserId, count(posts.OwnerUserId) as U_POSTS
FROM Posts, users WHERE users.Id = posts.OwnerUserId GROUP BY users.Id;''') # LIMIT 100000
   return result

def QuestPerUser(connector):
   result = once(lambda x: runquery(connector, x),'''SELECT Users.Id as UserId, count(Posts.Id) as U_QUESTIONS
FROM Posts, Users on Users.Id = OwnerUserId WHERE PostTypeId = 1 GROUP BY Users.Id;''') # LIMIT 100000
   return result

def AnsPerUser(connector):
   result = once(lambda x: runquery(connector, x),'''SELECT Users.Id as UserId, count(Posts.Id) as U_ANSWERS
FROM Posts, Users on Users.Id = OwnerUserId WHERE PostTypeId = 2 GROUP BY Users.Id;''') # LIMIT 100000
   return result

def UsersStats(connector):
   result = once(lambda x: runquery(connector, x),'''SELECT Users.Id as UserId, Users.DisplayName as Name, Users.Location as LOCATION, Users.CreationDate as DateCreated, ((strftime('%s','2014-09-26T00:00:00.000') - strftime('%s',Users.CreationDate))/(60*60*24)) as DAYS_ON_SITE, Users.Reputation as U_REPUTATION, Users.UpVotes as U_UPVOTES, Users.DownVotes as U_DOWNVOTES, Users.Views as U_VIEWS FROM Users GROUP BY Users.Id;''') # LIMIT 100000
   return result

def UsersAvAnsTime(connector):
   result = once(lambda x: runquery(connector, x),'''SELECT q.OwnerUserId as UserId, AVG((strftime('%s', a.CreationDate)-strftime('%s',q.CreationDate))) as U_AV_ANS_TIME FROM posts as q, posts as a WHERE q.PostTypeId = 1 and q.AcceptedAnswerId = a.Id GROUP BY q.OwnerUserId;''') # LIMIT 100000
   return result

def QuestWithAcceptedAnswers(connector):
   result = once(lambda x: runquery(connector, x),'''SELECT q.Id as PostId, q.OwnerUserId as UserId, q.Title as TitleQ, q.Body as BodyQ FROM posts as q, posts as a WHERE q.PostTypeId = 1 and q.AcceptedAnswerId = a.Id;''') # LIMIT 100000
   return result

def FirstAnsTime(connector):
   result = once(lambda x: runquery(connector, x),'''SELECT q.Id as QuestionId, q.CreationDate as Q_ASKED, MIN(strftime('%s', a.CreationDate)-strftime('%s',q.CreationDate)) as SecondsToFirstAnswer FROM posts as q, posts as a WHERE q.PostTypeId = 1 AND a.ParentId = q.Id GROUP BY q.Id;''') # LIMIT 100000
   return result

def AcceptAnsTime(connector):
   result = once(lambda x: runquery(connector, x),'''SELECT q.Id as QuestionId, q.CreationDate as Q_ASKED,
(strftime('%s', a.CreationDate)-strftime('%s',q.CreationDate)) as SecondsToAcceptedAnswer FROM posts as q, posts as a WHERE q.PostTypeId = 1 and q.AcceptedAnswerId = a.Id;''') # LIMIT 100000
   return result

def UpvotedAnsTime(connector):
   result = once(lambda x: runquery(connector, x),'''SELECT q.Id as QuestionId, q.CreationDate as Q_ASKED, MIN (strftime('%s', a.CreationDate)-strftime('%s',q.CreationDate)) as SecondsToUpvotedAnswer FROM posts as q, posts as a WHERE q.PostTypeId = 1 AND a.ParentId = q.Id AND a.Score > 0 GROUP BY q.Id;''') # LIMIT 100000
   return result

def FirstAnsTime1(connector):
   result = once(lambda x: runquery(connector, x),'''SELECT q.Id as QuestionId, q.CreationDate as Q_ASKED, (strftime('%s', a.CreationDate)-strftime('%s',q.CreationDate)) as SecondsToAcceptedAnswer, a.Id as AnswerId, q.OwnerUserId as AskerId, a.OwnerUserId as AnswererId FROM posts as q, posts as a WHERE q.PostTypeId = 1 and q.AcceptedAnswerId = a.Id;''') # LIMIT 100000
   return result

def AcceptAnsTime1(connector):
   result = once(lambda x: runquery(connector, x),'''SELECT q.Id as QuestionId, q.CreationDate as Q_ASKED, MIN(strftime('%s', a.CreationDate)-strftime('%s',q.CreationDate)) as SecondsToFirstAnswer, a.Id as AnswerId, q.OwnerUserId as AskerId, a.OwnerUserId as AnswererId FROM posts as q, posts as a WHERE q.PostTypeId = 1 AND a.ParentId = q.Id GROUP BY q.Id;''') # LIMIT 100000
   return result

def UpvotedAnsTime1(connector):
   result = once(lambda x: runquery(connector, x),'''SELECT q.Id as QuestionId, q.CreationDate as Q_ASKED, MIN (strftime('%s', a.CreationDate)-strftime('%s',q.CreationDate)) as SecondsToUpvotedAnswer, a.Id as AnswerId, q.OwnerUserId as AskerId, a.OwnerUserId as AnswererId FROM posts as q, posts as a WHERE q.PostTypeId = 1 AND a.ParentId = q.Id AND a.Score>0 GROUP BY q.Id;''') # LIMIT 100000
   return result

def NumUsers(connector):
   result = once(lambda x: runquery(connector, x),'''select count(*) as U_NUM from users;''') # LIMIT 100000
   return result

def NumQuestions(connector):
   result = once(lambda x: runquery(connector, x),'''select count(*) as Q_NUM from posts where PostTypeId=1;''') # LIMIT 100000
   return result

def NumAnswers(connector):
   result = once(lambda x: runquery(connector, x),'''select count(*) as ANSWERS_NUM from posts where PostTypeId=2;''') # LIMIT 100000
   return result

def NumComments(connector):
   result = once(lambda x: runquery(connector, x),'''select count(*) as COMMENTS_NUM from comments;''') # LIMIT 100000
   return result

def AnswerDistribution(connector):
   result = once(lambda x: runquery(connector, x),'''select AnswerCount, count(*) as Q_NUM from posts where PostTypeId=1 group by AnswerCount;''') # LIMIT 100000
   return result

def NumAcceptedAnswers(connector):
   result = once(lambda x: runquery(connector, x),'''select count(*) as Q_W_ACC_ANSWERS from posts where PostTypeId=1 and AcceptedAnswerId is not null;''') # LIMIT 100000
   return result

def AcceptedAnswers(connector):
   result = once(lambda x: runquery(connector, x),'''SELECT AcceptedAnswerId as AcceptedAnswerId , Users.Id as UserId FROM Posts, Users WHERE AcceptedAnswerId<>'' and users.Id = posts.OwnerUserId GROUP BY UserId;''') # LIMIT 100000
   return result

def PostsStats(connector):
   result = once(lambda x: runquery(connector, x),'''SELECT CreationDate as TimeCreated, PostTypeId as PostTypeId
FROM posts GROUP BY CreationDate;''') # LIMIT 100000
   return result

def PostsTitleLength_OLD(connector):
   result = once(lambda x: runquery(connector, x),'''SELECT Posts.Id as PostId, Posts.OwnerUserId as UserId, Posts.PostTypeId as PostTypeId, (length(Title) - length(replace(Title, ' ', '')) +1) as TITLE_LENGTH,
(length(Body) - length(replace(Body, ' ', '')) +1) as BODY_LENGTH FROM Posts GROUP BY Posts.Id;''') # LIMIT 100000
   return result

def PostsText_Data(connector):
   result = once(lambda x: runquery(connector, x),'''SELECT Id as PostId, OwnerUserId as UserId, Title as Q_Title, Body as Q_Body, (length(Title) - length(replace(Title, ' ', '')) +1) as TITLE_LENGTH, (length(Body) - length(replace(Body, ' ', '')) +1) as BODY_LENGTH FROM posts WHERE PostTypeId = 1;''') # LIMIT 100000
   return result

def PostsText_Data1(connector):
   result = once(lambda x: runquery(connector, x),'''SELECT Id as PostId, OwnerUserId as UserId, Title as Q_Title, Body as Q_Body FROM posts WHERE PostTypeId = 1;''') # LIMIT 100000
   return result

def QuestStats(connector):
   result = once(lambda x: runquery(connector, x),'''SELECT q.Id as QuestionId, q.OwnerUserId as UserId, a.OwnerUserId as AnswererId, q.ViewCount as Q_VIEWS,  q.Tags as Tags, q.CreationDate as TimeAsked, a.CreationDate as TimeAnswered, (strftime('%s', a.CreationDate)-strftime('%s',q.CreationDate)) as SecondsToAcceptedAnswer, a.Id as AnswerId FROM posts as q, posts as a WHERE q.PostTypeId = 1 and q.AcceptedAnswerId = a.Id GROUP BY q.Id;''') # LIMIT 100000
   return result

def UsersActivity(connector):
   result = once(lambda x: runquery(connector, x),'''SELECT Posts.Id as PostId, Posts.OwnerUserId as UserId,  Posts.CreationDate as TimePosted, Posts.PostTypeId as PostType FROM Posts, Users on Users.Id = OwnerUserId GROUP BY Posts.Id;''') # LIMIT 100000
   return result

def UsersBehaviour(connector):
   #TODO: check whether the command was executed already
   first = False
   if first:
      connector.execute('''create table answerers(userid INTEGER PRIMARY KEY);''')
      connector.execute('''create table askers(userid INTEGER PRIMARY KEY);''')
      connector.execute('''create table voters(userid INTEGER PRIMARY KEY);''')

      connector.execute('''insert into answerers (userid) select distinct users.id from users, posts where posts.posttypeid = 2 and posts.owneruserid = users.id;''')
      connector.execute('''insert into askers (userid) select distinct users.id from users, posts where posts.posttypeid = 1 and posts.owneruserid = users.id;''')
      connector.execute('''insert into voters (userid) select distinct users.id from users where upvotes > 0 OR downvotes > 0;''')

   data = {'q': 0, 'a': 0, 'v': 0, 'qa': 0, 'qv': 0, 'av': 0, 'qva': 0, 'u': 0}
   # count folks who questioned, answered, voted
   data['qva'] = once(lambda x: runquery(connector, x),'''select count(*) from voters, askers, answerers where voters.userid = askers.userid and askers.userid = answerers.userid;''')[0][0]
   # count folks who questioned, answered
   data['qa'] = once(lambda x: runquery(connector, x),'''select count(*) from askers, answerers where askers.userid = answerers.userid;''')[0][0]
   data['qv'] = once(lambda x: runquery(connector, x),'''select count(*) from askers, voters where askers.userid = voters.userid;''')[0][0]
   data['av'] = once(lambda x: runquery(connector, x),'''select count(*) from answerers, voters where answerers.userid = voters.userid;''')[0][0]
   # count folks who questioned, answered
   data['q'] = once(lambda x: runquery(connector, x),'''select count(*) from askers;''')[0][0]
   data['a'] = once(lambda x: runquery(connector, x),'''select count(*) from answerers;''')[0][0]
   data['v'] = once(lambda x: runquery(connector, x),'''select count(*) from voters;''')[0][0]
   data['u'] = once(lambda x: runquery(connector, x),'''select count(*) from users;''')[0][0]
   #print data
   return data

def TagStats(connector):
   result = once(lambda x: runquery(connector, x),'''SELECT q.Id as QuestionId,
MIN (strftime('%s', a.CreationDate)-strftime('%s',q.CreationDate)) as SecondsToUpvotedAnswer, q.body, q.tags
FROM posts as q, posts as a WHERE q.PostTypeId = 1 AND a.ParentId = q.Id AND a.Score > 0 GROUP BY q.Id''')
   return result

def NumofViews(connector, maxdate, s):
   result = once(lambda sql, arg: runquery(connector, sql, arg),'''SELECT ViewCount as Q_VIEWS, Count(*) as Q_VIEW_COUNT FROM posts WHERE (PostTypeId=1 AND CAST((strftime('%s',?) - strftime('%s',CreationDate)) AS INTEGER) < ?) GROUP BY ViewCount''', (maxdate, s))
   return result

def QuestTitleAnswers(connector):
   result = once(lambda x: runquery(connector, x),'''SELECT (length(Title) - length(replace(Title, ' ', '')) +1) as TITLE_LENGTH, (length(Body) - length(replace(Body, ' ', '')) +1) as BODY_LENGTH, AnswerCount as ANSWERS_NUM, Title as Q_TITLE FROM posts;''')
   return result

def RequestQuestion(connector, QuestionId):
   result = once(lambda x: runquery(connector, x),'''SELECT Id as postId, OwnerUserId as userId,
   Title as title, Body as body, CreationDate as timePosted, Tags as tags FROM Posts WHERE Id = ''' + str(QuestionId) + ''';''') # LIMIT 100000
   return result
