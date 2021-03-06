from pymongo import MongoClient
import pandas as pd
import re

class Mongo():

    def __init__(self):

        """ Connexion à la base de données. """

        client = MongoClient('mongodb://localhost:27017/')
        self.db = client.test_database
        self.col_name = 'indeed_v4_temp' # Table temporaire
        self.collection = self.db[self.col_name]
        self.col_name2 = 'indeed_v4' # Table actualisée, contenant les nouvelles données des salaires
        self.collection2 = self.db[self.col_name2]

    def add_db(self, line_to_add,counter):

        """ Ajoute une annonce à la DB. """

        self.collection.insert_one(line_to_add)
        #print('Annonce ', counter, ' added to DB  ')

    def check_db(self,line_to_check):

        """ Evite les doublons. """    

        if self.collection.find_one({'Resume':line_to_check['Resume']}):
            elem_test = self.collection.find_one({'Resume':line_to_check['Resume']})
            if elem_test['Location'] == line_to_check['Location']:
                return True
        return False

    def get_df(self):

        """ Charge la DB temporaire en dataframe > utilisé dans le script 'modeles.py'. """

        df = pd.DataFrame(list(self.collection.find()))
        return df
    
    def add_prediction(self,idt,forest,rbf):

        """ Ajoute les colonnes 'salaires_forest' et 'salaires_rbf' à la DB. """
       
        newvalues = { "$set": { "Forest": forest, "RBF":rbf } }
        myquery = self.collection.find_one({'_id':idt})
        self.collection.update_one(myquery, newvalues)
    
    def final_df(self,df):

        
        
        for i in df.index:
            self.collection2.insert_one(dict(df.loc[i,:]))
        return True

    def add_email(self,email):

        """ Ajoute une colonne 'email' à la DB. """

        collection = self.db['emails']
        collection.insert_one({'mail':email})
        return True

    def check_mail(self,email):
        """ Regex qui récupère l'email. """
        if re.match(r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)",email):
            return True
        return False

    def drop_collection(self):
        self.db.drop_collection(self.col_name)
        self.db.drop_collection(self.col_name2)
        return True

    def add_user(self,email,password):
        col_name = 'users' 
        collection = self.db[col_name]
        import random
        hash_id = random.getrandbits(128)
        collection.insert_one({'user_email':email, 'user_password':password, 'hash_id':hash_id})
        
    def check_user(self,email):
        col_name = 'users' 
        collection = self.db[col_name]
        user = collection.find_one({'user_email':email})
        if user:
            return True
        return False
            
    
#DB = Mongo()


            
            
            
            
            
            
            
            
        



        
        
        
        
        
        
        
        
        