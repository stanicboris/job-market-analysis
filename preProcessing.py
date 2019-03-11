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

        self.database = database()


    def process_location(self, location):

        """ Extrait le code postal (pour l'IDF) ou la ville (pour les autres villes),
            puis le classe dans la catégorie 'Bassin_emploi' correspondante. """

        # Extraction de la ville sans le code postal
        ville = re.findall(r'(\w+)(?= \()', location)

        # Boucle pour regrouper le bassin d'emploi parisien
        if ville in list('Toulouse', 'Nantes', 'Bordeaux', 'Montpellier', 'Lyon'):
            bassin_emploi = ville
            localisation = bassin_emploi
        else:
            bassin_emploi = 'Ile-de-France'

        if "Paris " in location:
            localisation = "Paris"

        if "(95)" in location:
            localisation = "Val d'oise 95"

        if "(94)" in location:
            localisation = "Val de Marne 94"

        if "(93)" in location:
            localisation = "Seine saint denis 93"

        if "(92)" in location:
            localisation = "Haut de Seine 92"

        if "(91)" in location:
            localisation = "Essonnes 91"

        if "(78)" in location:
            localisation = "Yvelines 78"

        if "(77)" in location:
            localisation = "Seine et Marne 77"

        return bassin_emploi , localisation


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

        # Missing data // à supprimer ?
        else:
            date = ''

        # Objet datetime
        return date.strftime("%d/%m/%Y")


    def process_salary(self, salary):

        """ Transforme l'info Indeed en salaire brut /an. """

        salaries = re.findall(r'(\d+ ?\d+)(?= €)', salary)
        frequency = re.findall(r'(?<=par )(\w+)', salary)

        # Gestion des fourchettes de salaires
        if len(salaries) >= 2:
            salary_min = int(pd.to_numeric(salaries[0].replace(" ", "")))
            salary_max = int(pd.to_numeric(salaries[1].replace(" ", "")))
            salary = (salary_min+salary_max)/2

        else:
            salary = int(pd.to_numeric(salaries[0].replace(" ", "")))

        # Gestion de l'échelle
        if frequency == 'jour':
            salary = salary * 365

        elif frequency == 'mois':
            salary = salary * 12

        else:
            salary = salary

        # Integer
        return salary


    def process_poste(self, poste, resume):

        """ Extrait le métier et le statut. Ex : Data Scientist / CDI """

        self.poste = poste.lower()
        self.resume = resume.lower()

        postes = re.findall(r'(analyst|science|scientist|engineer|ingénieur)', poste)
        contrats = re.findall(r'(cdd|cdi|intern|stage|stagiaire|internship', resume)

        # Catégorisation métier
        if 'analyst' in postes:
            poste = 'Data analyst'
        elif 'science' or 'scientist' in postes:
            poste = 'Data scientist'
        elif 'engineer' or 'ingénieur' in postes:
            poste = 'Data engineer'
        else:
            poste = 'Développeur'

        # Catégorisation contrat
        if 'cdd' in contrats:
            contrat = 'CDD'
        elif 'intern' or 'stage' or 'internship' or 'stagiaire' in contrats:
            contrat = 'Stage'
        else:
            contrat = 'CDI'

        return poste, contrat




