import json
import requests
from database_connection import database_connection

class ingest():

    def __init__(self, json_path):
        self.json_path = json_path
        self.database_connection = database_connection()

    
    def validate_data(self, data):
        if not (
                'sku' in data and
                'title' in data and
                'productDescription' in data and
                'price' in data and
                'productImage' in data and
                'catlevel1Name' in data and
                'catlevel2Name' in data
        ):
            return False
        return True
    
    def into_db(self):
        self.database_connection.delete_table()
        self.database_connection.create_table()
        self.database_connection.start_session()
        catalog = json.load(open(self.json_path))
        for i in catalog:
            try:
                if self.validate_data(i):
                    r = requests.post('http://127.0.0.1:5000/insert', json=i)
                    print(f"Status Code: {r.status_code}, Response: {r.json()}")

            except:
                print("AHHHHH")
                
        self.database_connection.commit()
        self.database_connection.close_session()