
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



ruoli=pd.read_csv('../dati_4-4-2017_per_new_DB/personale_ricerca_unipi_completo_flag_v2.csv', sep=';', encoding='latin1')

ruoli.rename(columns={'fascia': 'ruolo'}, inplace=True)


# calcolo i numeri totali per il grafico iniziale
ultimo=ruoli[ruoli.anno==2017]

ruoli=ruoli[ruoli.ruolo!='TU']
ruoli=ruoli[ruoli.anno>2000]
ruoli=ruoli[ruoli.anno<2018]


ruoli['ruolo'].replace(['RU','RD','LR','BS','BE','DR','SP','LD','LC','LR'],
                       ['RIC','RD','RIC','BOR','BOR','PHD','SP','LET','LET','LET',],inplace=True)

totale_ruoli=pd.pivot_table(ruoli, index=['anno','genere'], values='matricola', aggfunc='count').reset_index()
totale_ruoli['ruolo']='TOT'


ruoli_agg=pd.pivot_table(ruoli, index=['ruolo','anno','genere'], values='matricola', aggfunc='count').reset_index()

ruoli2=pd.concat([ruoli_agg,totale_ruoli]) 

ruoli_reshaped=ruoli2.pivot_table(index=['ruolo','anno'],columns='genere', values='matricola',).fillna(0).reset_index()


ruolo=(list(set(ruoli_reshaped['ruolo'].tolist())))*17
anni=(list(range(2001,2018)))*10
# genere=['M','F']*17*9

index=range(0,170)
empty=pd.DataFrame(index=index, columns=['ruolo', 'anno']).fillna(0)
empty['ruolo']=ruolo
empty['anno']=anni
        

ruolinew=pd.merge(empty,ruoli_reshaped, how='left').fillna(0)

ruolinew['T_ruolo']=(ruolinew['F']+ruolinew['M'])
ruolinew['Perc_F']=round((ruolinew['F']/ruolinew['T_ruolo'])*100,1).fillna(0)
ruolinew['Perc_M']=round((ruolinew['M']/ruolinew['T_ruolo'])*100,1).fillna(0)

ruolinew=ruolinew[ruolinew.ruolo!='TOT']

# Create JSON
mydict={}

#         mydict.setdefault(anno, {})
#         mydict[anno].setdefault('data',[])

for x in range(len(ruolinew)):
    ruolo=ruolinew.iloc[x,0]
    anno= str(ruolinew.iloc[x,1])
    F=ruolinew.iloc[x,2]
    M=ruolinew.iloc[x,3]
    perc_F=ruolinew.iloc[x,5]
    perc_M=ruolinew.iloc[x,6]
    

    
    if anno not in mydict:
        mydict.setdefault(anno, {})
        mydict[anno].setdefault('data',[])

      
        d1={'id':ruolo, 'name':ruolo, 'borderWidth':3, 'borderColor': 'white'}
        d2={'name':'F', 'parent':ruolo, 'value':F, 'color':'#90477B','Perc':perc_F}
        d3={'name':'M', 'parent':ruolo, 'value':M, 'color':'#105180','Perc':perc_M}
        mydict[anno]['data'].append(d1)
        mydict[anno]['data'].append(d2)
        mydict[anno]['data'].append(d3)
        
    else:
        d1={'id':ruolo, 'name':ruolo, 'borderWidth':3, 'borderColor': 'white'}
        d2={'name':'F', 'parent':ruolo, 'value':F, 'color':'#90477B','Perc':perc_F}
        d3={'name':'M', 'parent':ruolo, 'value':M, 'color':'#105180','Perc':perc_M}
        mydict[anno]['data'].append(d1)
        mydict[anno]['data'].append(d2)
        mydict[anno]['data'].append(d3)   
        


with open('../data_csv/treemap_anni_CORRETTO.json', 'w',) as fp:
    json.dump(mydict, fp, sort_keys=True, default=str,indent=4)
fp.close()
