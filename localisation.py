#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Mar  6 10:56:03 2019

@author: arnaudagbo

TP INDEED

traitement des données du premier CSV
"""

# Importation des librairies
import pandas as pd

# Importation du dataset
# d1 = pd.read_csv('data/indeed1.csv')
d2 = pd.read_csv('data/indeed2.csv')

# %% Permet d'enlever les nan présent dans la colonne Location
d2 = d2.dropna(how='any', subset=['Location'])

# Cela nous indique que nous avons 83 valeurs différentes de localisation
d2['Location'].value_counts()

# Permet d'afficher toutes les localisation contenant le mot paris + espace à l'interieur
mask1 = d2['Location'].str.contains("Paris ")
a = d2[mask1]['Location'].value_counts()
print (a)

# %% Remplacer les valeurs contenant "paris " par Paris dans le dataset
for i in d2['Location'].index:
    if "Paris " in d2.loc[i, 'Location']:
        d2.loc[i, 'Location'] = "Paris"

# Vérifier que cela a bien fonctionné, nous avons maintenant 725 Paris et un CDG
mask2 = d2['Location'].str.contains("Paris")
b = d2[mask2]['Location'].value_counts()

# %% Remplacer les valeurs contenant 95 par Val d'oise 95
for i in d2['Location'].index:
    if "(95)" in d2.loc[i, 'Location']:
        d2.loc[i, 'Location'] = "Val d'oise 95"

    # Remplacer les valeurs contenant 94 par Val de Marne  dans le dataset
for i in d2['Location'].index:
    if "(94)" in d2.loc[i, 'Location']:
        d2.loc[i, 'Location'] = "Val de Marne 94"

    # Remplacer les valeurs contenant 93 par Haut de seine  dans le dataset
for i in d2['Location'].index:
    if "(93)" in d2.loc[i, 'Location']:
        d2.loc[i, 'Location'] = "Seine saint denis 93"

    # Remplacer les valeurs contenant 92 par Haut de seine  dans le dataset
for i in d2['Location'].index:
    if "(92)" in d2.loc[i, 'Location']:
        d2.loc[i, 'Location'] = "Haut de Seine 92"

# Remplacer les valeurs contenant 91 par Essonnes  dans le dataset
for i in d2['Location'].index:
    if "(91)" in d2.loc[i, 'Location']:
        d2.loc[i, 'Location'] = "Essonnes 91"

    # Remplacer les valeurs contenant 78 par Yvelines 78 dans le dataset
for i in d2['Location'].index:
    if "(78)" in d2.loc[i, 'Location']:
        d2.loc[i, 'Location'] = "Yvelines 78"

    # Remplacer les valeurs contenant 77 par Seine et Marne 77 dans le dataset
for i in d2['Location'].index:
    if "(77)" in d2.loc[i, 'Location']:
        d2.loc[i, 'Location'] = "Seine et Marne 77"
