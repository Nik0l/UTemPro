from collections import Counter
import csv
from itertools import chain
import Features as features
import pandas as pd
#import util as util

QUESTIONID_INDEX = 0
TAG_INDEX        = 4

def Stats(filename_input):
   f = open(filename_input)
   data_input = csv.reader(f, delimiter=',', quotechar='|')
   i = 0
   total_tags = []
   data = {'unique_tags': {}, 'tags': [], 'pairs': []}
   for row in data_input:
       if i > 0:#ignore the header
          total_tags_p = [] # empty tags
          tags = parseTags(row[TAG_INDEX])
          #print tags
          #print tags
          for tag in tags:
             total_tags_p.append(tag)
             total_tags.append(tag)
          if len(total_tags_p) > 1:
             pairs = PairsFromSet(total_tags_p)
             for pair in pairs:
                data['pairs'].append(pair)
          data['tags'].append(tags) #tags
       i = i + 1
   #print data['set_a']
   data['unique_tags'] = Counter(total_tags)
   return data

def TagsAvPopularity(tags, pop_table):
   av_popularity = 0
   for tag in tags:
      #print tag
      #print pop_table[tag]
      ind = pop_table['Tags'][pop_table['Tags'] == tag].index.tolist()[0]
      av_popularity = av_popularity + pop_table['Occurancy'][ind]
   av_popularity = av_popularity/len(tags)
   return av_popularity

def TagsNumPop(tags, pop_table):
   num_pop = 0
   #score   = [25, 50, 100]
   score   = [2, 5, 10]
   for tag in tags:
      ind = pop_table['Tags'][pop_table['Tags'] == tag].index.tolist()[0]
      if pop_table['Occurancy'][ind] > score[2]: # a very popular tag
         num_pop = num_pop + 3
      elif pop_table['Occurancy'][ind] > score[1]: # a moderately popular tag
         num_pop = num_pop + 2
      elif pop_table['Occurancy'][ind] > score[0]: # just a popular tag
         num_pop = num_pop + 1
   return num_pop

def TagsTogetherNum(tag_x, tag_y, rows):
   num_tag_xy = 0
   for tags in rows:
      if len(tags) > 1:
         if ElemTogether(tag_x, tag_y, tags):
            num_tag_xy = num_tag_xy + 1
   return num_tag_xy

def TagsCoOcProb(tag_x, tag_y, unique_tags, all_tags):
   prob_t      = 0.0
   #all_tags   = len(pop_table) # number of all different tags
   alltags_num = len(list(unique_tags.elements())) # number of all tags
   #all_ques   = len(set_a)
   prob_xy  = TagsTogetherNum(tag_x, tag_y, all_tags) # occurancy of two tags together somewhere
   prob_x   = unique_tags[tag_x] # occurancy of the first tag 
   prob_y   = unique_tags[tag_y] # occurancy of the second tag
   # the probability of the two tags to appear together
   prob_t  = (prob_xy * alltags_num * 100) / (prob_x * prob_y)
   #print "prob_t: ", prob_t
   return prob_t

def TagsCoOcProb1(tag_x, tag_y, unique_tags, table):
   prob_t      = 0.0
   #all_tags   = len(pop_table) # number of all different tags
   alltags_num = len(unique_tags) # number of all tags
   prob_xy = probCoOcfromTable(tag_x, tag_y, table) # occurancy of two tags together somewhere
   #prob_x  = unique_tags[tag_x] # occurancy of the first tag
   ind1 = unique_tags['Tags'][unique_tags['Tags'] == tag_x].index.tolist()[0]
   prob_x = unique_tags['Occurancy'][ind1]
   #prob_y  = unique_tags[tag_y] # occurancy of the second tag
   ind2 = unique_tags['Tags'][unique_tags['Tags'] == tag_y].index.tolist()[0]
   prob_y = unique_tags['Occurancy'][ind2]
   # the probability of the two tags to appear together
   if prob_x != 0 and prob_y != 0:
      prob_t = (prob_xy * alltags_num * 100) / (prob_x * prob_y)
   else:
      prob_t = 0
   #print "prob_t: ", prob_t
   return prob_t

def probCoOcfromTable(tag_x, tag_y, table):
   print table.head()
   prob = 0
   for index in xrange(0, len(table)):
      taggs = parseTags(table['Tags'][index])
      if tag_x in taggs:
         if tag_y in taggs:
            print table['Tags'][index]
            prob = table['Occurancy'][index]
            break
   print prob
   return prob

def TagsCoOcProbAv(tags, unique_tags, all_tags):
   tag_spec = 0
   pairs = PairsFromSet(tags)
   for pair in pairs:
      tag_spec = tag_spec + TagsCoOcProb(pair[0], pair[1], unique_tags, all_tags)
   tag_spec = tag_spec / len(pairs)
   return tag_spec
   
def parseTags(text):
   #print text
   s = text.replace("><", " ")
   s = s.replace("<", "")
   s = s.replace(">", "")
   s = s.replace('"', '')
   s = s.split()
   return s

def tagFeatures(data_input, unique_tags):
   data = []
   data1 = {'tags': []}
   for index in xrange(0, len(data_input)):
       s = parseTags(data_input['Tags'][index])
       for tag in s:
           data1['tags'].append(tag)
       av_pop  = TagsAvPopularity(data1['tags'], unique_tags)
       num_pop = TagsNumPop(data1['tags'], unique_tags)
       quest_id = data_input['QuestionId'][index]
       data.append([quest_id, av_pop, num_pop])
       data1 = {'tags': []}
   result = pd.DataFrame(data, columns=['QuestionId', 'AV_POPULARITY_AV', 'NUM_POP_TAGS'])
   return result

def TagCoOcStats(pairs, filename):
   myfile = open(filename, 'wb')
   wr = csv.writer(myfile)
   #wr.writerow(header)
   print "total: ", len(pairs)
   PAIRS_U = set([str(x) for x in pairs])
   print "unique: ", len(PAIRS_U)
   for pair in PAIRS_U:
      wr.writerow([pair])

#very slow
def TagPairsCoocurance(all_tags, fn_unique_tags, fn_tag_coocurance):
   f = open(fn_unique_tags)
   data = csv.reader(f, delimiter=',', quotechar='|')
   myfile = open(fn_tag_coocurance, 'wb')
   wr = csv.writer(myfile)
   wr.writerow(['Tags_pair','Q_NUM_TOGETHER'])
   i = 0
   sc = set(["[", "]", "'", '"'])
   for row in data:
      if i > 0: #ignore the header
          couple = str(row[0] + row[1])
          tags = ''.join([c for c in couple if c not in sc])
          tags = list(tags.split())
          times_together = TagsTogetherNum(tags[0], tags[1], all_tags)
          wr.writerow([tags,  times_together])
          #print times_together
      i = i + 1

def ElemTogether(elem1, elem2, elems):
   #num = 0
   if elem1 in elems:
      if elem2 in elems:
         return True
      else:
         return False
   else:
      return False

# creates all possible pair combination from a set 
def PairsFromSet(source):
   result = []
   for p1 in range(len(source)):
      for p2 in range(p1 + 1, len(source)):
         result.append([source[p1], source[p2]])
   return result

def sortPairList2(data):
    tally = Counter(chain(*map(set, data)))
    data.sort(key=lambda x: sorted(tally[i] for i in x))

def tagList(data):
   quest_tags = []
   for _tags in data['Tags']:
       tags = parseTags(_tags)
       quest_tags.append(tags) #tags
   #print quest_tags
   return quest_tags

def uniqueTags(df):
   all_tags = []
   for index in xrange(0, len(df['Tags'])):
      tags = parseTags(df['Tags'][index])
      for tag in tags:
          all_tags.append(tag)
      if (index % 100000) == 0:
          print index
   tagss = Counter(all_tags)
   #print tags
   df_unique = pd.DataFrame(tagss.items(), columns=['Tags', 'Occurancy'])
   return df_unique

def uniqueTagsFromTwoDf(df1, df2):
   print len(df2)
   tags = []
   for index in xrange(0, len(df2)):
      tags.append(df2['Tag1'][index])
      tags.append(df2['Tag2'][index])
   tags_unique = list(set(tags))
   #print 'unique tags: ', len(tags_unique)
   lists = []
   for index in xrange(0, len(tags_unique)):
      try:
          ind = df1['Occurancy'][df1['Tags'] == tags_unique[index]].index.tolist()[0]
          lists.append([tags_unique[index], df1['Occurancy'][ind]])
      except IndexError:
          #print tags_unique[index]
          lists.append([tags_unique[index], 0])
      if (index % 100) == 0:
         print index
   #print lists
   #print len(tags_unique)
   df = pd.DataFrame(lists, columns=['Tags', 'Occurancy'])
   return df

def specificityCalc(df, df_unique):
   lists = []
   alltags_num = len(df_unique)
   for index in xrange(0, len(df)):
      try:
         ind1 = df_unique['Tags'][df_unique['Tags'] == df['Tag1'][index]].index.tolist()[0]
         ind2 = df_unique['Tags'][df_unique['Tags'] == df['Tag2'][index]].index.tolist()[0]
         prob_xy = df['Occurancy_Tags12'][index]
         prob_x = df_unique['Occurancy'][ind1]
         prob_y = df_unique['Occurancy'][ind2]
         tag_spec = float(prob_xy) * alltags_num * 100 / (prob_x * prob_y)
         lists.append([df['Tags'][index], df['Tag1'][index], df['Tag2'][index], prob_xy, prob_x, prob_y, tag_spec])
      except IndexError:
         lists.append([df['Tags'][index], df['Tag1'][index], df['Tag2'][index], 0, 0, 0, 0])
      if (index % 1000) == 0:
         print index
   #print len(lists)
   df_occ = pd.DataFrame(lists, columns=['Tags', 'Tag1', 'Tag2', 'Occurancy_Tags12',
                                         'Tag1_Occurancy', 'Tag2_Occurancy', 'TAG_SPECIFICITY'])
   return df_occ

def tags(df):
   tags_npr = []
   for index in xrange(0,len(df['Tags'])):
      num = df['Tags'][index].count('>')
      if num == 2:#only two tags
         tags_npr.append([df['QuestionId'][index], df['Tags'][index]])
      if (index % 50000) == 0:
         print index
   df2 = pd.DataFrame(tags_npr, columns=['QuestionId', 'Tags'])
   tags = Counter(df2['Tags'])
   #print tags
   df2_occ = pd.DataFrame(tags.items(), columns=['Tags', 'Occurancy_Tags12'])
   lists = []
   for index in xrange(0, len(df2_occ)):
      tags = parseTags(df2_occ['Tags'][index])
      lists.append([df2_occ['Tags'][index], tags[0], tags[1], df2_occ['Occurancy_Tags12'][index]])
   df2tags_occ = pd.DataFrame(lists, columns=['Tags', 'Tag1', 'Tag2', 'Occurancy_Tags12'])
   return df2, df2tags_occ

def matchAtoB(dfA, dfB):
   dfA = dfA.sort('Tags', ascending=True)
   dfB = dfB.sort('Tags', ascending=True)
   dfA = dfA.reset_index(drop=True)
   dfB = dfB.reset_index(drop=True)
   #print len(dfB)
   #print len(dfA)
   #print dfA.head()
   #print dfB.head()
   lists = []
   indices = []
   ind = 0
   lists.append([dfB['QuestionId'][0], dfA['TAG_SPECIFICITY'][ind]])
   for index in xrange(0, len(dfB)-1):
      if dfB['Tags'][index] != dfB['Tags'][index+1]:
          #print 'new tag'
          ind = ind + 1
      lists.append([dfB['QuestionId'][index+1], dfA['TAG_SPECIFICITY'][ind]])
      if (index % 10000) == 0:
          print index
   result = pd.DataFrame(lists, columns=['QuestionId', 'TAG_SPECIFICITY'])
   return result
