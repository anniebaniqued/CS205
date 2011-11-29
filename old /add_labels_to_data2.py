import urllib2
import re

from xml.dom.minidom import parseString

# open data_combined.csv
file = open("data_combined2.csv")
data_file = file.read()
file.close()

# for final output file with labels
fout=open("data_combined_w_labels_2_2.csv","a")

# Get lat and lng
entries = re.split('\n', data_file)
for i in range(0,len(entries)):
    lat = entries[i].split(',')[0]
    lng = entries[i].split(',')[1]
    
    # download the file
    xml_file = urllib2.urlopen('http://nominatim.openstreetmap.org/reverse?lat='+lat+'&lon='+lng)
    xml_data = xml_file.read()
    xml_file.close()

    # parse the xml you downloaded
    dom = parseString(xml_data)

    # retrieve the first xml tag (<tag>data</tag>) that the parser finds with name tagName:
    ## try:
    ##     xmlCity = dom.getElementsByTagName('city')[0].toxml()
    ## except Exception:
    ##     xmlCity = 'None'
    ## try:
    ##     xmlState = dom.getElementsByTagName('state')[0].toxml()
    ## except Exception:
    ##     xmlState = 'None'
    try:
        xmlCountry = dom.getElementsByTagName('country')[0].toxml()
        xmlCountry=xmlCountry.split('<country>')[1].split('</country>')[0]
    except Exception:
        xmlCountry = 'None'

    # strip off the tag (<tag>data</tag>  --->   data):
    ## state=xmlState.replace('<state>','').replace('</state>','')
    ## city=xmlCity.replace('<city>','').replace('</city>','')

    fout.write(lat + ',' + lng + ',' + xmlCountry.encode('utf8') + '\n') 

fout.close()
