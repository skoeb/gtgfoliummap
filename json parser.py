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
import geopandas as gpd

allcountriesjson = "geometry/world.geojson"

allcountries = gpd.read_file(allcountriesjson)

allcountries.loc[allcountries['ADMIN'] == 'Brunei', 'ADMIN'] = 'Brunei Darussalam'
allcountries.loc[allcountries['ADMIN'] == 'Myanmar', 'ADMIN'] = 'Burma'
allcountries.loc[allcountries['ADMIN'] == 'Kyrgyzstan', 'ADMIN'] = 'Kyrgyz Republic'

#%%
#pulls csv from static google sheet location, passes it to df
CSVURL = "https://docs.google.com/spreadsheets/d/e/2PACX-1vRkObK4sgJUYpz4XfHS3KG8teVYY6aWCO-efLM6Qrk0GkP_MNmsx5MLTcSo0QDRhlorEr1GSvp7Mc2F/pub?gid=0&single=true&output=csv"
import requests
import io

data = requests.get(CSVURL, verify = False)
csvdf = pd.read_csv(io.StringIO(data.text))
csvdf = csvdf.rename({'Country':'ADMIN'}, axis = 'columns')

#%%
#merge geodata with google sheet data
countrygdf = pd.merge(allcountries[['ADMIN', 'geometry']], csvdf, on = ['ADMIN'], how = 'inner')
countrygdf = countrygdf.fillna('missing')

#%%

#test to make sure all geometries mapped
if len(csvdf) != len(countrygdf):
    for i in list(csvdf['ADMIN']):
        if i not in list(countrygdf['ADMIN']):
            print(i, 'not found in gdf!')


#%%

def countryjsoner(row):
    country = row['ADMIN']

    introtext = f"The USAID-NREL Partnership is actively working in {country} through the following toolkits: \n"

    platformtext = '<ul>'
    if row['Greening The Grid Link'] != 'missing':
        link = row['Greening The Grid Link']
        text = row['Greening The Grid Link Name']
        platformtext += f"<li><a href='{link}' target='_blank'> {text} </a></li>\n"
    if row['RE Explorer Link'] != 'missing':
        link = row['RE Explorer Link']
        text = row['RE Explorer Link Name']
        platformtext += f"<li><a href='{link}' target='_blank'> {text} </a></li>\n"
    if row['I-JEDI Link'] != 'missing':
        link = row['I-JEDI Link']
        text = row['I-JEDI Link Name']
        platformtext += f"<li><a href='{link}' target='_blank'> {text} </a></li>\n"
    if row['Resilient Energy Platform Link'] != 'missing':
        link = row['Resilient Energy Platform Link']
        text = row['Resilient Energy Platform Link Name']
        platformtext += f"<li><a href='{link}' target='_blank'> {text} </a></li>\n"

    platformtext = platformtext[:-2]
    platformtext += '</ul>'

    row_ = countrygdf.loc[countrygdf['ADMIN'] == country]
    geojson = folium.GeoJson(row_, highlight_function = style_function, style_function = style_function)
    popup = folium.Popup(f"{introtext}<br>"
                         "<br>"
                         f"{platformtext}", max_width=300)
    popup.add_to(geojson)
    geojson.add_to(layer)


import folium
from folium import plugins


m = folium.Map(width = '100%', height = 800, location = (20,5),zoom_start = 3,
               no_wrap=True,max_bounds=True, min_zoom=3, tiles="MapBox Bright")

plugins.ScrollZoomToggler().add_to(m)

layer = folium.FeatureGroup(name='countries', show = True)

style_function = lambda feature: {
                       'fillColor': '#005DA3',
                       'fillOpacity' : 0.7,
                       'color': '#000000',
                       'weight':0.2
                       }

countrygdf.apply(countryjsoner, axis = 1)

m.add_child(layer)

m.save("index.html")

##%%
#m = folium.Map(width = '100%', height = 800, location = (20,5),zoom_start = 3,
#               no_wrap=True,max_bounds=True, min_zoom=3, tiles="MapBox Bright")
#
#plugins.ScrollZoomToggler().add_to(m)
#
#style_function = lambda x: {'fillColor': '#73ad02',
#                            'color': '#73ad02',
#                            'weight':1,
#                            }
#
#def countryjsoner(row):
#    country = row['Name']
#    tk = row['Toolkit']
#    link = row['Link']
#    row_ = all_json.loc[all_json['Name'] == country]
#    geojson = folium.GeoJson(row_, highlight_function = style_function, style_function = style_function)
#    popup = folium.Popup(f"<b>Country:</b> {country}<br>"
#                         f"<b>Toolkit:</b> {tk}<br>"
#                         f'<a href="{link}" target="_blank"> Click For Country Page </a>')
#    popup.add_to(geojson)
#    geojson.add_to(m)
#
#all_json.apply(countryjsoner, axis = 1)
#m.save("index.html")