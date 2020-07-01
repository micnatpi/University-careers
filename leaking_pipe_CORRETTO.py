
# coding: utf-8

# In[1]:

import pandas as pd
import numpy as np
#import matplotlib.pyplot as plt
#%matplotlib inline
pd.set_option('max_columns', 300)
pd.set_option('max_rows', 10000)
#elimino i warning
import warnings
warnings.filterwarnings("ignore")
import json
import datetime, time


# In[2]:

ruoli=pd.read_csv('../dati_4-4-2017_per_new_DB/personale_ricerca_unipi_completo_flag_v2.csv', sep=';', encoding='latin1')

ruoli=ruoli[ruoli['fascia'] != 'TU']


ruoli['fascia'].replace(['RU','RD','LR','BS','BE','DR','SP','LD','LC','LR'],
                       ['RIC','RD','RIC','BOR','BOR','PHD','SP','LET','LET','LET',],inplace=True)


leak=ruoli[ruoli['fascia'].isin(['PHD', 'AR','RD','RIC','PA','PO'])]


leak=leak[leak['anno']>2011]
leak=leak[leak['anno']<2015]


# In[7]:

leaking=pd.pivot_table(leak,index='fascia', columns='genere', aggfunc='count', values='anno').reset_index()


leaking['perc_m']=round((leaking['M']/(leaking['M']+leaking['F']))*100,1)
leaking['perc_f']=round((leaking['F']/(leaking['M']+leaking['F']))*100,1)
leaking


leak_fin=leaking.copy()
leak_fin['fascia'].replace(['PHD', 'AR','RD','RIC','PA','PO'],['1 PHD', '2 AR','3 RD','4 RIC','5 PA','6 PO'],inplace=True)

leak_fin.sort(['fascia'], ascending=[True], inplace=True)
leak_fin=leak_fin.reset_index(drop=True)

# In[11]:

leak_melt=pd.melt(leak_fin, id_vars=['fascia'],value_vars=['perc_m', 'perc_f'])

# Json completo
mydict = {}
for x in range(len(leak_melt)):
    ruolo = leak_melt.iloc[x,0]
    #print currentid
    genere=leak_melt.iloc[x,1]
    numero=str(leak_melt.iloc[x,2])

    
    if ruolo not in mydict:
        mydict.setdefault('ruoli', [])
        mydict.setdefault('series', [{},{}])
        mydict['series'][0].setdefault('data', [])

        mydict['series'][1].setdefault('data', [])

        if ruolo not in mydict['ruoli']:
            mydict['ruoli'].append(ruolo)
            
        
        if genere=='perc_m':
            mydict['series'][0]['data'].append(numero)
            mydict['series'][0]['name']='M'
        else:
            mydict['series'][1]['data'].append(numero)
            mydict['series'][1]['name']='F'
    else:

        if genere=='perc_m':
            mydict['series'][0]['data'].append(numero)
            mydict['series'][0]['name']='M'
        else:
            mydict['series'][1]['data'].append(numero)
            mydict['series'][1]['name']='F'
        



with open('../data_csv/leak_corretto.json', 'w',) as fp:
    json.dump(mydict, fp, sort_keys=True,  indent=4, default=str)
fp.close()




