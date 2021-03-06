#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Mar  5 10:08:04 2019

@author: ejoz / anthony
"""
import pandas as pd
import numpy as np
from sklearn import model_selection
from sklearn.model_selection import train_test_split
from sklearn.model_selection import GridSearchCV
from sklearn.model_selection import cross_val_score
from sklearn.ensemble import RandomForestClassifier, AdaBoostClassifier
from sklearn.svm import SVC
from sklearn.metrics import accuracy_score, f1_score
import matplotlib.pyplot as plt
import mongo


class Modele():

    def __init__(self):
        self = self

    def run_models(self):

        import mongo
        # Importation de la base de données en dataframe
        mongo = mongo.Mongo()
        df = mongo.get_df()
        cols = ['Bassin_emploi', 'Compagny', 'Contrat', 'Date', 'Date_scrap', 'Location', 'Poste', 'Resume', 'Salary', '_id','Forest','RBF']
        df = pd.DataFrame(df,columns=cols)

        # Sélection des données qui comportent un salaire
        data = df[['Bassin_emploi', 'Contrat', 'Poste', 'Salary']][df['Salary'] != '']

		# Encodage des données en numérique
        data = pd.get_dummies(data=data, columns={'Poste', 'Bassin_emploi', 'Contrat'}, drop_first=True)

		# Séparation des données indépendantes/target
        x = data.iloc[:, 1:]
        y = data['Salary'].astype('int64')
        x_train, x_test, y_train, y_test = train_test_split(x, y)

        # Implantation du Kernel RBF
        rbf = SVC()
        parameters = {'kernel': ['rbf'],
        			  'gamma': [1e-3, 1e-4],
        			  'C': [1, 10, 100, 1000],
        			  'shrinking' : [True, False]}
        clf_rbf = GridSearchCV(rbf, parameters, cv=5)
        clf_rbf.fit(x_train, y_train)
        clf_rbf.best_params_
        y_pred_rbf = clf_rbf.predict(x_test)

#        # Comparaison données test/entraînement > seulement pour les tests
#        plt.scatter(range(len(y_test)), y_test, color = 'blue')
#        plt.scatter(range(len(y_pred_rbf)), y_pred_rbf, color = 'red')
#        plt.legend(('Training set', 'Test set'))
#        plt.title('Comparaison des résultats avec le modèle Kernel RBF')

        # Implantation du Random Forest
        rf = RandomForestClassifier()
        parameters = grid_param = {'n_estimators': [100, 300, 500, 800, 1000],
        						   'criterion': ['gini', 'entropy'],
        						   'bootstrap': [True, False]}
        clf_rf = GridSearchCV(rf, parameters, cv=5)
        clf_rf.fit(x_train, y_train)
        clf_rf.best_params_
        y_pred_rf = clf_rf.predict(x_test)

#		 # Score du modèle
#        accuracy_score(y_test, y_pred_rf)
#        f1_score(y_test, y_pred_rf, average='micro')
#        all_accuracies = cross_val_score(estimator=clf_rf, X=x_train, y=y_train, cv=5)

#        # Comparaison données test/entraînement > seulement pour les tests
#        plt.scatter(range(len(y_test)), y_test, color = 'blue')
#        plt.scatter(range(len(y_pred_rf)), y_pred_rf, color = 'red')
#        plt.legend(('Training set', 'Test set'))
#        plt.title('Comparaison des résultats avec le modèle Random Forest')

        # Prédiction : ajout dans la DB Mongo
        data_to_pred = df[['Bassin_emploi', 'Contrat', 'Poste', '_id']][df['Salary'] == '']
        data_to_pred = pd.get_dummies(data=data_to_pred, columns={'Poste', 'Bassin_emploi', 'Contrat'}, drop_first=True)

        data_to_pred['Salaires_RBF'] = clf_rbf.predict(data_to_pred.iloc[:, 1:])
        data_to_pred['Salaires_Random_Forest'] = clf_rf.predict(data_to_pred.iloc[:, 1:-1])
        final_data = data_to_pred[['_id', 'Salaires_RBF', 'Salaires_Random_Forest']]

        indexes = final_data.index

        for i in indexes:
            forest = final_data.loc[i,'Salaires_Random_Forest']
            rbf = final_data.loc[i,'Salaires_RBF']
            df.loc[i,'Forest'] = forest
            df.loc[i,'RBF'] = rbf

        if mongo.final_df(df):
            print('DB updated')

        return True


