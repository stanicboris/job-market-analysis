# -*- coding: utf-8 -*-
"""
Created on Tue Feb 26 15:34:21 2019

@author: antho

-SCRAPPING : Choisir critère de recherche (Annonce DataScientist, localisation,
type de contrat ect...)
-DATA ARCHITECTURE : Remplir automatiquement une base Mongo
-MACHINE LEARNING : Sur les annonces ou il y salaire, appliquer randomForest et Kernel SVM
-MACHINE LEARNING : Sur les annonces ou il n 'y a pas de salaire, déduire le salaire de ces annonces
-BUSINESS INTELLIGENCE :Atomatiser cette base automatiquement_script d'Automation
-BUSINESS INTELLIGENCE : DataViz (libre) Report tous les lundi matin par exemple grâce à un script
-A mettre sur Gitub
ATTENTION : EXPLICATION CHAQUE LIGNE CODE
"""

import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
import re
import time
from datetime import datetime , timedelta
from pymongo import MongoClient


class Scrapper:
    
    def __init__(self, metier, localisation, email):
        self.email = email
        self.metier = metier
        self.localisation = localisation
        self.counter = 0

        client = MongoClient('localhost', 27017)
        db = client.test_database
        test = 'col_indeed_scrap'
        self.collection = db[test]

    def add_db(self, line_to_add):
        self.collection.insert_one(line_to_add)
        print('Annonce ', self.counter, ' added to DB : ', self.collection)

    def process_date(self,str_date):
        if re.findall(r'heures',str_date):
            nb_heures = re.findall(r'([0-9]) heures',str_date)
            nb_heures = int(nb_heures[0])  
            duree = datetime.now() - timedelta(hours=nb_heures)
            date = duree.date()
        elif re.findall(r'heure',str_date):
            nb_heures = 1
            duree = datetime.now() - timedelta(hours=nb_heures)
            date = duree.date()
        elif re.findall(r'jours',str_date):
            if re.findall(r' ([0-9]) jours',str_date):
                nb_jours = re.findall(r'([0-9]+) jours',str_date)
                nb_jours = int(nb_jours[0])  
                duree = datetime.now() - timedelta(days=nb_jours)
                date = duree.date()
            else:
                duree = datetime.now() - timedelta(days=30)
                date = duree.date()
        elif re.findall(r'jour',str_date):
            duree = datetime.now() - timedelta(days=1)
            date = duree.date()
        else:
            date = ''
        return date.strftime("%d/%m/%Y")

    def scrap(self):

        profile = webdriver.FirefoxProfile()
        profile.set_preference("browser.cache.disk.enable", False)
        profile.set_preference("browser.cache.memory.enable", False)
        profile.set_preference("browser.cache.offline.enable", False)
        profile.set_preference("network.http.use-cache", False)
        driver = webdriver.Firefox(profile, executable_path=r'C:\Users\antho\Documents\Python Scripts\geckodriver.exe')
        
        df = pd.DataFrame(columns=['Poste', 'Location', 'Compagny', 'Salary', 'Resume', 'Date'])
        driver.get('https://www.indeed.fr/')  # Aller sur le site
        driver.find_element_by_xpath('//*[@id="text-input-what"]').send_keys(self.metier)  # Ecrire dans la barre de recherche
        time.sleep(1)
        text = driver.find_element_by_xpath('//*[@id="text-input-where"]').get_attribute('value')  # prend le texte qui se met automatiquement dans la localisation
        for i in range(0, len(text)):
            time.sleep(0.2)
            driver.find_element_by_xpath('//*[@id="text-input-where"]').send_keys(Keys.BACKSPACE)  # effacer la localisation pré-ecrite
        driver.find_element_by_xpath('//*[@id="text-input-where"]').send_keys(self.localisation)  # Ecrire dans la barre de localisation
        driver.find_element_by_xpath('/html/body/div/div[2]/div[2]/div/form/div[3]/button').click()  # clicker sur rechercher

        groupe = 1
    
        while True:
            driver.delete_all_cookies()
            while True:
                
                results = driver.find_elements_by_class_name('result')
                len(results)
                for i in range(0, len(results)):
                    self.counter += 1
                    poste = results[i].find_element_by_class_name('jobtitle').text
                    poste_clikable = results[i].find_element_by_class_name('jobtitle') 
                    location = results[i].find_element_by_class_name('location').text
                    try:
                        company_elem = results[i].find_element_by_class_name('company').text
                    except:
                        company_elem = ''
                    try:
                        date = results[i].find_element_by_class_name('date').text
                        date = self.process_date(date)
                    except:
                        date = ''
                    try:
                        salary = results[i].find_element_by_class_name('salary').text
                    except:
                        salary = ''
                    
                    try:
                        poste_clikable.click() # ouvrir la side windows
                        listener = WebDriverWait(driver, 5).until(ec.visibility_of_element_located((By.XPATH, '//*[@id="vjs-desc"]')))
                        listener.click()
                        resume = driver.find_element_by_xpath('//*[@id="vjs-desc"]').text # récupérer la description
                    except:
                        resume = ''
                    line = {'Poste': poste, 'Location': location, 'Compagny': company_elem, 'Salary': salary, 'Resume': resume, 'Date': date}
                    if self.collection.find_one(line):
                        print('trouvé dans la Database, suivant !')
                    else:
                        self.add_db(line)
                        df = df.append(line, ignore_index=True)
                    
                time.sleep(1)
                btn_list = driver.find_elements_by_class_name('np')  # liste boutons suivant et precedent
                len(btn_list)
                if len(btn_list) > 1:  # si il y a precedent et suivant
                    try:
                        btn_list[1].click()  # clicker sur suivant
                    except:
                        driver.refresh()
                        time.sleep(2)
                        btn_list = driver.find_elements_by_class_name('np')  # liste boutons suivant et precedent
                        btn_list[1].click()  # clicker sur suivant

                elif btn_list[0].text == '« Précédent':  # si il y a que précédent on est arrivé au bout
                    break
                else:
                    btn_list[0].click()  # cllicker sur suivant

                try:
                    time.sleep(3)  # attendre que la popup s'ouvre
                    driver.find_element_by_xpath('//*[@id="popover-close-link"]').click()  # fermer popup
                except:
                    pass

            try:
                time.sleep(2)
                driver.find_element_by_xpath('/html/body/table[2]/tbody/tr/td/table/tbody/tr/td[2]/p/a').click() #cliker sur autres resultats de recherche
                groupe += 1
            except:
                break   
        return df    


location_list = ['Paris', 'Toulouse', 'Lyon', 'Nantes', 'Bordeaux', 'Montpelier']
for i in range(0,len(location_list)):
    parisds = Scrapper('Data scientist , data analyst , data engineer , développeur web',location_list[i],'anthony93460@gmail.com')
    parisds.scrap()


df = pd.DataFrame(list(parisds.collection.find()))

df.to_csv('indeed.csv')








