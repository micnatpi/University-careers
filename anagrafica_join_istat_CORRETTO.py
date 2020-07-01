
# coding: utf-8

# In[2]:


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
get_ipython().magic('matplotlib inline')
pd.set_option('max_columns', 300)
pd.set_option('max_rows', 10000)
#elimino i warning
import warnings
warnings.filterwarnings("ignore")
#import networkx as nx

#leggo il file completo dei dati
df=pd.read_csv('../dati_4-4-2017_per_new_DB/personale_ricerca_unipi_completo_flag_v3.csv', sep=';')

df.rename(columns ={'Cognome_Nome':'cognome_nome', 'Anno':'anno', 'Fascia':'fascia', 'Struttura':'struttura', 'Genere':'genere', 'Codice':'CODE', 'Matricola':'MATRICOLA'}, inplace=True)

usati=df[['CODE']].drop_duplicates(take_last=True)

#leggo il file della anagrafica
anagrafica=pd.read_csv('../dati_4-4-2017_per_new_DB/anagrafica.csv',sep=',')
# seleziono le sole variabili che mi servono
anagrafica2=anagrafica[['CODE', 'GENERE', 'CATASTO_NASC', 'CATASTO_FIS']]
anagrafica2.head()

#unisco i due dataframe

anagrafica3=pd.merge(usati, anagrafica2, on='CODE', how='left')
#elimino i valori null
anagrafica3=anagrafica3[~(anagrafica3.CATASTO_FIS.isnull())]

#leggo il file codici istat per la generazione delle mappe
istat=pd.read_csv('../dati_4-4-2017_per_new_DB/codici_istat.csv',sep=';')

# seleziono le variabili istat che mi sevono
istat2=istat[['Codice Catastale del comune','Denominazione in italiano', 'Denominazione regione']]
istat2.rename(columns ={'Codice Catastale del comune':'CATASTO_NASC'}, inplace=True)

# unisco le info sul posto di nascita
joined=pd.merge(anagrafica3, istat2, on='CATASTO_NASC', how='left')

joined.rename(columns={'Denominazione in italiano':'comune_nascita', 'Denominazione regione':'regione_nascita'}, inplace=True)

# aggiungo le info sulla residenza
joined2=pd.merge(joined, istat2, left_on='CATASTO_FIS', right_on='CATASTO_NASC', how='left')

joined2=joined2[['CODE', 'GENERE', 'CATASTO_NASC_x', 'CATASTO_FIS', 'comune_nascita','regione_nascita' ,'Denominazione in italiano','Denominazione regione' ]]

joined2.rename(columns={'CATASTO_NASC_x':'CATASTO_NASC', 'Denominazione in italiano':'comune_residenza','Denominazione regione':'regione_residenza'}, inplace=True)

# calcolo le statistiche sul comune di residenza
joined_g_comune=pd.pivot_table(joined2,index='comune_residenza', columns='GENERE', aggfunc='count', values='CODE').reset_index().fillna(0)
joined_g_comune['Tot']=joined_g_comune['F']+joined_g_comune['M']

# salvo il file nel csv
joined_g_comune.to_csv('../data_csv/anagrafica_grouped_comune_CORRETTO.csv')

# leggo le info sulle distanze di acccesso
comuni=pd.read_csv("../trigger-2017-04-24_VITTORIO/data_csv/comuni_accesso.csv")
comuni=comuni[['comune', 'Trasporto privato', 'Trasporto pubblico locale']]

comuni_accesso=pd.merge(comuni, joined_g_comune, left_on='comune', right_on='comune_residenza', how='left').fillna(0)
comuni_accesso.drop('comune_residenza', inplace=True,axis=1)

comuni_accesso=comuni_accesso.reset_index()

comuni_accesso.to_csv('../data_csv/comuni_accesso_CORRETTO.csv', index=False)


# calcolo le statistiche sulla regione di nascita

joined_g_regione=joined.groupby(by=['regione_nascita'])['regione_nascita'].count().sort_values(ascending=False)

#salvo il file
joined_g_regione.to_csv('../data_csv/anagrafica_grouped_regione_CORRETTO.csv')




