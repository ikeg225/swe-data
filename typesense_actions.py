import os
import typesense
from dotenv import load_dotenv

class TypesenseActions:
    def __init__(self):
        load_dotenv()
        self.client = typesense.Client({
            'nodes': [{
                'host': os.getenv("TYPESENSE_HOST"),
                'port': os.getenv("PORT"),
                'protocol': 'http'
            }],
            'api_key': os.getenv("TYPESENSE_API"),
            'connection_timeout_seconds': 2
        })
    
    def del_cr_collection(self, name):
        self.client.collections[name].delete()
        schema = {
            "name": name,  
            "fields": [
                {"name": ".*", "type": "auto" }
            ]
        }
        self.client.collections.create(schema)
        return
    
    def start_companies(self):
        document = {
            'id': 'test',
            'company': 'test',
            'mainURL': 'test',
            'foundLogo': True
        }
        self.client.collections['companies'].documents.create(document)
        return 
    
    def del_test_companies(self):
        self.client.collections['companies'].documents['test'].delete()
        return
    
    def client(self):
        return self.client