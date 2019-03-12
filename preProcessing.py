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

#df = pd.read_csv('indeed.csv', sep=',', index_col='Unnamed: 0')

#%% Exploration : NaN, types d'objets
#df.isna().sum() / len(df) * 100
#df.info()

#%% Class Pre-processing

class preprocessing():

    """ Contient toutes les fonctions nécessaires à la création de colonnes 'propres'
        pour la prédiction et la visualisation. """

    def __init__(self):

        self = self


    def process_location(self, location):

        """ Extrait le code postal (pour l'IDF) ou la ville (pour les autres villes),
            puis le classe dans la catégorie 'Bassin_emploi' correspondante. """

        location = location.lower()
        # Extraction de la ville sans le code postal
        ville = re.findall(r'([a-zA-Z ]*)(?= \()', location)
        if len(ville) == 0:
            ville = re.findall(r'(^[a-zA-Z ]*)', location)
        ville = ville[0]
        localisation = ''
        # Boucle pour regrouper le bassin d'emploi parisien
        for i in ['toulouse', 'nantes', 'bordeaux', 'montpellier', 'lyon']:
            if ville == i:
                localisation = ville
                bassin_emploi = ville
                break
            else:
                bassin_emploi = 'Ile-de-France'

        if "Paris " in location:
            localisation = "Paris"
        elif "(95)" in location:
            localisation = "Val d'Oise 95"
        elif "(94)" in location:
            localisation = "Val de Marne 94"
        elif "(93)" in location:
            localisation = "Seine-Saint-Denis 93"
        elif "(92)" in location:
            localisation = "Hauts-de-Seine 92"
        elif "(91)" in location:
            localisation = "Essonnes 91"
        elif "(78)" in location:
            localisation = "Yvelines 78"
        elif "(77)" in location:
            localisation = "Seine-et-Marne 77"
        else:
            localisation = ville

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

        frequency = re.findall(r'(?<=par )(\w+)', salary)
        salary = salary.replace(' ','')
        sal = re.findall(r'([0-9]+)',salary)
        if len(sal) >= 2:
            sal_min = int(sal[0])
            sal_max = int(sal[1])
            salary = (sal_min+sal_max)/2
        else:
            salary = int(sal[0])

        if frequency[0] == 'mois':
            salary = salary *12
        elif frequency[0] == 'jour' or frequency[0] == 'jours':
            salary = salary * 365
        elif frequency[0] == 'an' or frequency[0] == 'ans':
            salary = salary
            
        # Integer
        return salary


    def process_poste(self,poste, resume):
        
        """ Extrait le métier et le statut. Ex : Data Scientist / CDI """

        poste = poste.lower()
        resume = resume.lower()

        postes = re.findall(r'(analyst|analyste|science|scientist|engineer|ingénieur)', poste)
        contrats = re.findall(r'(cdd|cdi|intern|stage|stagiaire|internship)', resume)
        
        if len(postes) >= 1:
            for i in postes:
                if i == 'science' or i == 'scientist':
                    poste = 'Data Scientist'
                    break
                elif i == 'engineer' or i == 'ingénieur':
                    poste = 'Data Engineer'
                    break
                elif i == 'analyst' or i =='analyste':
                    poste = 'Data Analyst'
                    break
                else:
                    poste = 'Dev'
        else:
            poste = 'Dev'
            
        if len(contrats) >=1:
            for i in contrats:
                if i == 'cdd':
                    contrat = 'CDD'
                    break
                elif i == 'intern' or i == 'stage' or i == 'stagiaire' or i == 'internship':
                    contrat = 'Stage'
                    break
                else:
                    contrat = 'CDI'
        else:
            contrat = 'CDI'
            

        return poste, contrat




