
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



eta=pd.read_csv('../dati_4-4-2017_per_new_DB/ingressi_uscite.csv', sep=';', encoding='latin1')
eta.drop('Unnamed: 0', axis=1, inplace=True)
eta['fascia'].replace(['RIC','PA','PO','SP','DR','BS','AR','TU','LC','RD','LR','LD'],
                     ['RIC','PA','PO','SP','PHD','BOR','AR','TU','LET','RD','LET','LET'],inplace=True)


eta2=eta[eta['fascia'].isin(['PHD','AR', 'RD', 'RIC','LR', 'PA', 'PO'])]

carriera=pd.DataFrame()
carriera['min']=eta2.groupby(['fascia','genere'])['eta_ingresso'].min()
carriera['q1']=eta2.groupby(['fascia','genere'])['eta_ingresso'].quantile(q=0.25, interpolation='midpoint')
carriera['median']=eta2.groupby(['fascia','genere'])['eta_ingresso'].quantile(q=0.50, interpolation='midpoint')
carriera['q3']=eta2.groupby(['fascia','genere'])['eta_ingresso'].quantile(q=0.75, interpolation='midpoint')
carriera['max']=eta2.groupby(['fascia','genere'])['eta_ingresso'].max()
carriera=carriera.reset_index()


POS=[('PHD',1), ('AR',2),('RD',3),('RIC',4),('PA',5),('PO',6)]
posizione=pd.DataFrame(POS, columns=('fascia','rank'))

carriera2=pd.merge(carriera, posizione, on='fascia', how='inner')

carriera2=carriera2.sort_values(by='rank', ascending=[True]).reset_index(drop=True)

carriera2['key']= carriera2["rank"].astype(str) + ' ' + carriera2["fascia"].astype(str) + ' ' + carriera2["genere"].astype(str)

carriera2=carriera2.drop(carriera2.columns[[0, 1, 7]], axis=1)
carriera2.rename(columns={'key': 'fascia'}, inplace=True)


mydict = []

for x in range(len(carriera2)):
    diz={}
    ruolo = carriera2.iloc[x,5]    
    min=int(carriera2.iloc[x,0])
    q1=int(carriera2.iloc[x,1])
    median=int(carriera2.iloc[x,2])
    q3=int(carriera2.iloc[x,3])
    max=int(carriera2.iloc[x,4])
    valore=[min,q1,median,q3,max]
    print (valore)
    name='name'
    data='data'
    diz[name]=ruolo
    diz[data]=valore
    mydict.append(diz)



newlist = sorted(mydict, key=itemgetter('name')) 




with open('../data_csv/carriera_tipica_CORRETTO.json', 'w',) as fp:
    json.dump(newlist, fp, sort_keys=True, indent=4)
fp.close()





