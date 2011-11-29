import urllib2
import re
import csv
import numpy as np
import matplotlib.pyplot as plt 
import matplotlib.cm as cm
from matplotlib.font_manager import fontManager, FontProperties

file = open("data_for_fiona_01252011.csv")
data = file.read()
file.close()

entries = re.split('\r', data)
results = 0

lat = []
lng = []

fig = plt.figure()
ax = fig.add_subplot(1,1,1)

for i in range(0, len(entries)):
    try:
        lt = np.float64(entries[i].split(',')[0])
        ln = np.float64(entries[i].split(',')[1])
        if (abs(lt)<=90 and abs(ln)<=180):
             lat.append(lt)
             lng.append(ln)
             results+=1
    except Exception:
        results+=1

#print lat[0:5]
#print lng[0:5]
plt.scatter(np.asarray(lng), np.asarray(lat))

plt.show()
