import re
import csv
import numpy as np

folders = ['ldn', 'nyc', 'par']
results = 0
compiled = csv.writer(open("formatted_data/data_venues_2.csv","wb"))

for folder in folders:
    files = ['arts-venues.csv','food-venues.csv','nightlife-venues.csv','park-venues.csv','shop-venues.csv']
    for file in files: 
        file = open("data/venues-foursquare-0710/"+folder+"/"+file)
        data = file.read()
        file.close()
        
        entries = re.split('\n', data)
        
        for i in range(1, len(entries)):
            row =  entries[i].split(',')
            if len(row)==5 and row[2]!='' and row[3]!='' and row[4]!='':
                lat =  np.float64(row[2])
                lng =  np.float64(row[3])
                #for i in range(0,int(row[4])):
                compiled.writerow( (lat, lng) )  

        results+=1

        print results
