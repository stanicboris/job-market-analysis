print('coucou')
from pymongo import MongoClient
client = MongoClient('mongodb://localhost:27017/')
db = client.test_database
col_name = 'indeed_v4_temp' # Table temporaire
collection = db[col_name]
col_name2 = 'indeed_v4' # Table actualisée, contenant les nouvelles données des salaires
collection2 = db[col_name2]
collection.insert_one({'id':'bite'})

a = collection.find()
print(a[0])