import json
import requests

catalog = json.load(open('out.json'))

for i in catalog:
    try:
        if 'sku' not in i:
            pass
        if 'title' not in i:
            i['title'] = "NA"
        if 'productDescription' not in i:
            i['productDescription'] = "NA"
        if 'price' not in i:
            i['price'] = 0.0
        if 'productImage' not in i:
            i['productImage'] = "NA"
        if 'catlevel1Name' not in i:
            i['catlevel1Name'] = "NA"
        if 'catlevel2Name' not in i:
            i['catlevel2Name'] = "NA"

        r = requests.post('http://127.0.0.1:5000/insert', json=i)
        #print(f"Status Code: {r.status_code}, Response: {r.json()}")

    except:
        print("AHHHHH")
        break