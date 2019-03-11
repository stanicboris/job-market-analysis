#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Mar  5 10:08:04 2019

@author: ejoz
"""

from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.tree import DecisionTreeClassifier, export_graphviz
from sklearn.ensemble import RandomForestClassifier, AdaBoostClassifier
from sklearn import metrics, svm
from sklearn.externals.six import StringIO
from IPython.display import Image
import pydotplus

df = pd.read_csv('indeed.csv', sep=',', index_col='Unnamed: 0')

#%%
import preProcessing

preProcessing.preprocessing()


#%% Kernel RBF
svm = svm.SVC(random_state=42)
parameters = {'kernel': ['rbf'],
			  'gamma': [1e-3, 1e-4],
			  'C': [1, 10, 100, 1000]}
clf = GridSearchCV(svm, parameters, cv=5)
clf.fit(x, y)

#%% Random Forest
rf = RandomForestClassifier()
parameters = grid_param = {'n_estimators': [100, 300, 500, 800, 1000],
						   'criterion': ['gini', 'entropy'],
						   'bootstrap': [True, False]
}
clf = GridSearchCV(svm, parameters, cv=5)
clf.fit(x, y)


