
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


df2=df2[df2.ruolo.isin(['RD', 'RIC', 'PA', 'PO'])]


ruoli=pd.pivot_table(df2, index=['anno', 'struttura','ruolo', 'genere'], values='matricola', aggfunc='count').reset_index()
ruoli=ruoli.rename(columns={'matricola':'numero'})

# TUTTE LE VARIABILI
stem_ruoli_anno_genere=ruoli[ruoli.struttura.isin(["Dip. Ingegneria Civile E Industriale","Dip. Ingegneria Dell'Informazione", 
                               "Dip. Ingegneria Dell'Energia, Dei Sistemi, Del Territorio E Delle Costruzioni",
                              "Dip. Patologia Chirurgica, Medica, Molecolare E Dell'Area Critica",
                              "Dip. Medicina Clinica E Sperimentale", 
                               "Dip. Ricerca Traslazionale E Delle Nuove Tecnologia In Medicina E Chirurgia"])]

# AGGREGO SU RUOLO ANNO E GENERE
ruoli_anno_genere=stem_ruoli_anno_genere.groupby(by=['ruolo','anno','genere']).sum().reset_index()
ruoli_anno_genere['struttura']='All_dip'

# AGGREGO SU ANNO E GENERE
anno_genere=stem_ruoli_anno_genere.groupby(by=['anno','genere']).sum().reset_index()
anno_genere['struttura']='All_dip'
anno_genere['ruolo']='All_ruolo'

# # # CALCOLO LE PERCENTUALI SUI TOTALI DI DIPARTIMENTO-RUOLO-ANNO

reshape_dip=stem_ruoli_anno_genere.pivot_table(index=['struttura','ruolo','anno'],columns='genere', values='numero',).fillna(0).reset_index()
reshape_dip.F = reshape_dip.F.astype(int)
reshape_dip.M = reshape_dip.M.astype(int)
reshape_dip['TOT_dip']=reshape_dip['M']+reshape_dip['F']
reshape_dip['Perc_M']=round(reshape_dip['M']/reshape_dip['TOT_dip']*100,1)
reshape_dip['Perc_F']=round(reshape_dip['F']/reshape_dip['TOT_dip']*100,1)


ruolifin=reshape_dip.copy()

# # GENERA JSON PER HIGHCHARTS


lista=["Dip. Ingegneria Civile E Industriale","Dip. Ingegneria Dell'Informazione", 
                               "Dip. Ingegneria Dell'Energia, Dei Sistemi, Del Territorio E Delle Costruzioni",
                              "Dip. Patologia Chirurgica, Medica, Molecolare E Dell'Area Critica",
                              "Dip. Medicina Clinica E Sperimentale", 
                               "Dip. Ricerca Traslazionale E Delle Nuove Tecnologia In Medicina E Chirurgia"]

for dip in lista:
    dipartimento=ruolifin[ruolifin['struttura']==dip]
    print(dip, len(dipartimento))
    mydict={}

    for x in range(len(dipartimento)):
#         dip=dipartimento.iloc[x,0]
        anno=str(dipartimento.iloc[x,2])
        ruolo=dipartimento.iloc[x,1]
        F=float(dipartimento.iloc[x,3])
        M=float(dipartimento.iloc[x,4])
        perc_F=dipartimento.iloc[x,7]
        perc_M=dipartimento.iloc[x,6]


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

  
    nome=dip.replace(" ", "")

    with open('../data_csv/dipartimenti_CORRETTO/treemap_dip_anno_%s.json' %nome, 'w') as fp:
        json.dump(mydict, fp, allow_nan=True,  indent=4)
    fp.close()


