import urllib2
import re
import numpy as np
import csv

from xml.dom.minidom import parseString
from functools import partial
from googlemaps import GoogleMaps
from incf.countryutils import transformations

## Specifies how much of the 22 000 000 + checkin data is going to be used
## A batch_sample_size of 15 will give about 1 000 000 checkins
## A batch_sample_size of 10 will give about   600 000 checkins
batch_sample_size = 1

def get_checkin_data():
    """ Loading data from checkin_data 
    returns a list of dictionary items with the elements:

    'user_id' 
    'lat' 
    'lng'
    'time'
    'text'
    'venue_id'
    """

    # open checkin_data.txt file containing 22388261 checkins
    checkin_file = open("foursquare/checkin_data.txt")
    checkins = list()

    # only takes a sample of the 22 million dataset
    i=0
    results = 0

    # reads in 10*1024**2 bytes at a time
    for buff in iter(partial(checkin_file.read, 10*1024**2), ''):
        if results < batch_sample_size: 
            entries = re.split('\n', buff)
            for entry in entries:
                try:
                    row = re.split('\t',entry)
                    user_id = int(row[0])
                    lat = row[2]
                    lng = row[3]
                    time = row[4]
                    text = row[5]
                    checkins.append({'user_id':user_id, 'lat':lat, 'lng':lng, 'time':time, 'text': text})
                except Exception:
                    i = i
                i+=1
        else:
            break
        results +=1
    print i

    return checkins

###############################

def get_user_data():
    """ Loading data from users_data
    returns a list of dictionary items with the elements:

    FOR USERS: 
    'user_id' 
    'status' - status count 
    'followers' - followers count
    'friends' - friends count
    """
    
    # open users_data.txt file
    users_file = open("foursquare/users_data.txt")
    data = users_file.read()
    users = list()

    entries = re.split('\n', data)
    for entry in entries:
        try:
            row = re.split('\t',entry)
            user_id = int(row[0])
            status = row[1]
            followers = row[2]
            friends = row[3]
            users.append({'user_id':user_id, 'status':status, 'followers':followers, 'friends':friends})
        except Exception:
            pass

    return users

############################################

def get_feature(data, feature, label = ''):
    """ Returns an NumPy.Array of the feature values of all items
    or of the items of a specific label.

    data -- List of dictionary items who all have at least
            the feature selected and the label element.
    feature -- Selected feature as a string
    label -- If set only items with this specific label are taken (DEFAULT = '')
    labelDictEntry -- if the dictionary entry is not named label it can be changed here.
    """
    ret_val = []
    for i in data:
        if (label == ''):
            ret_val.append(i[feature])
    return np.array(ret_val)

def uniqueList(seq, idfun=None):
    """ Returns a unique list of elements in preserved order.

    seq -- Any Sequence
    idfun -- Identification function on which the entry is unified
    """
    # order preserving 
    if idfun is None: 
        def idfun(x): return x 
    seen = {} 
    result = [] 
    for item in seq: 
        marker = idfun(item) 
        if marker in seen: continue 
        seen[marker] = 1 
        result.append(item) 
    return result

def getUniqueLabels(data, name = 'label'):
    """ Returns a List of the Labels in the data in the order they appear.
    Each label is only one time in the list.

    data -- List of Data elements as dictonaries who have at least the 'label' element.
    name -- Name of the dictionary entry for the label. This allows to have more than one label in the data dictionary.
    """
    ret_val = []
    for i in uniqueList(data, lambda item: item[name]):
        ret_val.append(i[name])
    return ret_val

def eval_labels(data, name = 'label'):
    """ Returns a dictionary with all labels and their numerical representation
    [0...numberOfLabels-1], as well as the number of occurences in the data.
    It also adds numerical entrys to convert a number to a label name.

    data -- List of Data elements as dictonaries who have at lest the 'label' element.
    name -- Name of the dictionary entry for the label. This allows to have more than one label in the data dictionary.
    """
    labels = {}
    label_list = getUniqueLabels(data)
    for i in range(len(label_list)):
        labels[label_list[i]] = [i, get_feature(data, name, label_list[i]).size]
        labels[i] = label_list[i]
    return labels

def addFeatureToData(data,featureName,featureFunction):
    """ Adds a new feature to the data set.

    data -- List of Data elements as dictonaries.
    featureName -- String of the feature name.
                   If it already exists the old feature will be over written.
    featureFunction(item) -- A function that takes an item of the data set and returns
                       the value of this feature.
    """
    for item in data:
        item[featureName] = featureFunction(item)

## ****************************************************************************

from datetime import datetime, date, time
import time

all_data = get_checkin_data()
## time_arr = get_feature(all_data, 'time')
## day_arr = np.zeros(7)
## for time in time_arr:
##     date_time = datetime.strptime(time, "%Y-%m-%d %H:%M:%S")
##     day = date_time.isoweekday() #1 is Monday and 7 is Sunday
##     day_arr[day-1] +=1
## print day_arr

i = 0

def add_country(item): 
    global i

    if i%50==0:
        time.sleep(.001)
        
    lat = item['lat']
    lng = item['lng']
    gmaps = GoogleMaps('ABQIAAAAu0ztSnkJ_S-_BzA-8maOXhQTdVdK_9Ld5ng0u3eDH3ut8YZvuBRKRiijF5aJ5D9LWbWZPvGs4NWWPw')

    result = gmaps.reverse_geocode(float(lat), float(lng))
    address = result['Placemark'][0]
    try:
        country_code = address['AddressDetails']['Country']['CountryNameCode']
        full_country_name = transformations.cc_to_cn(country_code)
    except Exception:
        country_code = 'None'
        full_country_name = 'None'

    i+=1
    
    return full_country_name

addFeatureToData(all_data, 'country', add_country)
print all_data
