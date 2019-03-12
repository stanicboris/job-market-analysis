#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Mar  5 10:08:04 2019

@author: ejoz
"""
import pandas as pd
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split, GridSearchCV, cross_val_score
from sklearn.ensemble import RandomForestClassifier, AdaBoostClassifier
from sklearn.svm import SVC
from sklearn.metrics import accuracy_score, f1_score

#%% A transformer en importation mongo
df = pd.read_csv('indeed_v4.csv', sep=',', index_col='Unnamed: 0', na_filter=True)
df.info()
df.isna().sum()

#%% Pre-prcessing pour fitter le modèle
data = df[['Bassin_emploi', 'Contrat', 'Poste', 'Salary']][df['Salary'].isna() == False]
data = pd.get_dummies(data=data, columns={'Poste', 'Bassin_emploi', 'Contrat'}, drop_first=True)

x = data.iloc[:, 1:]
y = data['Salary']

lab_enc = LabelEncoder()
y_encoded = lab_enc.fit_transform(y)

x_train, x_test, y_train, y_test = train_test_split(x, y_encoded)

#%% Kernel RBF
rbf = SVC()
parameters = {'kernel': ['rbf'],
			  'gamma': [1e-3, 1e-4],
			  'C': [1, 10, 100, 1000]}
clf_rbf = GridSearchCV(rbf, parameters, cv=5)
clf_rbf.fit(x_train, y_train)
clf_rbf.best_params_


#%% Random Forest
rf = RandomForestClassifier()
parameters = grid_param = {'n_estimators': [100, 300, 500, 800, 1000],
						   'criterion': ['gini', 'entropy'],
						   'bootstrap': [True, False]}
clf_rf = GridSearchCV(rf, parameters, cv=5)
clf_rf.fit(x_train, y_train)
clf_rf.best_params_
y_pred = clf_rf.predict(x_test)
accuracy_score(y_test, y_pred)
f1_score(y_test, y_pred, average='micro')
all_accuracies = cross_val_score(estimator=clf_rf, X=x_train, y=y_train, cv=5)

