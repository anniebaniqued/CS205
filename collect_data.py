import urllib2
import re
import csv

api_key = 'anniebaniqued-ZPim1vQ29-0O2CEcHldZ_zjTC69'

url = 'http://api.infochimps.com/geo/location/foursquare/places/search?apikey='+api_key 

usock = urllib2.urlopen(url)
data = usock.read()
usock.close()

#file = open("data.txt")
#data = file.read()
#file.close()

entries = re.split('{"md5id":', data)
results = 0

compiled = csv.writer(open('data_infochimps_100.csv', 'wb'), delimiter=' ')

for i in range(1, len(entries)):
    print entries[i].split('"coordinates":[')[1].split('],')[0]
    compiled.writerow(entries[i].split('"coordinates":[')[1].split('],')[0])
    results+=1

print results
