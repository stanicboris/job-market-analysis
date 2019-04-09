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
        import villes_csv

        location = location.lower()
        # Extraction de la ville et du le code postal
        localisation = re.findall(r'(.*)\(', location)[0]
        cp = int(re.findall(r'.* \(([0-9]*).*', location)[0])
        bassin_emploi = villes_csv.get_circo(cp)

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
        elif sal == 1:
            salary = int(sal[0])
        else: 
            salary = salary

        if frequency[0] == 'mois':
            salary = int(sal[0]) *12
        elif frequency[0] == 'jour' or frequency[0] == 'jours':
            salary = int(sal[0]) * 365
        elif frequency[0] == 'an' or frequency[0] == 'ans':
            salary = int(sal[0])
        elif frequency[0] == 'heure' or frequency[0] == 'heures':
            salary = int(sal[0]) * 24 * 365
        elif frequency[0] == 'semaine' or frequency[0] == 'semaines':
            salary = int(sal[0]) * 4 * 12
        else:
            salary = 0
            
        # Integer
        return salary


    def process_poste(self,poste, resume):
        
        """ Extrait le métier et le statut. Ex : Data Scientist / CDI """

        # On enleve les majuscules pour le traitement du texte"
        poste = poste.lower()
        resume = resume.lower()

        # Extraction d'informations pour classification
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




