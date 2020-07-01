
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


df=pd.read_csv('../dati_4-4-2017_per_new_DB/personale_ricerca_unipi_completo_flag_v2.csv', sep=';', encoding='latin1')
df.rename(columns={'fascia': 'ruolo'}, inplace=True)

ruoli=pd.pivot_table(df, index=['anno', 'ruolo', 'genere'], values='matricola', aggfunc='count').reset_index()

ruoli=ruoli[ruoli.ruolo!='TU']
ruoli=ruoli[ruoli.anno>2000]
ruoli=ruoli[ruoli.anno<2018]
ruoli['ruolo'].replace(['RU','RD','LR','BS','BE','DR','SP','LD','LC','LR'],
                       ['RIC','RD','RIC','BOR','BOR','PHD','SP','LET','LET','LET',],inplace=True)

ruoli=ruoli.rename(columns={'matricola':'numero'})



totale_ruoli=ruoli.groupby(by=['anno','genere']).sum().reset_index()
totale_ruoli['ruolo']='TOT'

ruolig=ruoli.groupby(by=['ruolo','anno','genere']).sum().reset_index()


ruolit=pd.concat([ruolig,totale_ruoli]) 
ruolit=ruolit[['ruolo', 'anno', 'genere', 'numero']]

ruoli_reshaped=ruolit.pivot_table(index=['ruolo','anno'],columns='genere', values='numero',).fillna(0).reset_index()

ruoli_reshaped.F = ruoli_reshaped.F.astype(int)
ruoli_reshaped.M = ruoli_reshaped.M.astype(int)

ruoli_reshaped['T_ruolo']=ruoli_reshaped['F']+ruoli_reshaped['M']
ruoli_reshaped['Perc_F']=round((ruoli_reshaped['F']/ruoli_reshaped['T_ruolo'])*100,1)
ruoli_reshaped['Perc_M']=round((ruoli_reshaped['M']/ruoli_reshaped['T_ruolo'])*100,1)


ruoli_melted=pd.melt(ruoli_reshaped,id_vars=['ruolo','anno'],value_vars=['F','M','T_ruolo','Perc_M','Perc_F'])


ruoli_melted=ruoli_melted.sort_values(['anno','ruolo','genere']).reset_index(drop=True)

ruoli_d=ruoli_melted.sort_values(['ruolo','anno','genere']).reset_index(drop=True)

ruoli_d=ruoli_d.rename(columns={'value':'numero'})

ruoli_d=pd.pivot_table(ruoli_d,index=['ruolo','anno'], columns='genere',values='numero').reset_index()


ruolo=(list(set(ruoli_d['ruolo'].tolist())))*17
anni=(list(range(2001,2018)))*10
# genere=['M','F']*17*9

index=range(0,170)
empty=pd.DataFrame(index=index, columns=['ruolo', 'anno']).fillna(0)
empty['ruolo']=ruolo
empty['anno']=anni

ruolinew=pd.merge(empty,ruoli_d, how='left')


ruoli_melt=pd.melt(ruolinew, id_vars=['ruolo','anno'], value_vars=['F','M'], var_name='genere', value_name='numero')

cols=ruoli_melt.columns.tolist()
cols=['anno', 'ruolo', 'genere', 'numero']
ruolinew=ruoli_melt[cols]


ruoli_def=ruolinew.sort_values(by=['anno', 'ruolo', 'genere']).reset_index(drop=True)


ruoli_def['numero']=ruoli_def['numero'].astype(str).str.replace('nan', 'null')


# Json completo per linee di trend
mydict = {}
for x in range(len(ruoli_def)):
    ruolo = ruoli_def.iloc[x,1]
    #print currentid
    anno=str(int(ruoli_def.iloc[x,0]))
    genere=ruoli_def.iloc[x,2]
    numero=str(ruoli_def.iloc[x,3])
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
        mydict[ruolo]['anno'].append(anno)
        if genere=='M':
            mydict[ruolo]['series'][0]['data'].append(numero)
        if genere=='F':
            mydict[ruolo]['series'][1]['data'].append(numero)
    else:
        if anno not in mydict[ruolo]['anno']:
            mydict[ruolo]['anno'].append(anno)
        if genere=='M':
            mydict[ruolo]['series'][0]['data'].append(numero)
        if genere=='F':
            mydict[ruolo]['series'][1]['data'].append(numero)
        


with open('../data_csv/ruoli_confronto_CORRETTO.json', 'w',) as fp:
    json.dump(mydict, fp, sort_keys=True, indent=4)
fp.close()


