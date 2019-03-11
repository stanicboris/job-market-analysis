from pymongo import MongoClient


class Mongo():

    def __init__(self):
        client = MongoClient('localhost', 27017)
        db = client.test_database
        test = 'col_indeed_scrap'
        self.collection = db[test]

    def add_db(self, line_to_add,counter):
        self.collection.insert_one(line_to_add)
        print('Annonce ', counter, ' added to DB  ')