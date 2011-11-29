import re

from xml.dom.minidom import parseString

# open data_combined.csv
file = open("test_w_labels.csv")
data_file = file.read()
file.close()

# for final output file with labels
fout=open("test_w_labels_formatted.csv","wb")

# Get lat and lng
entries = re.split('\r', data_file)
entries_f = []
print len(entries)
for i in range(0,len(entries)):
	if (i<len(entries)-1):
		entries_f.append(entries[i] + entries[i+1].split('\n')[0])
		entries[i+1] = entries[i+1].split('\n')[1] 
for i in entries_f:
	fout.write(i+ '\n')
fout.close()
