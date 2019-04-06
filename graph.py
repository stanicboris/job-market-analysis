#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Apr  6 14:45:23 2019

@author: arnaudagbo
"""

import pandas as pd
import plotly
import plotly.plotly as py
import plotly.graph_objs as go

plotly.tools.set_credentials_file(username='masternono', api_key='GYUhjVOFUUtRYfjBq74Q')

# import du dataset
df = pd.read_csv('data/indeedv5.csv', index_col='Unnamed: 0')
df2 = pd.read_csv('data/indeed4.csv', index_col='Unnamed: 0')


# Fonction qui plot un graph salaire en fct ville et l'affiche sur le site plotly
def moySalaireParVille(df):
    df = df.dropna(how='any', subset=['Salary'])
    df = df.groupby('Bassin_emploi').mean()
    df = py.plot({
        "data": [go.Bar(x=df.index, y=df['Salary'])],
        "layout": go.Layout(title="Répartition de la moyenne des salaires selon les villes Semaine du 10 Mars")

    }, auto_open=True)
    return df


graphMoySalaryParVille = moySalaireParVille(df2)


# Fonction qui plot un graph de la moyenne des salaires par métier
def moySalaireParMetier(df):
    df = df.groupby('Poste').mean()
    df = py.plot({
        "data": [go.Bar(x=df.index, y=df['Salary'])],
        "layout": go.Layout(title="Répartition de la moyenne des salaires selon les métiers Semaine du 10 Mars")

    }, auto_open=True)
    return df


graphMoySalaryParMetier = moySalaireParMetier(df)


# Fonction qui plot un graph de la répartition des offres d'emploi selon le bassin d'emploi
def RepartitionAnnonceParVille(df):
    df = df['Bassin_emploi'].value_counts()
    labels = df.index
    values = df.values

    trace = go.Pie(labels=labels, values=values)

    df = py.plot([trace], filename='repartition des offres d\'emploi selon le bassin d\'emploi', auto_open=True)
    return df


graphRepartitionAnnonceParVille = RepartitionAnnonceParVille(df)