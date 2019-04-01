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
import threading
import time
import preProcessing as pp 
import mongo
from bs4 import BeautifulSoup
import requests

class Scrapper:
    
    def __init__(self, metier, localisation, email):
        self.email = email
        self.metier = metier
        self.localisation = localisation
        self.counter = 0
        self.preprocess = pp.preprocessing()
        self.db = mongo.Mongo()

    def scrap(self):

        profile = webdriver.FirefoxProfile()
        profile.set_preference("browser.cache.disk.enable", False)
        profile.set_preference("browser.cache.memory.enable", False)
        profile.set_preference("browser.cache.offline.enable", False)
        profile.set_preference("network.http.use-cache", False)
        driver = webdriver.Firefox(profile)
        

        #df = pd.DataFrame(columns=['Poste', 'Location', 'Compagny', 'Salary', 'Resume', 'Date'])
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
        page = 0
        while True:
            driver.delete_all_cookies()
            while True:
                
                results = driver.find_elements_by_class_name('result')
                len(results)
                for i in range(0, len(results)):
                    driver.execute_script("arguments[0].scrollIntoView();", results[i])
                    self.counter += 1
                    poste = results[i].find_element_by_class_name('jobtitle').text
                    poste_clikable = results[i].find_element_by_class_name('jobtitle') 
                    location = results[i].find_element_by_class_name('location').text
                    bassin , location = self.preprocess.process_location(location)

                    try:
                        company_elem = results[i].find_element_by_class_name('company').text
                    except:
                        company_elem = ''

                    try:
                        date = results[i].find_element_by_class_name('date').text
                        date = self.preprocess.process_date(date)
                    except:
                        date = ''

                    try:
                        salary = results[i].find_element_by_class_name('salary').text
                        salary = self.preprocess.process_salary(salary)
                    except:
                        salary = ''

                    try:
                        
                        lien = results[i].find_element_by_class_name('turnstileLink').get_attribute('href')
                        if lien == None:
                            print('Pas de lien !')
                            continu = input('probleme de lien regarde la page')
                        r = requests.get(lien)
                        soup = BeautifulSoup(r.content,features='html.parser')
                        content = soup.find("div", {"class":"jobsearch-JobComponent-description"})
                        resume = ''
                        for elem in content.select("p,ul,li,ol"):
                            resume = resume + ' ' + elem.text
                        if resume == '':
                            resume = content.text
                    except:
                        resume = ''
                        
                    poste , contrat = self.preprocess.process_poste(poste,resume)

                    date_scrap = datetime.now().strftime("%d/%m/%Y, %H:%M:%S")

                    line = {'Poste': poste, 'Contrat':contrat, 'Location': location, 'Bassin_emploi':bassin, 'Compagny': company_elem, 'Salary': salary, 'Resume': resume,'Lien':lien, 'Date': date,'Date_scrap':date_scrap}

                    #TEST TEST TEST
                    print('\n\n RESUME = ',resume,'\nLIEN = ',lien)

                    if self.db.check_db(line):
                        print('trouvé dans la Database, suivant !') 
                    else:
                        if company_elem == '' and salary == '' and date == '' and poste == '' and location =='':
                            print('Blank Line ',counter)
                            continu = input('Continuer')
                        else:
                            #print(poste,' ajouté')
                            self.db.add_db(line,self.counter)
                            #df = df.append(line, ignore_index=True)
                
                time.sleep(1)
                btn_list = driver.find_elements_by_class_name('np')  # liste boutons suivant et precedent
                len(btn_list)
                if len(btn_list) > 1:  # si il y a precedent et suivant
                    try:
                        btn_list[1].click()  # clicker sur suivant
                        page +=1
                    except:
                        driver.refresh()
                        time.sleep(2)
                        btn_list = driver.find_elements_by_class_name('np')  # liste boutons suivant et precedent
                        btn_list[1].click()  # clicker sur suivant
                        page +=1

                elif btn_list[0].text == '« Précédent':  # si il y a que précédent on est arrivé au bout
                    break
                else:
                    btn_list[0].click()  # cllicker sur suivant
                    page +=1

                try:
                    time.sleep(3)  # attendre que la popup s'ouvre
                    driver.find_element_by_xpath('//*[@id="popover-close-link"]').click()  # fermer popup
                except:
                    pass

                if self.counter > 800:
                    driver.close()
                    return True

            try:
                time.sleep(2)
                driver.find_element_by_xpath('/html/body/table[2]/tbody/tr/td/table/tbody/tr/td[2]/p/a').click() #cliker sur autres resultats de recherche
                groupe += 1
            except:
                break   
        return True




class ScrapThread (threading.Thread):
    def __init__(self, n,metiers):
        threading.Thread.__init__(self)
        self.n = n
        self.location_list = ['Paris', 'Toulouse', 'Lyon', 'Nantes', 'Bordeaux', 'Montpelier']
        self.metiers = metiers
        
    def run(self):
        print("thread ", self.location_list[self.n])
        scrappeur = Scrapper(self.metiers,self.location_list[self.n],'anthony93460@gmail.com')
        scrappeur.scrap()


def startThreads(location_list,metiers,email):
    #location_list = ['Paris', 'Toulouse', 'Lyon', 'Nantes', 'Bordeaux', 'Montpellier']
    #metiers = 'data scientist , data analyst , data engineer , développeur , business intelligence'
    threads = {}
    for i in range(0,len(location_list)):
        threads['thread'+str(i)] = ScrapThread(i,metiers)
        threads['thread'+str(i)].start()
    print(threads)
    return threads
        
location_list = ['Paris', 'Toulouse', 'Lyon', 'Nantes', 'Bordeaux', 'Montpellier']
metiers = 'data scientist , data analyst , data engineer , développeur , business intelligence'
email = 'anthony.93460@gmail.com'
 

# startThreads(location_list,metiers,email)

# df = pd.DataFrame(list(parisds.collection.find()))

# df.to_csv('indeed.csv')








