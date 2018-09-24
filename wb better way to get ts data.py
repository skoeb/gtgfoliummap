#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Sep 10 14:27:49 2018

@author: skoebric
"""

import wbdata as wb
import datetime
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

daterange = (datetime.datetime(1990, 1, 1), datetime.datetime(2017, 12, 31))

allcountries = wb.get_data('4.1_SHARE.RE.IN.ELECTRICITY',
                           data_date = daterange,
                           pandas = True)

allcountries = allcountries.reset_index()

phl = allcountries.loc[allcountries['country'] == 'Philippines']
phl = phl[['date','value']]
phl.date = pd.to_datetime(phl.date)
phl.set_index('date',inplace = True)
phl.dropna(inplace = True)
phl.sort_index(ascending = True, inplace = True)
phlseries = phl['value']

#from statsmodels.graphics.tsaplots import plot_acf
#
#plot_acf(phl, alpha = 1)

#fig, ax = plt.subplots(figsize=(12, 8))
#ax = phlseries.ix['1990':].plot(ax=ax,label='Trend',color='#0000FF')


from statsmodels.tsa.arima_model import ARIMA
arm = [1]
ma = [1,0.5]
mod = ARIMA(phl, order=(1,1,0))
res = mod.fit()
#res.plot_predict(start='2016-01-01', end='2030-01-01', alpha = .8, plot_insample = True, dynamic = False)
test = res.conf_int()

pred = res.predict(start='1995-01-01', end='2030-01-01')
pred.name = 'pred_diff'
phl = pd.concat([pred, phl], axis = 1)
phl = phl.fillna(method = 'ffill')
phl.loc['1990':'2015', 'pred_diff'] = 0


cumullist = []
def cumulrowgetter(row):
    cumullist.append(row['pred_diff'])
    return sum(cumullist)

phl['total_diff'] = phl.apply(cumulrowgetter, axis = 1)
phl['forecast'] = phl['value'] + phl['total_diff']

prev = 1
def RPSapplier(row):
    global prev
    year = row.name
    if year <= pd.to_datetime('2020-01-01'):
        prev = row['forecast']
        return(prev)
    elif year > pd.to_datetime('2020-01-01'):
        prev = prev + 1
        return(prev)
    
    
phl['RPS'] = phl.apply(RPSapplier, axis = 1)

phl['Historical Penetration'] = phl['forecast']
phl.loc['2021':, 'Historical Penetration'] = None
phl['Projection with RPS'] = phl['RPS']
phl.loc[:'2019', 'Projection with RPS'] = None
phl['Projection without RPS'] = phl['forecast']
phl.loc[:'2019', 'Projection without RPS'] = None
phlout = phl[['Historical Penetration','Projection with RPS','Projection without RPS']]



sns.set_style('darkgrid')
fig, ax = plt.subplots(figsize = (9,4))
ax.plot(phl['Historical Penetration'], color = '#06387a')
ax.plot(phl['Projection with RPS'], linestyle = '--', color = '#2cb602')
ax.plot(phl['Projection without RPS'], linestyle = '--', color = '#ff8f31')
ax.set_yticks(range(0,50,5))
ax.set_xticklabels(range(1990,2035,5))
ax.set_xlabel('Year', size = 14)
ax.set_ylabel('Percent Renewable Electricity', size = 14)
ax.set_title('Penetration of Renewables in Philippines Electricity Mix', size = 16)
plt.annotate('Source: World Bank Indicator 4.1_SHARE.RE.IN.ELECTRICITY. Projection using ARIMA(1,1,0) model between 2016-2030',
             (0,0), (0, 12), xycoords='axes fraction', textcoords='offset points', va='top', size = 9)
ax.legend()
plt.tight_layout()
