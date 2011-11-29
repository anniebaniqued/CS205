import urllib2
import re
import csv
import numpy as np

file = open("data/twitter_foursquare.csv")
data = file.read()
file.close()

entries = re.split('', data)
results = 0

compiled = csv.writer(open('formatted_data/data_infochimps_100.csv', 'wb'))

for i in range(1, len(entries)):
    row = entries[i].split('"coordinates":[')[1].split('],')[0]
    lat = np.float64(row.split(',')[0])
    lng = np.float64(row.split(',')[1])
    compiled.writerow( (lat, lng) )  
    results+=1

print results
