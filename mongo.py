from pymongo import MongoClient


class Mongo():

    def __init__(self):
        client = MongoClient('localhost', 27017)
        db = client.test_database
        test = 'indeed_v4'
        self.collection = db[test]

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
    
    def add_prediction(self,id,forest,rbf):
       
        newvalues = { "$set": { "Forest": forest, "RBF":rbf } }
        myquery = self.collection.find_one({'_id':id})
        self.collection.update_one(myquery, newvalues)
