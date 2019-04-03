# plot un graphique et l'enregistre dans une page HTML
import plotly
import plotly.graph_objs as go
import pandas as pd

df = pd.read_csv('indeed_v4.csv', index_col='Unnamed: 0')


def dashtest(df):
    df = df.dropna(how='any', subset=['Salary'])
    df = df.groupby('Bassin_emploi').mean()
    df = plotly.offline.plot({
        "data": [go.Bar(x=df.index, y=df['Salary'])],
        "layout": go.Layout(title="Répartition de la moyenne de salaire selon les villes Semaine du 10 Mars")

    }, auto_open=True)
    return df


dashtest(df)t