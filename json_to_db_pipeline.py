import json
import requests
from database_model import Database_Model

class ingest():

    def __init__(self, json_path):
        self.json_path = json_path
        self.Database_Model = Database_Model()

    
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
    
    def fix_data(self, data):
        if 'sku' not in data:
            return False
        if 'title' not in data:
            data['title'] = ''
        if 'productDescription' not in data:
            data['productDescription'] = ''
        if 'price' not in data:
            data['price'] = ''
        if 'productImage' not in data:
            data['productImage'] = ''
        if 'catlevel1Name' not in data:
            data['catlevel1Name'] = ''
        if 'catlevel2Name' not in data:
            data['catlevel2Name'] = ''
        return data
    
    def into_db(self):

        self.Database_Model.delete_table()

        self.Database_Model.create_table()

        self.Database_Model.start_session()

        catalog = json.load(open(self.json_path))
        count = 0
        for i in catalog:
            try:
                if self.validate_data(i):
                    r = requests.post('http://127.0.0.1:5000/insert', json=i)
                    print(f"Status Code: {r.status_code}, Response: {r.json()}")
                else:
                    fixed_i = self.fix_data(i)
                    count+=1
                    if fixed_i:
                        r = requests.post('http://127.0.0.1:5000/insert', json=fixed_i)
                        print(f"Status Code: {r.status_code}, Response: {r.json()}")
            except:
                print("Error Loading Data")
                
        self.Database_Model.commit()
        self.Database_Model.close_session()

if __name__ == "__main__":
    ingest('out.json').into_db()