from pymongo import MongoClient
import pandas as pd

class Mongo():

    def __init__(self):
        client = MongoClient('localhost', 27017)
        self.db = client.test_database
        self.col_name = 'indeed_v4_temp'
        self.collection = self.db[self.col_name]
        self.col_name2 = 'indeed_v4'
        self.collection2 = self.db[self.col_name2]

    def add_db(self, line_to_add,counter):
        self.collection.insert_one(line_to_add)
        print('Annonce ', counter, ' added to DB  ')

    def check_db(self,line_to_check):
        if self.collection.find_one({'Resume':line_to_check['Resume']}):
            elem_test = self.collection.find_one({'Resume':line_to_check['Resume']})
            if elem_test['Location'] == line_to_check['Location']:
                return True
        return False

    def get_df(self):
        df = pd.DataFrame(list(self.collection.find()))
        return df
    
    def add_prediction(self,idt,forest,rbf):
       
        newvalues = { "$set": { "Forest": forest, "RBF":rbf } }
        myquery = self.collection.find_one({'_id':idt})
        self.collection.update_one(myquery, newvalues)
    
    def final_df(self,df):
        self.db.drop_collection(self.col_name)
        
        for i in df.index:
            self.collection2.insert_one(df.loc[i,:])
        return True
