import mongo
# Importation de la base de données en dataframe
mongo = mongo.Mongo()

df = mongo.get_df()
print('Longueur Database = ',len(df)) 