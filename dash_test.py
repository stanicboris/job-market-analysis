# -*- coding: utf-8 -*-
"""
Éditeur de Spyder

Ceci est un script temporaire.
"""
import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd

df = pd.read_csv("indeed_v4.csv", sep=",")

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = html.Div(children=[
    html.H1(children='Rapport Indeed'),

    html.Div(children='''
        Analyse de l'emploi à Paris, Lyon, Toulouse, Nantes et Bordeaux
    '''),

    dcc.Graph(
        id='example-graph',
        figure={
            'data': [
                {'x': df['Bassin_emploi'], 'y': df['Salary'][df['Salary']<50000], 'type': 'bar', 'name': 'Semaine précédente'}
            ],
            'layout': {
                'title': 'Répartition des offres d\'emploi'
            }
        }
    ),
        html.H1(children='Rapport Indeed'),

    html.Div(children='''
        Analyse de l'emploi à Paris, Lyon, Toulouse, Nantes et Bordeaux
    '''),
        dcc.Graph(
        id='example-graph2',
        figure={
            'data': [
                {'x': [1, 2, 3], 'y': [4, 1, 2], 'type': 'bar', 'name': 'Semaine précédente'},
                {'x': [1, 2, 3], 'y': [2, 4, 5], 'type': 'bar', 'name': u'Semaine actuelle'},
            ],
            'layout': {
                'title': 'Répartition des offres d\'emploi'
            }
        }
    )
])

if __name__ == '__main__':
    app.run_server(debug=True)
    
    