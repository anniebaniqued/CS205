import re
import csv
import numpy as np

results = 0
compiled = csv.writer(open("data_combined.csv","wb"))

files = ['data_infochimps_100.csv','data_venues_.csv','data_companies_13836.csv']

fout=open("data_combined.csv","a")
# first file:
for file in files:
    for line in open("formatted_data/"+file):
        fout.write(line)

fout.close()
