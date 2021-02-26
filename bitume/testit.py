
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
import numpy as np

import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg')

# logistic regression modeling
lr_model = LogisticRegression()

from numpy import genfromtxt

import pandas as pd

tbl_df = pd.read_csv('samples/data/data_mining_DB_clients_tbl.csv')

bis_df = pd.read_csv('samples/data/data_mining_DB_clients_tbl_bis.csv')

"""
Clients :

Id
CDSEXE
MTREV
NBENF      : nombre d’enfants
CDSITFAM   : situation familiale, catégorielle
DTADH      : date adhésion à l’organisme
CDTMT      : statut (siège ou bien tsmt) = catégorielle 

CDDEM      : code démission 
DTDEM      : date démission 
ANNEE_DEM  : année démission
CDMOTDEM   : motif démission - Rien si non-démissionnaire ou si motif inconnu.

CDCATCL    : catégorie (sociétaire / adhérent)
AGEAD      : âge du client à l’adhésion
rangagead  : âge du client à l’adhésion par tranches 
agedem     : âge du client à la démission
rangagedem : âge du client à la démission par tranches 
rangdem    : date démission sous format mois année 
adh        : durée en années de l’adhésion 
rangadh    : durée en années de l’adhésion par tranches
"""

"""
Clients BIS:

Id         : auto increment
CDSEXE     : catégorielle
DTNAIS     : date naissance adhérent
MTREV      : numérique
NBENF      : nombre d’enfants
CDSITFAM   : situation familiale, catégorielle
DTADH      : date adhésion à l’organisme
CDTMT      : statut (siège ou bien tsmt) = catégorielle
CDMOTDEM   : motif démission. Rien si non-démissionnaire
CDCATCL    : catégorie (sociétaire / adhérent) Bpadh variable inconnue
DTDEM      : date démission (31/12/1900 si non démissionnaire)
"""

# tbl_array = genfromtxt('samples/data/data_mining_DB_clients_tbl.csv')

print(tbl_df)

result = pd.concat([tbl_df, bis_df], ignore_index=True, sort=False)
# print(result)

result['ANNEE_DEM'] = np.where(result['DTDEM'] != '1900-12-31', result['DTDEM'].apply(lambda x: int(x.split('-')[0])), result['ANNEE_DEM'])

# print(result)

result['AGEAD'] = np.where(result['AGEAD'].isnull() & result['DTNAIS'].notnull(), (result['DTADH'].apply(lambda x: int(x.split('-')[0]))) - (result['DTNAIS'].apply(lambda x: 0 if type(x) == float else int(x.split('-')[0]))), result['AGEAD'])

result['AGEAD'] = np.where(result['AGEAD'], result['AGEAD'].apply(lambda x: 0 if x > 500 else x), result['AGEAD'])

# year(DTADH) - year(DTNAISS)

# print(result)

result = result.drop(['Id'], axis=1)
result.insert(0, 'Id', result.index + 1)

# print(result)


result['adh'] = np.where(
    result['adh'].isnull(),  # & result['DTDEM'] != '1900-12-31'
    (result['DTDEM'].apply(lambda x: int(x.split('-')[0]))) - (result['DTADH'].apply(lambda x: 0 if type(x) == float else int(x.split('-')[0]))),
    result['adh']
)

# 2007 - 1900 = 107
result['adh'] = np.where(result['adh'], result['adh'].apply(lambda x: 107 + x if x < 0 else x), result['adh'])

# year(DTDEM) - year(DTADH) si démissionnaire

# print(result)

result['agedem'] = np.where(result['agedem'].isnull() & result['DTDEM'].notnull() & result['DTNAIS'].notnull(),
                            (result['DTDEM'].apply(lambda x: int(x.split('-')[0]))) - (result['DTNAIS'].apply(lambda x: 0 if type(x) == float else int(x.split('-')[0]))),
                            result['agedem'])

result['agedem'] = np.where(result['agedem'], result['agedem'].apply(lambda x: 0 if x < 0 else x), result['agedem'])
result['agedem'] = np.where(result['agedem'], result['agedem'].apply(lambda x: 0 if x == 1900 else x), result['agedem'])

# year(DTDEM) - year(DTNAISS))

# print(result)

# Clean structs

result = result.drop(['rangdem'], axis=1)
result = result.drop(['rangadh'], axis=1)
result = result.drop(['rangagead'], axis=1)
result = result.drop(['rangagedem'], axis=1)

# print(result)


CREATE_DB = True

if CREATE_DB:

    from sqlalchemy import create_engine
    engine = create_engine('sqlite:///clients_tbl.db', echo=False)

    tbl_df.to_sql('clients', con=engine, if_exists='replace')
    bis_df.to_sql('bis', con=engine, if_exists='replace')
    result.to_sql('result', con=engine, if_exists='replace')
    engine.execute("SELECT * FROM clients").first()
    engine.execute("SELECT * FROM bis").first()
    engine.execute("SELECT * FROM result").first()
