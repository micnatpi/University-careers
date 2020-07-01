
# coding: utf-8


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


eta=pd.read_csv('../dati_4-4-2017_per_new_DB/ingressi_uscite.csv', sep=';', encoding='latin1')
eta.drop('Unnamed: 0', axis=1, inplace=True)

# In[3]:

eta['fascia'].replace(['RIC','PA','PO','SP','DR','BS','AR','TU','LC','RD','LR','LD'],
                     ['RIC','PA','PO','SP','PHD','BOR','AR','TU','LET','RD','LET','LET'],inplace=True)


eta2=eta[eta.fascia!='BOR']
eta2=eta2[eta2.fascia!='TU']



entry=pd.pivot_table(eta2, index=['inizio','genere'], values='eta_ingresso', aggfunc='count').reset_index()
entry['fascia']='TOT'

entry_ruolo=pd.pivot_table(eta2, index=['inizio','fascia','genere'], values='eta_ingresso', aggfunc='count').reset_index()


entry_tot=pd.concat([entry_ruolo, entry])


eta_reshaped=entry_tot.pivot_table(index=['fascia','inizio'],columns='genere', values='eta_ingresso',).fillna(0).reset_index()


ruolo=(list(set(eta_reshaped['fascia'].tolist())))*16
anni=(list(range(2001,2017)))*9

index=range(0,144)
empty=pd.DataFrame(index=index, columns=['inizio','fascia'])
empty['inizio']=anni
empty['fascia']=ruolo

eta_reshaped=pd.merge(empty,eta_reshaped, how='left').fillna('null')



eta_melted=pd.melt(eta_reshaped,id_vars=['inizio','fascia'],value_vars=['F','M'], var_name='genere')

eta_d=eta_melted.sort_values(['inizio','fascia','genere']).reset_index(drop=True)
eta_d=eta_d.rename(columns={'value':'numero'})


# Json completo
mydict = {}
for x in range(len(eta_d)):
    ruolo = eta_d.iloc[x,1]
    #print currentid
    eta=str(eta_d.iloc[x,0])
    genere=eta_d.iloc[x,2]
    numero=str(eta_d.iloc[x,3])
    #print valori
    if ruolo not in mydict:
        mydict.setdefault(ruolo, {})
        mydict[ruolo].setdefault('anno', [])
        mydict[ruolo].setdefault('series', [])
        m={'name':'M'}
        f={'name':'F'}
        mydict[ruolo]['series'].append(dict(m))
        mydict[ruolo]['series'].append(dict(f))
        mydict[ruolo]['series'][0].setdefault('data', [])
        mydict[ruolo]['series'][1].setdefault('data', [])
        mydict[ruolo]['anno'].append(eta)
        if genere=='M':
            mydict[ruolo]['series'][0]['data'].append(numero)
        else:
            mydict[ruolo]['series'][1]['data'].append(numero)
    else:
        if eta not in mydict[ruolo]['anno']:
            mydict[ruolo]['anno'].append(eta)
        if genere=='M':
            mydict[ruolo]['series'][0]['data'].append(numero)
        else:
            mydict[ruolo]['series'][1]['data'].append(numero)


with open('../data_csv/nuove_nomine_confronto_CORRETTO.json', 'w',) as fp:
    json.dump(mydict, fp, sort_keys=True, indent=4)
fp.close()


# In[39]:

len(mydict['TOT']['eta'])


# In[ ]:



