from sqlalchemy import create_engine
import json
from flask import Flask
from flask import request
from flask import Response
from sqlalchemy.orm import sessionmaker
from table import Base, Product

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
        try:
                # Check if the relevant request arguments have been provided
                if not (
                        'sku' in request.form and
                        'title' in request.form and
                        'productDescription' in request.form and
                        'price' in request.form and
                        'productImage' in request.form and
                        'catlevel1Name' in request.form and
                        'catlevel2Name' in request.form
                ):
                        # Bad request
                        return Response(json.dumps({
                                'status': 'bad_request',
                                'error': 'Missing required arguments'
                        }), status=400, mimetype='application/json')

                # Add a new product
                new_product = Product(
                        sku = request.form['sku'],
                        title = request.form['title'],
                        productDescription = request.form['productDescription'],
                        price = request.form['price'],
                        productImage = request.form['productImage'],
                        catlevel1Name = request.form['catlevel1Name'],
                        catlevel2Name = request.form['catlevel2Name']
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
                # server error
                return Response(json.dumps({
                        'status': 'server_error',
                        'error': str(exc)
                }), status=500, mimetype='application/json')

if __name__ == '__main__':
        app.run()