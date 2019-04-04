import pandas as pd

df = pd.read_csv('EUCircos_Regions_departements_circonscriptions_communes_gps.csv',sep=';', error_bad_lines=False)

print('Nb de lignes',len(df))

print('\n Colonnes = ',df.columns)
