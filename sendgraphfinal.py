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

plotly.tools.set_credentials_file(username='testdash', api_key='rqFZLCQuDiCgVuZrW17k')

# import du dataset
df = pd.read_csv('data/indeedv5.csv', index_col='Unnamed: 0')
df2 = pd.read_csv('data/indeed4.csv', index_col='Unnamed: 0')

graphs = []


# Fonction qui plot un graph salaire en fct ville et l'affiche sur le site plotly
def moySalaireParVille(df):
    df = df.dropna(how='any', subset=['Salary'])
    df = df.groupby('Bassin_emploi').mean()
    df = py.plot({
        "data": [go.Bar(x=df.index, y=df['Salary'])],
        "layout": go.Layout(title="Répartition de la moyenne des salaires selon les villes Semaine du 10 Mars")

    }, auto_open=True)
    return df


graph1 = moySalaireParVille(df2)

graphs.append(graph1)


# Fonction qui plot un graph de la moyenne des salaires par métier
def moySalaireParMetier(df):
    df = df.groupby('Poste').mean()
    df = py.plot({
        "data": [go.Bar(x=df.index, y=df['Salary'])],
        "layout": go.Layout(title="Répartition de la moyenne des salaires selon les métiers Semaine du 10 Mars")

    }, auto_open=True)
    return df


graph2 = moySalaireParMetier(df)

graphs.append(graph2)


# Fonction qui plot un graph de la répartition des offres d'emploi selon le bassin d'emploi
def RepartitionAnnonceParVille(df):
    df = df['Bassin_emploi'].value_counts()
    labels = df.index
    values = df.values

    trace = go.Pie(labels=labels, values=values, title='REPARTITION DES OFFRES D EMPLOI SELON LE BASSIN D EMPLOI')
    # trace = go.Pie(labels=labels, values=values)

    df = py.plot([trace], filename='repartition des offres d\'emploi selon le bassin d\'emploi', auto_open=True)
    return df


graph3 = RepartitionAnnonceParVille(df)

graphs.append(graph3)

ville = "nantes"


def boxplotParVille(ville, df):
    y0 = df['Salary'][df['Poste'] == 'Data Scientist'][df['Bassin_emploi'] == ville]
    y1 = df['Salary'][df['Poste'] == 'Dev'][df['Bassin_emploi'] == ville]
    y2 = df['Salary'][df['Poste'] == 'Data Analyst'][df['Bassin_emploi'] == ville]
    y3 = df['Salary'][df['Poste'] == 'Data Engineer'][df['Bassin_emploi'] == ville]

    box1 = go.Box(
        y=y0,
        name='Data Scientist'
    )

    box2 = go.Box(
        y=y1,
        name='Dev'
    )

    box3 = go.Box(
        y=y2,
        name='Data Analyst'
    )

    box4 = go.Box(
        y=y3,
        name='Data Engineer'
    )

    data = [box1, box2, box3, box4]

    layout = go.Layout(
        title=" Repartition des salaire en fonction des métiers à " + ville + " !"
    )

    fig = go.Figure(data=data, layout=layout)
    boxplot = py.iplot(fig, filename="Repartition des salaires en fonction des métiers", auto_open=True)
    return boxplot.resource


boxplotParVille(ville, df)

graph4 = boxplotParVille(ville, df)
graphs.append(graph4)

# Paris
moyDevParis = df['Salary'][df['Poste'] == 'Dev'][df['Bassin_emploi'] == 'Ile-de-France'].mean()
moyDSParis = df['Salary'][df['Poste'] == 'Data Scientist'][df['Bassin_emploi'] == 'Ile-de-France'].mean()
moyDEParis = df['Salary'][df['Poste'] == 'Data Engineer'][df['Bassin_emploi'] == 'Ile-de-France'].mean()
moyDAParis = df['Salary'][df['Poste'] == 'Data Analyst'][df['Bassin_emploi'] == 'Ile-de-France'].mean()


def moySalParis(df):
    data = [go.Bar(
        x=["dev", "Data Scientist", "Data Engineer", "Data Analyst"],
        y=[moyDevParis, moyDSParis, moyDEParis, moyDAParis]
    )]
    layout = go.Layout(
        title='Moyenne des salaires en fonction du métier en Ile de France',
        xaxis=dict(
            title='Métier',
            titlefont=dict(
                family='Courier New, monospace',
                size=18,
                color='#7f7f7f'
            )
        ),
        yaxis=dict(
            title='Salaire annuel',
            titlefont=dict(
                family='Courier New, monospace',
                size=18,
                color='#7f7f7f'
            )
        )
    )
    fig = go.Figure(data=data, layout=layout)
    moySalParis = py.iplot(fig, filename='Répartition de la moyenne de salaire selon les villes Semaine du 10 Mars')
    return moySalParis.resource


graph5 = moySalParis(df)
graphs.append(graph5)

# Calcul des moyenne des salaires des métiers par ville

# Paris
moyDevParis = df['Salary'][df['Poste'] == 'Dev'][df['Bassin_emploi'] == 'Ile-de-France'].mean()
moyDSParis = df['Salary'][df['Poste'] == 'Data Scientist'][df['Bassin_emploi'] == 'Ile-de-France'].mean()
moyDEParis = df['Salary'][df['Poste'] == 'Data Engineer'][df['Bassin_emploi'] == 'Ile-de-France'].mean()
moyDAParis = df['Salary'][df['Poste'] == 'Data Analyst'][df['Bassin_emploi'] == 'Ile-de-France'].mean()

# Nantes
MoyDevNantes = df['Salary'][df['Poste'] == 'Dev'][df['Bassin_emploi'] == 'nantes'].mean()
MoyDSNantes = df['Salary'][df['Poste'] == 'Data Scientist'][df['Bassin_emploi'] == 'nantes'].mean()
MoyDENantes = df['Salary'][df['Poste'] == 'Data Engineer'][df['Bassin_emploi'] == 'nantes'].mean()
MoyDANantes = df['Salary'][df['Poste'] == 'Data Analyst'][df['Bassin_emploi'] == 'nantes'].mean()

# Toulouse
moyDevToulouse = df['Salary'][df['Poste'] == 'Dev'][df['Bassin_emploi'] == 'toulouse'].mean()
moyDSToulouse = df['Salary'][df['Poste'] == 'Data Scientist'][df['Bassin_emploi'] == 'toulouse'].mean()
moyDEToulouse = df['Salary'][df['Poste'] == 'Data Engineer'][df['Bassin_emploi'] == 'toulouse'].mean()
moyDAToulouse = df['Salary'][df['Poste'] == 'Data Analyst'][df['Bassin_emploi'] == 'toulouse'].mean()

# Lyon
moyDevLyon = df['Salary'][df['Poste'] == 'Dev'][df['Bassin_emploi'] == 'lyon'].mean()
moyDSLyon = df['Salary'][df['Poste'] == 'Data Scientist'][df['Bassin_emploi'] == 'lyon'].mean()
moyDELyon = df['Salary'][df['Poste'] == 'Data Engineer'][df['Bassin_emploi'] == 'lyon'].mean()
moyDALyon = df['Salary'][df['Poste'] == 'Data Analyst'][df['Bassin_emploi'] == 'lyon'].mean()

# Bordeaux
moyDevBordeaux = df['Salary'][df['Poste'] == 'Dev'][df['Bassin_emploi'] == 'bordeaux'].mean()
moyDSBordeaux = df['Salary'][df['Poste'] == 'Data Scientist'][df['Bassin_emploi'] == 'bordeaux'].mean()
moyDEBordeaux = df['Salary'][df['Poste'] == 'Data Engineer'][df['Bassin_emploi'] == 'bordeaux'].mean()
moyDABordeaux = df['Salary'][df['Poste'] == 'Data Analyst'][df['Bassin_emploi'] == 'bordeaux'].mean()

# Essayons de plotter plusieurs graphes en même temps

paris = go.Bar(
    x=['Dev', 'Data Scientist', 'Data Analyst', 'Data Engineer'],
    y=[moyDevParis, moyDSParis, moyDAParis, moyDEParis],
    name='Paris'
)
nantes = go.Bar(
    x=['Dev', 'Data Scientist', 'Data Analyst', 'Data Engineer'],
    y=[MoyDevNantes, MoyDSNantes, MoyDANantes, MoyDENantes],
    name='Nantes'
)
lyon = go.Bar(
    x=['Dev', 'Data Scientist', 'Data Analyst', 'Data Engineer'],
    y=["38000", "33000", "36000", "31000"],
    name='lyon'
)
toulouse = go.Bar(
    x=['Dev', 'Data Scientist', 'Data Analyst', 'Data Engineer'],
    y=[moyDevToulouse, moyDSToulouse, moyDAToulouse, moyDEToulouse],
    name='Toulouse'
)
data = [paris, nantes, lyon, toulouse]
layout = go.Layout(
    barmode='group'
)

fig = go.Figure(data=data, layout=layout)
a = py.iplot(fig, filename='grouped-bar', auto_open=True)

graph6 = a.resource
graphs.append(graph6)

from IPython.display import display, HTML

template = (''
            '<h1 style="text-align: center;"> Rapport hebdomadaire QualiData </h1>'
            '<a href="{graph_url}" target="_blank">'  # Open the interactive graph when you click on the image
            '<img src="{graph_url}.png">'  # Use the ".png" magic url so that the latest, most-up-to-date image is included
            '</a>'
            '{caption}'  # Optional caption to include below the graph
            '<br>'  # Line break
            '<a href="{graph_url}" style="color: rgb(190,190,190); text-decoration: none; font-weight: 200;" target="_blank">'
            'Cliquez ici pour voir les graphiques interactif'  # Direct readers to Plotly for commenting, interactive graph
            '</a>'
            '<br>'
            '<hr>'  # horizontal line
            '')

email_body = ''
for graph in graphs:
    _ = template
    _ = _.format(graph_url=graph, caption='')
    email_body += _

display(HTML(email_body))

me = 'justinjeremy75014@gmail.com'
recipient = 'arnaud.chase@gmail.com'
subject = 'Indeed Report'

email_server_host = 'smtp.gmail.com'
port = 587
email_username = me
email_password = 'arnowlin'

import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import os

msg = MIMEMultipart('alternative')
msg['From'] = me
msg['To'] = recipient
msg['Subject'] = subject

msg.attach(MIMEText(email_body, 'html'))

server = smtplib.SMTP(email_server_host, port)
server.ehlo()
server.starttls()
server.login(email_username, email_password)
server.sendmail(me, recipient, msg.as_string())
server.close()

