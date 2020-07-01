
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
from collections import OrderedDict
from collections import defaultdict
import operator
from operator import itemgetter


df=pd.read_csv('../dati_4-4-2017_per_new_DB/personale_ricerca_unipi_completo_flag_v2.csv', sep=';', encoding='latin1')

df.rename(columns={'fascia': 'ruolo'}, inplace=True)
df2=df[df.ruolo!='TU']
df2=df2[df2.anno>2000]
df2=df2[df2.anno<2018]
df2['ruolo'].replace(['RU','RD','LR','BS','BE','DR','SP','LD','LC','LR'],
                       ['RIC','RD','RIC','BOR','BOR','PHD','SP','LET','LET','LET',],inplace=True)

ruoli=pd.pivot_table(df2, index=['anno', 'struttura','ruolo', 'genere'], values='matricola', aggfunc='count').reset_index()
ruoli=ruoli.rename(columns={'matricola':'numero'})


# TUTTE LE VARIABILI
stem_ruoli_anno_genere=ruoli[ruoli.struttura.isin(["Dip. Ingegneria Civile E Industriale","Dip. Ingegneria Dell'Informazione", 
                               "Dip. Ingegneria Dell'Energia, Dei Sistemi, Del Territorio E Delle Costruzioni",
                              "Dip. Patologia Chirurgica, Medica, Molecolare E Dell'Area Critica",
                              "Dip. Medicina Clinica E Sperimentale", 
                               "Dip. Ricerca Traslazionale E Delle Nuove Tecnologia In Medicina E Chirurgia"])]

stem_ruoli_anno_genere=stem_ruoli_anno_genere[stem_ruoli_anno_genere.anno==2016]


stem_ruoli_anno_genere=stem_ruoli_anno_genere[stem_ruoli_anno_genere.ruolo.isin(['PA','PO','RD','RIC'])]


stem_ruoli_anno_genere['ruolo'].replace(['PA','PO','RD','RIC'],['3 PA','4 PO','1 RD','2 RIC'],inplace=True)


lista=["Dip. Ingegneria Civile E Industriale","Dip. Ingegneria Dell'Informazione", 
                               "Dip. Ingegneria Dell'Energia, Dei Sistemi, Del Territorio E Delle Costruzioni",
                              "Dip. Patologia Chirurgica, Medica, Molecolare E Dell'Area Critica",
                              "Dip. Medicina Clinica E Sperimentale", 
                               "Dip. Ricerca Traslazionale E Delle Nuove Tecnologia In Medicina E Chirurgia"]


for dip in lista:
    dipartimento=stem_ruoli_anno_genere[stem_ruoli_anno_genere['struttura']==dip]
    print(dip, len(dipartimento))
    filere=dipartimento.pivot_table(index=['anno','ruolo'],columns='genere', aggfunc='sum', values='numero').fillna(0).reset_index()
    
    filere['TOT']=filere['F']+filere['M']
    filere['Perc_F']=round(filere['F']/filere['TOT']*100,1)
    filere['Perc_M']=round(filere['M']/filere['TOT']*100,1)
    leak_melt=pd.melt(filere, id_vars=['ruolo'],value_vars=['Perc_M', 'Perc_F'])
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


            if genere=='Perc_M':
                mydict['series'][0]['data'].append(numero)
                mydict['series'][0]['name']='M'
            else:
                mydict['series'][1]['data'].append(numero)
                mydict['series'][1]['name']='F'
        else:

            if genere=='perc_M':
                mydict['series'][0]['data'].append(numero)
                mydict['series'][0]['name']='M'
            else:
                mydict['series'][1]['data'].append(numero)
                mydict['series'][1]['name']='F'
        
        nome=dip.replace(" ", "")

    with open('../data_csv/dipartimenti_CORRETTO/leak_%s.json' %nome, 'w' ) as fp:
        json.dump(mydict, fp, sort_keys=True,  indent=4, default=str)
    fp.close()




