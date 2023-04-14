from pymongo import MongoClient

class MongoDb():
    def __init__(self,url_conection:str,database:str) -> None:
        self.client = MongoClient(url_conection)
        self.database_name = database
        self.database = self.client[self.database_name]

    def get_database(self):
        return self.database
    
    def get_collection(self,collection:str):
        return self.database[collection]
    
    def insert_one(self,collection:str,data:dict):
        return self.database[collection].insert_one(data)
    
    def find_one(self,collection:str,query:dict):
        return self.database[collection].find_one(query)

    def find(self,collection:str,query:dict):
        return self.database[collection].find(query)
    
    def update_one(self,collection:str,query:dict,data:dict):
        return self.database[collection].update_one(query,{"$set":data})
    
    def delete_one(self,collection:str,query:dict):
        return self.database[collection].delete_one(query)