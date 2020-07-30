import json

import pandas as pd

with open('bus_stops.json', encoding='cp850') as f:
    data = json.load(f)

results = data['results']

l = []

for i in range(0, len(results)):
    
    for j in range(0, len(results[i]['operators'])):
        
        for k in range(0, len(results[i]['operators'][j]['routes'])):
            
            n = [results[i]['stopid'], results[i]['displaystopid'], results[i]['shortname'], results[i]['fullname'],
                 results[i]['latitude'], results[i]['longitude'], results[i]['operators'][j]['name'],
                 results[i]['operators'][j]['operatortype'], results[i]['operators'][j]['routes'][k]]
            l.append(n)


df = pd.DataFrame(l)
df.columns = ['stopid', 'displaystopid', 'shortname', 'fullname', 'latitude', 'longitude', 'name', 'operatortype', 'route']
df.to_csv('bus_stops.csv')
