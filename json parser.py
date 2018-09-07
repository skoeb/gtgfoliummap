# -*- coding: utf-8 -*-
"""
Created on Wed Jan 31 17:26:03 2018

@author: skoebric

How to add countries to the Greening the Grid map, a simple guide for the novice coder:
1) update the 'whereweworklist.csv' with new entries!
2) update 'os.chdir' below to represent the path to the github project folder on your computer
3) run this script!
4) commit changes to github
    
if getting errors: make sure country names/spelling are consistent with 'allcountries.geojson', 
check the google sheet for spelling errors: https://docs.google.com/spreadsheets/d/1-Hh_36BxhGH2TgKMuZvfj1nHCyIx1rSQ3CqAOc2fm74/edit?usp=sharing

"""

import json
import pandas as pd
import os

#set working directory to github folder, change if on mac / other computer
os.chdir("/Users/skoebric/Dropbox/GitHub/gtgfoliummap/geometry/")

allcountriesjson = "/Users/skoebric/Dropbox/GitHub/gtgfoliummap/geometry/world.geojson"

#opens the json with outlines of all countries, creates 'dump' which contains a list of all countries geography/properties
openfile = open(allcountriesjson, 'r')
json_input = json.load(openfile)
dump = json_input['features']

#%%
#pulls csv from static google sheet location, passes it to df
CSVURL = "https://docs.google.com/spreadsheets/d/e/2PACX-1vRkObK4sgJUYpz4XfHS3KG8teVYY6aWCO-efLM6Qrk0GkP_MNmsx5MLTcSo0QDRhlorEr1GSvp7Mc2F/pub?gid=0&single=true&output=csv"
import requests
import io

data = requests.get(CSVURL)
df = pd.read_csv(io.StringIO(data.text))

#%%
#checks the df and creates two lists, one for 'pilot projects', one for 'other assistance'
#and one dict 'whereweworkdictlist' with a list of properties for each 
whereweworkindexed = df.set_index('Country')
whereweworkindexed['Name'] = whereweworkindexed.index
#whereweworkdictlist = wherewework.to_dict(orient = 'records')

projects = list(whereweworkindexed['Name'])
#otherbens = list(whereweworkindexed[whereweworkindexed['Assistance Type'] == 'Other Assistance']['Name'])
#%%     
#create 'whereweworkout' with the geography and properties for each country in lists
whereweworkout = []
for x in dump:
#    if (x['properties']['name']) in otherbens:
#        y = whereweworkindexed.loc[x['properties']['name']].dropna()
#        x['properties'] = y.to_dict()
#        whereweworkout.append(x)
    if (x['properties']['NAME']) in projects:
        y = whereweworkindexed.loc[x['properties']['NAME']].dropna()
        x['properties'] = y.to_dict()
        whereweworkout.append(x)

#%%
#export geojson
outdict = {"type": "FeatureCollection",
                     "features":whereweworkout}


#save the pilotprojectsout list to the 'wherewework.geojson' file
outfile = "/Users/skoebric/Dropbox/GitHub/gtgfoliummap/geometry/wherewework.geojson"
with open(outfile, 'w') as outpath:
    json.dump(outdict, outpath)



