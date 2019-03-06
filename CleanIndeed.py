#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Mar  6 11:13:19 2019

@author: ejoz
"""

# Importation des librairies nécessaires au nettoyage du dataframe
import pandas as pd
import numpy as np
import re
from datetime import datetime, timedelta
from math import isnan
pd.options.display.max_columns = None

df = pd.read_csv('indeed.csv', sep=',', index_col='Unnamed: 0')

#%% Exploration : NaN, types d'objets
df.isna().sum() / len(df) * 100
df.info()

#%% Class Pre-processing

class preprocessing():

    """ Contient toutes les fonctions nécessaires à la création de colonnes 'propres'
        pour la prédiction et la visualisation. """

    def __init__(self, database):

        self.database = database


    def process_location(self, location):

        """ Extrait le code postal (pour l'IDF) ou la ville (pour les autres villes),
            puis le classe dans la catégorie 'Bassin_emploi' correspondante. """

        # Extraction de la ville sans le code postal
        ville = re.findall(r'(\w+)(?= \()', location)

        # Boucle pour regrouper le bassin d'emploi parisien
        if ville in list('Toulouse', 'Nantes', 'Bordeaux', 'Montpellier', 'Lyon'):
            bassin_emploi = ville
        else:
            bassin_emploi = 'Ile-de-France'

        return bassin_emploi


    def process_date(self, str_date):

        """ Transforme l'information Indeed 'il y a n heures/jours' par un objet datetime. """

        # Plusieurs heures
        if re.findall(r'heures', str_date):
            nb_heures = re.findall(r'([0-9]+) heures', str_date)
            nb_heures = int(nb_heures[0])
            duree = datetime.now() - timedelta(hours = nb_heures)
            date = duree.date()

        # Une heure
        elif re.findall(r'heure', str_date):
            nb_heures = 1
            duree = datetime.now() - timedelta(hours = nb_heures)
            date = duree.date()

        # Plusieurs jours
        elif re.findall(r'jours',str_date):

            if re.findall(r' ([0-9]) jours', str_date):
                nb_jours = re.findall(r'([0-9]+) jours', str_date)
                nb_jours = int(nb_jours[0])
                duree = datetime.now() - timedelta(days = nb_jours)
                date = duree.date()

            # 30+ jours
            else:
                duree = datetime.now() - timedelta(days = 30)
                date = duree.date()

        # Un jour
        elif re.findall(r'jour', str_date):
            duree = datetime.now() - timedelta(days = 1)
            date = duree.date()

        # Missing data
        else:
            date = ''

        # Objet datetime
        return date.strftime("%d/%m/%Y")


    def process_salary(self, salary):

        """ Transforme l'info Indeed en salaire brut /an. """





#%% Salary
#
#df['salary_min'] = df['Salary'].str.extract(r'([0-9]{2,3} [0-9]{3})(?= €)', expand=False)
#df['salary_min'] = pd.to_numeric(df['salary_min'].str.replace(" ", ""))
#
#df['salary_max'] = df['Salary'].str.extract(r'(?<=- )([0-9]{2,3} [0-9]{3})', expand=False)
#df['salary_max'] = pd.to_numeric(df['salary_max'].str.replace(" ", ""))
#
#df['Frequency'] = df['Salary'].str.extract(r'(?<=par )(\w+)', expand=False)
#
#df['salary_mean'] = (df['salary_min']+df['salary_max'])/2
#
##%%
#df['Poste'] = df['Poste'].str.lower()
#df['Poste'].str.extract(r'(cdi)', expand=False)