import pandas as pd
import json
from pandas.io.json import json_normalize 

with open('bus_stops.json', encoding='cp850') as f:
    data = json.load(f)

results = data['results']

l = []

for i in range(0, len(results)):
    
    for j in range(0, len(results[i]['operators'])):
        
        for k in range(0, len(results[i]['operators'][j]['routes'])):
            
            n = []
            n.append(results[i]['stopid'])
            n.append(results[i]['displaystopid'])
            n.append(results[i]['shortname'])
            n.append(results[i]['fullname'])
            n.append(results[i]['latitude'])
            n.append(results[i]['longitude'])
            n.append(results[i]['operators'][j]['name'])
            n.append(results[i]['operators'][j]['operatortype'])
            n.append(results[i]['operators'][j]['routes'][k])
            l.append(n)


df = pd.DataFrame(l)
df.columns = ['stopid', 'displaystopid', 'shortname', 'fullname', 'latitude', 'longitude', 'name', 'operatortype', 'route']
df.to_csv('bus_stops.csv')
