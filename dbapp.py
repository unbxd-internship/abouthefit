from sqlalchemy import create_engine
import json
from flask import Flask
from flask import request
from flask import Response
from sqlalchemy.orm import sessionmaker
from table import Base, Product
import requests
db_string = "postgresql://unbxd:myPassword@localhost:5432/catalog"

db = create_engine(db_string)

Base.metadata.create_all(db)

Session = sessionmaker(bind=db)

app = Flask("CatalogEntry")
#app.run(debug=True)


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
        
@app.route('/get_category', methods = ['GET'])
def get_category():
        #get all the categories
        try:
                s = Session()
                result_temp = s.query(Product).all()
                #response = []
                catlevel1 = []
                catlevel2 = []
                for row in result_temp:
                        if row.catlevel1name not in catlevel1:
                                catlevel1.append(row.catlevel1name)
                        if row.catlevel2name not in catlevel2:
                                catlevel2.append(row.catlevel2name)
                return {'catlevel1Name': catlevel1, 'catlevel2Name': catlevel2}

                #return Response(json.dumps({
                #         'status': 'ok',
                #         'sku': product.sku,
                #         'title': product.title,
                #         'productDescription': product.productdescription,
                #         'price': product.price,
                #         'productImage': product.productimage,
                #         'catlevel1Name': product.catlevel1name,
                #         'catlevel2Name': product.catlevel2name
                # }), status=200, mim
        
        except Exception as exc:
                #server error
                return Response(json.dumps({
                        'status': 'server_error',
                        'error': str(exc)
                }), status=500, mimetype='application/json')
        
@app.route('/category', methods = ['GET'])
def category():
        try:
                # Check if the relevant request arguments have been provided
                if not (
                        'catlevel1Name' in request.args or
                        'catlevel2Name' in request.args
                ):
                        # Bad request
                        return Response(json.dumps({
                                'status': 'bad_request',
                                'error': 'Missing required arguments'
                        }), status=400, mimetype='application/json')
        
                # Get the product from the database
                catlevel1Name = request.args['catlevel1Name']
                catlevel2Name = request.args['catlevel2Name']
                s = Session()
                result_temp = s.query(Product).filter(Product.catlevel1name == catlevel1Name, Product.catlevel2name==catlevel2Name).all()
                #response = []
                temp = []
                result_count = 0
                for row in result_temp:
                        result_count += 1
                        temp.append(Product.jsonformat(row))
                        #print(row.sku)
                        #print("sku:", row.sku, "title:", row.title, "productdescription:", row.productdescription, "price:", row.price, "productimage:", row.productimage, "catlevel1name:", row.catlevel1name, "catlevel2name:", row.catlevel2name)
                print(result_count)
                return temp

                #return Response(json.dumps({
                #         'status': 'ok',
                #         'sku': product.sku,
                #         'title': product.title,
                #         'productDescription': product.productdescription,
                #         'price': product.price,
                #         'productImage': product.productimage,
                #         'catlevel1Name': product.catlevel1name,
                #         'catlevel2Name': product.catlevel2name
                # }), status=200, mimetype='application/json')
        
        except Exception as exc:
                # Server error
                return Response(json.dumps({
                        'status': 'server_error',
                        'error': str(exc)
                }), status=500, mimetype='application/json')

@app.route('/product', methods = ['GET'])
def get_product():
       print("here")
       try:
                      # Check if the relevant request arguments have been provided
                        if not (
                                'sku' in request.args
                        ):
                                # Bad request
                                return Response(json.dumps({
                                        'status': 'bad_request',
                                        'error': 'Missing required arguments'
                                }), status=400, mimetype='application/json')
        
                        # Get the product from the database
                        s = Session()
                        product = s.query(Product).filter_by(sku = request.args['sku']).first()
                        s.close()
        
                        if product is None:
                                # Not found
                                return Response(json.dumps({
                                        'status': 'not_found'
                                }), status=404, mimetype='application/json')
        
                        # Ok - product found
                        return Response(json.dumps({
                                'status': 'ok',
                                'sku': product.sku,
                                'title': product.title,
                                'productDescription': product.productdescription,
                                'price': product.price,
                                'productImage': product.productimage,
                                'catlevel1Name': product.catlevel1name,
                                'catlevel2Name': product.catlevel2name
                        }), status=200, mimetype='application/json')    
        
       except Exception as exc:
                       # Server error
                        return Response(json.dumps({
                                'status': 'server_error',
                                'error': str(exc)
                        }), status=500, mimetype='application/json')
          
@app.route('/search', methods = ['GET'])
def search():
        #print("here")
        try:
                # Check if the relevant request arguments have been provided
                if not (
                        'searchTerm' in request.args
                ):
                        # Bad request
                        return Response(json.dumps({
                                'status': 'bad_request',
                                'error': 'Missing required arguments'
                        }), status=400, mimetype='application/json')

                # Get the search term
                search_term = request.args['searchTerm']
                search_term= search_term.replace(" ","+")
                print(search_term)
                # Get the products from the database
                link = "https://search.unbxd.io/fb853e3332f2645fac9d71dc63e09ec1/demo-unbxd700181503576558/search?q={}".format(search_term)
                print(link)
                response = requests.get(link).content
                #print(response.json())
                return Response(response)
        except Exception as exc:
                # Server error
                return Response(json.dumps({
                        'status': 'server_error',
                        'error': str(exc)
                }), status=500, mimetype='application/json')

if __name__ == '__main__':
        app.run(debug= True)
