import json
import requests
import sys
from models.database_model import Database_Model

'''Class to ingest the json file into the database'''
class ingest():

    def __init__(self, json_path):
        self.json_path = json_path
        self.Database_Model = Database_Model()

    '''Function to fix the data if any of the fields are missing'''
    def fix_data(self, data):
        if 'sku' not in data:
            return False
        if 'title' not in data:
            data['title'] = "NA"
        if 'productDescription' not in data:
            data['productDescription'] = "NA"
        if 'price' not in data:
            data['price'] = 0
        if 'productImage' not in data:
            data['productImage'] = "NA"
        if 'catlevel1Name' not in data:
            data['catlevel1Name'] = 'NA'
        if 'catlevel2Name' not in data:
            data['catlevel2Name'] = 'NA'
        return data

    def into_db(self):
        self.Database_Model.delete_table()
        self.Database_Model.create_table()
        self.Database_Model.start_session()
        catalog = json.load(open(self.json_path))

        for i in catalog:
            try:
                fixed_i = self.fix_data(i)
                if fixed_i:
                    r = requests.post('http://0.0.0.0:5000/insert', json=fixed_i)
                    print(f"Status Code: {r.status_code}, Response: {r.json()}")
            except Exception as e:
                print("Error Loading Data", e)

        self.Database_Model.commit()
        self.Database_Model.close_session()

if __name__ == "__main__":
    ingest('out.json').into_db()
