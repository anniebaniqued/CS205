import re
import csv
import numpy as np

results = 0

files = ['data_infochimps_100.csv','data_venues_2.csv','data_companies_13836.csv']

fout=open("data_combined2.csv","a")
for file in files:
    for line in open("formatted_data/"+file):
        fout.write(line)

fout.close()
