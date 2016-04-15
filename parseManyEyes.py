import pandas as pd
import xml.etree.ElementTree as ET
import glob
from collections import Counter

def iter_docs(feed):
    data = []
    for doc in feed.iterfind('.//{http://www.w3.org/2005/Atom}entry'):
	title = doc.find('{http://www.w3.org/2005/Atom}title').text
	date = doc.find('{http://www.w3.org/2005/Atom}published').text
	author = doc.find('{http://www.w3.org/2005/Atom}author')
	name = author.find('{http://www.w3.org/2005/Atom}name').text
	datum = [title, date, name]
	data.append(datum)
    return data

def parseFiles(outputfile):
    #DIR = '/home/hduser/Desktop/tests/PARSED_DATA_MANYEYES/DATA/'
    # the path to crawled xml files
    DIR = '/home/hduser/Dropbox/DATA/DATA/'
    filename = 'manyeyes_'

    doc_df = pd.DataFrame(list([]), columns=['Title', 'Date', 'Name'])
    doc_df.to_csv(outputfile)

    filenames = glob.glob(DIR + "*.xml")

    for afile in filenames:
        print afile
        tree = ET.parse(afile)
        root = tree.getroot()
        doc_df = pd.DataFrame(list(iter_docs(root)))
        doc_df.to_csv(outputfile, mode='a', header=False, encoding='utf-8')
        
def statsData(outputfile):
	df = pd.read_csv(outputfile)
	df['Date'] = pd.to_datetime(df['Date'])
	df['year'] = df['Date'].dt.year
	df['month'] = df['Date'].dt.month
	df['day'] = df['Date'].dt.day
	print df['Date'][0:5]
	print df.head()
	print df.shape
	people = list(Counter(df['Name']))
	datasets = list(Counter(df['Title']))
	years = Counter(df['year'])
	print years
	print len(people)
	print len(datasets)
	#not extracted
	#print (490982 - 489900)/489.900
	
outputfile = 'parse.csv'
parseFiles(outputfile)
statsData(outputfile)


