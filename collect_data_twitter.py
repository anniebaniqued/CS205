import urllib2
import re
import csv
import numpy as np

file = open("data/twitter_foursquare.csv")
data = file.read()
file.close()

entries = re.split('\n', data)
results = 0

compiled = csv.writer(open('formatted_data/data_twitter.csv', 'wb'))

for i in range(1, len(entries)):
    try:
        row = entries[i].split('"')[1].split('"')[0]
        lat = np.float64(row.split(',')[0])
        lng = np.float64(row.split(',')[1])
        compiled.writerow( (lat, lng) )
        results+=1
        print lat
        print lng
    except Exception:
        results = results
        
print results
