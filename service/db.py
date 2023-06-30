import pymongo

class StreetEasierDataBase():
    """
    A simple wrapper class to interface with MongoDB

    Written mostly by Bard, but also tweaked by me
    """
    def __init__(self, host = "localhost", port = 27017, database_name = "StreetEasyResults"):
        self.client = pymongo.MongoClient(host, port)
        self.database = self.client[database_name]

    def initialize_collection(self, collection_name):
        if not self.database.get_collection(collection_name):
            self.database.create_database()

    def insert_listing(self, collection_name, document):
        self.database[collection_name].insert_one(document)

    def delete_listing(self, collection_name, document_id):
        self.database[collection_name].delete_one({"_id": document_id})

    def update_listing(self, collection_name, document_id, new_document):
        self.database[collection_name].update_one({"_id": document_id}, new_document)