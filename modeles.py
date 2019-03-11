#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Mar  5 10:08:04 2019

@author: ejoz
"""

from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.tree import DecisionTreeClassifier, export_graphviz
from sklearn.ensemble import RandomForestClassifier, AdaBoostClassifier
from sklearn.svm import SVC
from sklearn.externals.six import StringIO
from IPython.display import Image
import pydotplus

#%%
import pandas as pd
import numpy as np

df = pd.read_csv('indeed.csv', sep=',', index_col='Unnamed: 0', na_filter=True)
x = df.iloc[:, 1:5]
y = df.loc[:, 'Salary']
df.summary()
df.info()
df.isna().sum()

#%%
import preProcessing
process = preProcessing.preprocessing()

nanas = df['Salary'].isna().sum()
df['Salary'].isnull().sum()
df['Salary'] = df['Salary'].astype('str')

df['Poste'] = df['Poste'].astype('str')
df['Resume'] = df['Resume'].astype('str')

for row in range(len(x)):
	poste, contrat = process.process_poste(df.loc[row, 'Poste'], df.loc[row, 'Resume'])
	df.loc[row, 'Poste_clean'] = poste
	df.loc[row, 'Contrat'] = contrat

df['Contrat'].unique()
df['Poste_clean'].unique()


#%% Kernel RBF
parameters = {'kernel': ['rbf'],
			  'gamma': [1e-3, 1e-4],
			  'C': [1, 10, 100, 1000]}
clf = GridSearchCV(SVC(), parameters, cv=5)
clf.fit(x, y)

#%% Random Forest
rf = RandomForestClassifier()
parameters = grid_param = {'n_estimators': [100, 300, 500, 800, 1000],
						   'criterion': ['gini', 'entropy'],
						   'bootstrap': [True, False]
}
clf = GridSearchCV(svm, parameters, cv=5)
clf.fit(x, y)


