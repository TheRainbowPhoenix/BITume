
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

# tbl_array = genfromtxt('samples/data/data_mining_DB_clients_tbl.csv')

print(tbl_df)

from sqlalchemy import create_engine
engine = create_engine('sqlite:///clients_tbl.db', echo=False)

tbl_df.to_sql('clients', con=engine, if_exists='replace')
bis_df.to_sql('bis', con=engine, if_exists='replace')
engine.execute("SELECT * FROM clients").first()
engine.execute("SELECT * FROM bis").first()