
# coding: utf-8

# In[1]:


import pandas as pd
import numpy as np
pd.set_option('max_columns', 300)
pd.set_option('max_rows', 10000)
#elimino i warning
import warnings
warnings.filterwarnings("ignore")
import json
import datetime, time
from collections import OrderedDict
from collections import defaultdict
import operator
from operator import itemgetter




df=pd.read_csv('../dati_4-4-2017_per_new_DB/personale_ricerca_unipi_completo_flag_v3.csv', sep=';')

df.rename(columns={'fascia': 'ruolo'}, inplace=True)



rat=pd.read_csv('../dati_4-4-2017_per_new_DB/ratings_2016_fin.csv', sep=';', encoding='utf-8')

rat['Cognome e Nome']=rat.COGNOME.astype(str).str.cat(rat.NOME.str.title(), sep=' ')
rat=rat[['Cognome e Nome', 'Struttura', 'AREA_SET', 'anno', 'rating']]


df2=pd.merge(rat, df[['Cognome_Nome','Matricola','Struttura','Genere']], right_on=['Cognome_Nome','Struttura'], left_on=['Cognome e Nome','Struttura'],how='left')
df2=df2.drop_duplicates(['Cognome e Nome'], take_last=True)
df2=df2[['Cognome e Nome','Matricola','Struttura','AREA_SET','anno','Genere', 'rating']]


rating2=pd.pivot_table(df2,index=['Struttura','Genere'], values='rating', aggfunc='mean').reset_index()
rating2['rating']=rating2['rating'].round(2)


# Json completo
mydict = {}
for x in range(len(rating2)):
    dip = rating2.iloc[x,0]
    genere=rating2.iloc[x,1]
    rating=float(rating2.iloc[x,2])
    mydict.setdefault('codice', [])
    mydict.setdefault('series', [{},{}])
    mydict['series'][0].setdefault('data', [])
    mydict['series'][1].setdefault('data', [])

    if dip not in mydict['codice']:
        mydict['codice'].append(dip)            

    if genere=='M':
        mydict['series'][0]['data'].append(rating)
        mydict['series'][0]['name']='M'
    else:
        mydict['series'][1]['data'].append(rating)
        mydict['series'][1]['name']='F'
      


with open('../data_csv/rating2016_CORRETTO.json', 'w', encoding='utf-8') as fp:
    json.dump(mydict, fp, sort_keys=True,  indent=4)
fp.close()
