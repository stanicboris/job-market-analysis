# -*- coding: utf-8 -*-
"""
Éditeur de Spyder

Ceci est un script temporaire.
"""
import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_table
import pandas as pd

df = pd.read_csv("indeed_v4.csv", sep=",", index_col='Unnamed: 0')

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = html.Div(children=[
    html.H1(children="DB"),
    dash_table.DataTable(
    id='table',
    columns=[{"name": i, "id": i} for i in df.columns],
    data=df.to_dict("rows"),
    style_table={
        'maxHeight': '300',
        'overflowY': 'scroll'
    },
    filtering=True,
    editable=True
)
    ,
    html.H1(children='Rapport Indeed'),

    html.Div(children='''
        Analyse de l'emploi à Paris, Lyon, Toulouse, Nantes, Montpellier et Bordeaux
    '''),

    dcc.Graph(
        id='example-graph',
        figure={
            'data': [
                {'x': df['Bassin_emploi'], 'y': df['Salary'], 'type': 'bar', 'name': 'Semaine précédente'}
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
                {'x': df['Bassin_emploi'], 'y': df['Salary'][df['Poste']=='Dev'], 'type': 'bar', 'name': u'Dev'},
                {'x': df['Bassin_emploi'], 'y': df['Salary'][df['Poste']=='Data Scientist'], 'type': 'bar', 'name': u'Data Scientist'},
                {'x': df['Bassin_emploi'], 'y': df['Salary'][df['Poste']=='Data Analyst'], 'type': 'bar', 'name': u'Data Analyst'}
            ],
            'layout': {
                'title': 'Répartition des offres d\'emploi'
            }
        }
    )
])

if __name__ == '__main__':
    app.run_server(debug=True)
    
    