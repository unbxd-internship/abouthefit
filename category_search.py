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

#Get all the products in a category and sub-category       
@app.route('/category', methods = ['GET'])
def category():
        try:
                s = Session()
                query = s.query(Product)
                if 'catlevel1Name' in request.args:
                        query = query.filter_by(catlevel1name = request.args['catlevel1Name'])
                if 'catlevel2Name' in request.args:
                        query = query.filter_by(catlevel2name = request.args['catlevel2Name'])
                if 'page' in request.args:
                        page = int(request.args['page'])
                        start = (page-1)*10
                        end = start+10
                else:
                        start = 0
                        end = 10
                count_products = query.count()
                if 'sort' in request.args:
                        if request.args['sort']=='price asc':
                                result_temp = query.order_by(Product.price.asc()).slice(start,end).all()
                        elif request.args['sort']=='price desc':
                                result_temp = query.order_by(Product.price.desc()).slice(start,end).all()
                else:
                        result_temp = query.slice(start,end).all()
                results = []
                for row in result_temp:
                        results.append(Product.jsonformat(row))
                s.close()
                numberOfPages = math.ceil(count_products/10)

                return Response(json.dumps({'products': results, 'numberOfPages': numberOfPages, 'ProductCount': count_products}), status = 200, mimetype='application/json')
        
        except Exception as exc:
                # Server error
                return Response(json.dumps({
                        'status': 'server_error',
                        'error': str(exc)
                }), status=500, mimetype='application/json')
        
#Get individual product details fetched on sku
@app.route('/product', methods = ['GET'])
def get_product():
       # print("here")
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

#Get results based on search query         
@app.route('/search', methods = ['GET'])
def search():
        #print("here")
        try:
                # Check if the relevant request arguments have been provided
                if not ('q' in request.args):
                        # Bad request
                        return Response(json.dumps({
                                'status': 'bad_request',
                                'error': 'Missing required arguments'
                        }), status=400, mimetype='application/json')

                params = "q="+request.args['q']

                if 'sort' in request.args:
                        params = params + "&sort="+request.args['sort']

                if 'page' in request.args:
                        page = int(request.args['page'])
                        start_param = (int(request.args['page'])-1)*10
                        params = params + "&start="+ str(start_param)+ "&rows=10"
                else:
                        page = 1
                        params = params + "&start=0&rows=10"

                #params= params.replace(" ","+")
                #Define the UNBXD API and parameters
                link = "https://search.unbxd.io/fb853e3332f2645fac9d71dc63e09ec1/demo-unbxd700181503576558/search?{}".format(params)
                print(link)
                response = json.loads(requests.get(link).content)['response']
                #print(response)
                #print(len(response['products']))
                final_response = {'products': [], 'TotalNumberOfPages': 0, 'ProductCount': 0, 'PageNumber': 0}
                for i in response['products']:
                        try:
                                final_response['products'].append({'sku': i['sku'], 'title': i['title'], 'productdescription': i['productDescription'], 'price': i['price'], 'productimage': i['productImage'], 'catlevel1name': i['catlevel1Name'], 'catlevel2name': i['catlevel2Name']})
                        except:
                                print(final_response)
                #"TotalNumberOfPages": 10, "ProductCount": 92, "PageNumber": 1,"products": []
                #print(final_response)
                final_response['ProductCount'] = response['numberOfProducts']
                print("a", final_response['ProductCount'])
                final_response['TotalNumberOfPages'] = math.ceil(int(response['numberOfProducts'])/10)
                print("b", final_response['TotalNumberOfPages'])
                final_response['PageNumber'] = page
                print("c", final_response['PageNumber'])
                #print(final_response)
                return Response(json.dumps(final_response), status=200, mimetype='application/json')
        
        except Exception as exc:
                # Server error
                return Response(json.dumps({
                        'status': 'server_error',
                        'error': str(exc)
                }), status=500, mimetype='application/json')

if __name__ == '__main__':
        app.run(debug=True)
