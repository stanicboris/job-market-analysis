import mongo
# Importation de la base de données en dataframe
mongo = mongo.Mongo()
mongo.drop_collection()