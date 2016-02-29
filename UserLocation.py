# Extracting users' longitude, latitude, time zone, region, country from a textually written location.
__author__ = 'nb254'
#Requires a table 'users_stats.csv' where users' information is stored
from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut
from geopy.exc import GeocoderParseError
from geopy.exc import GeocoderServiceError
from geopy import geocoders # pip install geopy
from datetime import datetime
from collections import Counter
import time, csv
#import geonamescache
from geopy.geocoders import GeoNames
#from geonames import geonames
from tzwhere import tzwhere
from pytz import timezone
import pytz
import requests
from pytz import UnknownTimeZoneError
import enchant
from nltk.metrics import edit_distance
import Features as features
import pandas as pd
from collections import Counter
# you really wanna do something more useful with the data...
TIME    = 60 * 30 # one hour
started = True

USERID_INDEX        = 0
USER_NAME_INDEX     = 1
USER_LOCATION_INDEX = 2

HEADER2 = features.KEY_LOC + features.USER_LOC
HEADER  = ['UserId'] + features.KEY_LOC + features.USER_LOC + ['USERS_SAME_LOC']

#db_name      = 'android'
#file_name     = 'users_stats.csv'
file_name_ul  = 'UNIQUE_LOCATIONS.csv'
file_name_ul2 = 'UNIQUE_LOCATIONS2.csv'
file_name_tem = 'users_locations.csv'
file_name_fin = 'users_locations1.csv'

#create a list of unique locations (dictionary)
def UniqueLocations(locs):
   locs_unique = Counter(locs)
   print locs_unique
   un = pd.DataFrame(locs_unique.items(), columns=['LOCATION', 'USERS_SAME_LOC'])
   print 'unique locations:', len(un)
   return un

##########deprecated - too less queries are available#########################
def writeLocTZ(user_name, locs, file_name):
   # coordinates of user's location are saved
   csv_writer = csv.writer(open(file_name, 'a'))
   HEADER = ['Unique_Locations', 'LAT', 'LON']
   csv_writer.writerow(HEADER)
   #geolocator = Nominatim()
   #g = geocoders.GoogleV3()
   geolocator     = GeoNames(username=user_name)
   g              = geocoders.GeoNames(username=user_name)
   rows = [] #new data
   #print locs
   for loc in locs:
      #if the data was not filled
      if loc[0] != '':
         coord    = coordFromLocName(loc[0], geolocator, g)
         #timezone = Timezone(coord, time_diff)
         res      = [loc[0], coord[0], coord[1]]
         csv_writer.writerow(res)

def coordFromLocName(loc, geolocator, g):
   # coordinates of user's location
   coord     = [0, 0]
   #print Location
   if loc != '':
      try:
         location = geolocator.geocode(loc)
         try:
            #print(location.address)
            #print((location.latitude, location.longitude))
            coord = [location.latitude, location.longitude]
         except AttributeError:
            print ('AttributeError: ' + loc)
      #sometimes the timeout error happens
      except GeocoderTimedOut as e:
            print("Error: geocode failed on input %s with message"%(loc))
   return coord

def Timezone(coord, time_diff, g):
   timezone  = 0
   if coord != [0, 0]:
      try:
          timezone  = g.timezone((coord[0], coord[1]))
          time_diff = datetime.now(timezone).strftime('%z')
      except GeocoderParseError:
          print ("GeocoderParseError: " + str(coord))
   else:
      timezone  = 'somewhere'
      time_diff = 0
   return timezone

def SavetoCSV(data, header, file_name):
   csv_writer = csv.writer(open(file_name, 'wb'))
   csv_writer.writerow(header)
   for row in data:
      csv_writer.writerow([row])

def OpenCSV(file_name):
   data = csv.reader(open(file_name))
   res = []
   for row in data:
      res.append(row)
   return res

def OpenUniqueLocCSV(file_name):
   data = csv.reader(open(file_name))
   res = []
   for row in data:
      res.append([row[0], row[1], row[2]])
   return res

#match users' location with their timezones
def matchLocations(data, data_unique, HEADER, file_name):
   LOC_INDEX  = 0
   csv_writer = csv.writer(open(file_name, 'wb'))
   csv_writer.writerow(HEADER)
   look_up = []
   for each in data_unique:
      look_up.append(each)
      #print look_up
   for row in data:
       for i in range (1, len(look_up)):
          if row[USER_LOCATION_INDEX] == look_up[i][LOC_INDEX] and row[USER_LOCATION_INDEX] != '':
             csv_writer.writerow([row[USERID_INDEX]] + look_up[i])

def deleteEmptyRows(file_name_o, HEADER, file_name_s):
   LAT_INDEX   = 2
   LON_INDEX   = 3
   res = []
   loc = []
   dat = csv.reader(open(file_name_o))
   data = []
   for row in dat:
      data.append(row)
   csv_writer = csv.writer(open(file_name_s, 'wb'))
   #print "number of rows: ", len(data)
   csv_writer.writerow(HEADER)
   i = 0
   j = 0
   for row in data:
      if row[LAT_INDEX] <> '0' and row[LON_INDEX] <> '0' and i>0:
         res.append(row)
         loc.append(row[USER_LOCATION_INDEX])
         j +=1
      i +=1
   unique = Counter(loc)
   for entry in res:
      entry = entry + [unique[entry[2]]]
      #print entry
      csv_writer.writerow(entry)
   #print unique[LAT]
   print "total users: ", i
   print "no location for users: ",(i-j)

def findTimezones(user_name, file_name, file_name_s):
   geolocator = GeoNames(username=user_name)
   g = geocoders.GeoNames(username=user_name)
   location_index = 0
   lat_index = 1
   lon_index = 2
   res = []
   data = []
   HOUR = 60 * (60 + 4)
   utc = pytz.utc
   utc.zone
   dat = csv.reader(open(file_name))
   w = tzwhere.tzwhere()
   i = 0
   for row in dat:
      if i>0:
         data.append([row[location_index], row[lat_index], row[lon_index]])
      i = i + 1
   csv_writer = csv.writer(open(file_name_s, 'wb'))
   #print "number of rows: ", len(data)
   csv_writer.writerow(HEADER2)
   for row in data:
      if (row[lat_index] <> '0' and row[lon_index] <> '0'):
         lat = float(row[lat_index])
         lon = float(row[lon_index])
         timezone = w.tzNameAt(lat, lon)
         print lat
         print lon
         print timezone
         try:
            country_info = reverceGeoCode([row[lat_index], row[lon_index]], g, geolocator, user_name)
         except GeocoderServiceError:
            print "hourly limit has been exceeded, time to wait for an hour..."
            time.sleep(HOUR)
            print "starting again..."
            country_info = reverceGeoCode([row[lat_index], row[lon_index]], g, geolocator, user_name)
         try:
            time_diff = timeDifference(utc, timezone)
         except AttributeError:
            time_diff = 0
            print timezone
         temp = [row[location_index], row[lat_index], row[lon_index], timezone, time_diff, country_info[2], country_info[3], country_info[4]]
      else:
         temp = row + [0,0,0,0,0]
      res.append(temp)
      try:
         csv_writer.writerow(temp)
      except UnicodeEncodeError:
         csv_writer.writerow(row + [0,0,0,0,0])
   return res

def timeDifference(utc, Time_Zone):
   print Time_Zone
   try:
      time_zone = timezone(Time_Zone)
      loc_dt    = time_zone.localize(datetime(2015, 02, 27, 6, 0, 0))
      time_diff = loc_dt.strftime('%z')
   except UnknownTimeZoneError:
      time_zone = 0
      time_diff = 0
   print time_diff
   return time_diff

def reverceGeoCode(coord, g, geolocator, user_name):
   try:
      location = geolocator.reverse(coord)
      url1 = 'http://api.geonames.org/countrySubdivisionJSON?lat='+str(coord[0])+'&lng='+str(coord[1])+'&username='+user_name
      response = requests.get(url1)  #GET call
      data = response.json()     #make a dictionary from JSON response
      print data
      try:
         loc_info = [coord[0], coord[1], data['distance'], data['countryCode'], data['adminName1']]
      except KeyError:
         try:
            loc_info = [coord[0], coord[1], data['distance'], data['countryCode'], 0]
         except KeyError:
            try:
               loc_info = [coord[0], coord[1], 0, data['countryCode'], 0]
            except KeyError:
               loc_info = [coord[0], coord[1], 0, 0, 0]
      print loc_info
   except GeocoderTimedOut as e:
      loc_info = [coord[0], coord[1], 0, 0, 0]
   return loc_info

def spellChecker(sentences, file_name_s):
   dict_name  = 'en_GB'
   spell_dict = enchant.Dict(dict_name)
   max_dist   = 3
   corrected  = []
   csv_writer = csv.writer(open(file_name_s, 'wb'))
   #csv_writer.writerow(HEADER2)
   for sentence in sentences:
      corrected_sent = ''
      sentence = str(sentence)
      sc = set(["[", "]", "'", '"'])
      words = ''.join([c for c in sentence if c not in sc])
      words = words.split()
      #print words
      for word in words:
         print word
         suggestions = spell_dict.suggest(word)
         #print suggestions[0]
         #print edit_distance(word, suggestions[0])
         if suggestions and edit_distance(word, suggestions[0]) <= max_dist:
            #print word
            corrected_sent = corrected_sent + " " + suggestions[0]
         else:
            corrected_sent = corrected_sent + " " + word
            corrected_sent.replace("[","")
            corrected_sent.replace("]","")
            corrected_sent.replace("'","")
         #print corrected_sent
      corrected.append(corrected_sent)
      csv_writer.writerow([corrected_sent])
   print corrected

def findLocations(user_name, locs, file_name_s):
   #TODO: delete before committing
   geolocator = GeoNames(username=user_name)
   g = geocoders.GeoNames(username=user_name)
   csv_writer = csv.writer(open(file_name_s, 'wb'))
   csv_writer.writerow(['LOCATION', 'LAT', 'LON'])
   for loc in locs:
      loc = str(loc)
      coord = coordFromLocName(loc, geolocator, g)
      csv_writer.writerow([loc, coord[0], coord[1]])

#############################################################
'''
#data = csv.reader(open(file_name))
#find unique locations
#uniq_locs = UniqueLocations(data)
#SavetoCSV(uniq_locs, HEADER, file_name_ul)
# open unique locations
DIR = '/mnt/nb254_data/src/data/'
file_name = DIR + 'users_stats.csv'
file_name_ul  = DIR + 'derived_data/unique_locations.csv'
file_name1 = DIR + 'derived_data/unique_locations_geodata.csv'
file_name_ul2 = DIR + 'derived_data/unique_locations_geodata1.csv'
file_name_tem = DIR + 'derived_data/users_locations.csv'
#uniq_locs = OpenCSV(file_name_ul)
#print uniq_locs
#WriteLocTZ(uniq_locs, file_name1)
#users' statistics
data = OpenCSV(file_name)
# create the file with the unique locations
#SpellChecker(uniq_locs, 'corrected_loc.csv')
#locs = OpenCSV('corrected_loc.csv')
#FindLocations(locs, 'LOCS.csv')
#FindTimezones(file_name1, file_name_ul2)
# open the file with the unique locations
data_unique = csv.reader(open(file_name_ul2))
# match the information from the unique locations file to the users' IDs
matchLocations(data, data_unique, HEADER, file_name_tem)
#deleteEmptyRows(file_name_tem, HEADER, file_name_fin)
'''
