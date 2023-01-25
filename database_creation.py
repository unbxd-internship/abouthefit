from sqlalchemy import create_engine
import json
from flask import Flask
from flask import request
from flask import Response
from sqlalchemy.orm import sessionmaker
from table import Base, Product
import requests
import math

db_string = "postgresql://unbxd:myPassword@localhost:5432/catalog"

db = create_engine(db_string)

Base.metadata.create_all(db)

Session = sessionmaker(bind=db)

app = Flask("CatalogEntry")

@app.route('/clear', methods = ['POST'])
def clear():
    print(request)
    if request.form['password'] == 'myPassword':
        try:
                Base.metadata.drop_all(db)
                # Ok - table deleted
                return Response(json.dumps({
                        'status': 'ok'
                }), status=200, mimetype='application/json')
        except Exception as exc:
                # server error
                return Response(json.dumps({
                        'status': 'server_error',
                        'error': str(exc)
                }), status=500, mimetype='application/json')
        

@app.route('/insert', methods = ['POST'])
def insert():
        #print("request",request.json)
        try:    
                
                # Check if the relevant request arguments have been provided
                if not (
                        'sku' in request.json and
                        'title' in request.json and
                        'productDescription' in request.json and
                        'price' in request.json and
                        'productImage' in request.json and
                        'catlevel1Name' in request.json and
                        'catlevel2Name' in request.json
                ):
                        # Bad request
                        return Response(json.dumps({
                                'status': 'bad_request',
                                'error': 'Missing required arguments'
                        }), status=400, mimetype='application/json')

        # Add a new product
                new_product = Product(
                        sku = request.json['sku'],
                        title = request.json['title'],
                        productdescription = request.json['productDescription'],
                        price = request.json['price'],
                        productimage = request.json['productImage'],
                        catlevel1name = request.json['catlevel1Name'],
                        catlevel2name = request.json['catlevel2Name']
                )

        # Add the product to the database
                s = Session()
                s.add(new_product)
                s.commit()
                s.close()

        # Ok - product added
                return Response(json.dumps({
                        'status': 'ok'
                }), status=200, mimetype='application/json')

        except Exception as exc:
                print(exc)
                #server error
                return Response(json.dumps({
                        'status': 'server_error',
                        'error': str(exc)
                }), status=500, mimetype='application/json')
        

if __name__ == '__main__':
        app.run(debug=True)