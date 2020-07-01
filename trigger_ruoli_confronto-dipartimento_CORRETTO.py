
# coding: utf-8

# In[2]:


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
from collections import OrderedDict
from collections import defaultdict
import operator
from operator import itemgetter


# In[3]:

df=pd.read_csv('../dati_4-4-2017_per_new_DB/personale_ricerca_unipi_completo_flag_v2.csv', sep=';', encoding='latin1')

df.rename(columns={'fascia': 'ruolo'}, inplace=True)


df2=df[df.ruolo.isin(['RD', 'RIC', 'PA', 'PO'])]

ruoli=pd.pivot_table(df2, index=['struttura','anno', 'ruolo', 'genere'], values='matricola', aggfunc='count').reset_index()

ruoli=ruoli[ruoli.struttura.isin(["Dip. Ingegneria Civile E Industriale","Dip. Ingegneria Dell'Informazione", 
                               "Dip. Ingegneria Dell'Energia, Dei Sistemi, Del Territorio E Delle Costruzioni",
                              "Dip. Patologia Chirurgica, Medica, Molecolare E Dell'Area Critica",
                              "Dip. Medicina Clinica E Sperimentale", 
                               "Dip. Ricerca Traslazionale E Delle Nuove Tecnologia In Medicina E Chirurgia"])]

ruoli=ruoli[ruoli.anno>2000]
ruoli=ruoli[ruoli.anno<2018]
ruoli['ruolo'].replace(['RU','RD','LR','BS','BE','DR','SP','LD','LC','LR'],
                       ['RIC','RD','RIC','BOR','BOR','PHD','SP','LET','LET','LET',],inplace=True)


ruoli=ruoli.rename(columns={'matricola':'numero'})


totale_ruoli=ruoli.groupby(by=['struttura','anno','genere']).sum().reset_index()
totale_ruoli['ruolo']='TOT'

ruolit=pd.concat([ruoli,totale_ruoli]) 
ruolit=ruolit[['struttura','ruolo', 'anno', 'genere', 'numero']]

ruoli_reshaped=ruolit.pivot_table(index=['struttura','ruolo','anno'],columns='genere', values='numero',).fillna(0).reset_index()

ruoli_reshaped.F = ruoli_reshaped.F.astype(int)
ruoli_reshaped.M = ruoli_reshaped.M.astype(int)

ruoli_reshaped['T_ruolo']=ruoli_reshaped['F']+ruoli_reshaped['M']
ruoli_reshaped['Perc_F']=round((ruoli_reshaped['F']/ruoli_reshaped['T_ruolo'])*100,1)
ruoli_reshaped['Perc_M']=round((ruoli_reshaped['M']/ruoli_reshaped['T_ruolo'])*100,1)


ruoli_melted=pd.melt(ruoli_reshaped,id_vars=['struttura','ruolo','anno'],value_vars=['F','M','T_ruolo','Perc_M','Perc_F'])

ruoli_melted=ruoli_melted.sort_values(['struttura','anno','ruolo','genere']).reset_index(drop=True)

ruoli_d=ruoli_melted.sort_values(['struttura','ruolo','anno','genere']).reset_index(drop=True)


ruoli_d=ruoli_d.rename(columns={'value':'numero'})


ruoli_d=pd.pivot_table(ruoli_d,index=['struttura','ruolo','anno'], columns='genere',values='numero').reset_index()


ruolo=(list(set(ruoli_d['ruolo'].tolist())))*6*17
anni=(list(range(2001,2018)))*6*5
struttura=(list(set(ruoli_d['struttura'].tolist())))*5*17
struttura.sort()

index=range(0,510)
empty=pd.DataFrame(index=index, columns=['struttura','ruolo', 'anno']).fillna(0)

empty['ruolo']=ruolo
empty['anno']=anni
empty['struttura']=struttura
empty=empty.sort_values(by=['struttura','ruolo','anno']).reset_index(drop=True)

prova=pd.merge(empty,ruoli_d, how='left')

prova2=prova[['struttura','anno','ruolo', 'F', 'M']]
prova2['F']=prova2['F'].astype(str).str.replace('nan', 'null')
prova2['M']=prova2['M'].astype(str).str.replace('nan', 'null')
# prova2

ruoli_melt=pd.melt(prova2, id_vars=['struttura','anno','ruolo'], value_vars=['F','M'], var_name='genere', value_name='numero')


ruoli_def=ruoli_melt.copy()

# Json completo per linee di trend

lista=["Dip. Ingegneria Civile E Industriale","Dip. Ingegneria Dell'Informazione", 
                               "Dip. Ingegneria Dell'Energia, Dei Sistemi, Del Territorio E Delle Costruzioni",
                              "Dip. Patologia Chirurgica, Medica, Molecolare E Dell'Area Critica",
                              "Dip. Medicina Clinica E Sperimentale", 
                               "Dip. Ricerca Traslazionale E Delle Nuove Tecnologia In Medicina E Chirurgia"]

for dip in lista:
    dipartimento=ruoli_def[ruoli_def['struttura']==dip]
    print(dip, len(dipartimento))
    mydict={}

    for x in range(len(dipartimento)):
        ruolo = dipartimento.iloc[x,2]
        #print currentid
        anno=str(int(dipartimento.iloc[x,1]))
        genere=dipartimento.iloc[x,3]
        numero=str(dipartimento.iloc[x,4])
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
    nome=dip.replace(" ", "")

    with open('../data_csv/dipartimenti_CORRETTO/%s_TOT.json' %nome, 'w') as fp:
        json.dump(mydict, fp,   indent=4)
    fp.close()



