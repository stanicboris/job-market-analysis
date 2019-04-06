import mongo
import pandas as pd
# Importation de la base de données en dataframe
mongo = mongo.Mongo()

df = mongo.get_df()
print('Longueur Database = ',len(df)) 


print(df['Salary'].dtypes)

df['Salary'] = pd.to_numeric(df['Salary'])

print(df['Salary'].dtypes)

df.to_csv('indeed_v5.csv')