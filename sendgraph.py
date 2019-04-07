#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Apr  7 01:10:13 2019

@author: arnaudagbo
"""

import pandas as pd
import plotly 
import plotly.plotly as py
import plotly.graph_objs as go
plotly.tools.set_credentials_file(username='masternono', api_key='GYUhjVOFUUtRYfjBq74Q')

#import du dataset
df = pd.read_csv('indeed_v5.csv',index_col='Unnamed: 0')
#df2 = pd.read_csv('data/indeed4.csv',index_col='Unnamed: 0')

graphs = []

# Fonction qui plot un graph salaire en fct ville et l'affiche sur le site plotly
def moySalaireParVille(df):
    df = df.dropna( how='any',subset=['Salary'])
    df = df.groupby('Bassin_emploi').mean()
    df = py.plot({
    "data": [go.Bar(x=df.index,y=df['Salary'])],
    "layout": go.Layout(title="Répartition de la moyenne des salaires selon les villes Semaine du 10 Mars")
    
}, auto_open=True)
    return df

graph1 = moySalaireParVille(df)

graphs.append(graph1)

#Fonction qui plot un graph de la moyenne des salaires par métier 
def moySalaireParMetier(df):
    df = df.groupby('Poste').mean()
    df = py.plot({
    "data": [go.Bar(x=df.index,y=df['Salary'])],
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

    trace = go.Pie(labels=labels, values=values, title ='REPARTITION DES OFFRES D EMPLOI SELON LE BASSIN D EMPLOI')
    #trace = go.Pie(labels=labels, values=values)

    df = py.plot([trace], filename='repartition des offres d\'emploi selon le bassin d\'emploi', auto_open=True)
    return df


graph3 = RepartitionAnnonceParVille(df)


graphs.append(graph3)

from IPython.display import display, HTML

template = (''
    '<a href="{graph_url}" target="_blank">' # Open the interactive graph when you click on the image
        '<img src="{graph_url}.png">'        # Use the ".png" magic url so that the latest, most-up-to-date image is included
    '</a>'
    '{caption}'                              # Optional caption to include below the graph
    '<br>'                                   # Line break
    '<a href="{graph_url}" style="color: rgb(190,190,190); text-decoration: none; font-weight: 200;" target="_blank">'
        'Cliquez ici pour voir les graphiques interactif'  # Direct readers to Plotly for commenting, interactive graph
    '</a>'
    '<br>'
    '<hr>'                                   # horizontal line
'')

email_body = ''
for graph in graphs:
    _ = template
    _ = _.format(graph_url=graph, caption='')
    email_body += _

display(HTML(email_body))

me  = 'indeed.data@gmail.com'
recipient = 'anthony.93460@gmail.com'
subject = 'Indeed Report'

email_server_host = 'smtp.gmail.com'
port = 587
email_username = me
email_password = 'indeed123data'

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

