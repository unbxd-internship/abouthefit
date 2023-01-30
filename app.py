from database_connection import database_connection
from table import Product
import json
from flask import Flask, request, Response
from flask_cors import CORS
import requests
import math

database_connection = database_connection()

app = Flask(__name__)
CORS(app)


@app.route('/insert', methods=['POST'])
def insert():
    json_data = request.json
    if database_connection.validate_data(json_data):
        try:
            database_connection.start_session()
            database_connection.insert_data(json_data)
            database_connection.commit()
            database_connection.close_session()
            return Response(json.dumps({
                'status': 'ok'
            }), status=200, mimetype='application/json')
        except Exception as exc:
            return Response(json.dumps({
                'status': 'server_error',
                'error': str(exc)
            }), status=500, mimetype='application/json')
    else:
        return Response(json.dumps({
            'status': 'bad_request',
            'error': 'Missing required arguments'
        }), status=400, mimetype='application/json')


@app.route('/delete', methods=['DELETE'])
def delete():
    try:
        database_connection.delete_table()
        return Response(json.dumps({
            'status': 'ok'
        }), status=200, mimetype='application/json')
    except Exception as exc:
        return Response(json.dumps({
            'status': 'server_error',
            'error': str(exc)
        }), status=500, mimetype='application/json')
    

@app.route('/', methods=['GET'])
@app.route('/home', methods=['GET'])
def get_homepage():
    try:
        database_connection.start_session()
        result_temp, result_count = database_connection.get_data(request.args)
        database_connection.close_session()
        result_products = []
        for product in result_temp:
            result_products.append(Product.jsonformat(product))

        numberOfPages = math.ceil(result_count/10)
        if 'page' not in request.args:
            page = 1
        else:
            page = int(request.args['page'])
        return Response(json.dumps({'TotalNumberOfPages': numberOfPages, 'ProductCount': result_count, 'PageNumber': page,  'products':result_products}), status = 200, mimetype='application/json')
    
    except Exception as exc:
        return Response(json.dumps({
            'status': 'server_error',
            'error': str(exc)
        }), status=500, mimetype='application/json')
    
@app.route('/category/', methods=['GET'])
@app.route('/category/<catlevel1name>', methods=['GET'])
@app.route('/category/<catlevel1name>/catlevel2name', methods=['GET'])
@app.route('/category/<catlevel1name>/<catlevel2name>/', methods=['GET'])
def category(catlevel1name = None, catlevel2name = None):
    try:
        database_connection.start_session()
        args = request.args.to_dict()
        if catlevel1name != None:
            args['catlevel1Name'] = catlevel1name
            if catlevel2name != None:
                args['catlevel2Name'] = catlevel2name
        result_temp, result_count = database_connection.get_data(args)
        #print(result_count, "result_count")
        
        database_connection.close_session()
        result_products = []

        for product in result_temp:
            result_products.append(Product.jsonformat(product))
        #print("result_products",result_products)
        numberOfPages = math.ceil(result_count/10)
        if 'page' in args:
            page = int(args['page'])
        else:
            page = 1
        return Response(json.dumps({'TotalNumberOfPages': numberOfPages, 'ProductCount': result_count, 'PageNumber': page,  'products':result_products}), status = 200, mimetype='application/json')
    
    except Exception as exc:
        return Response(json.dumps({
            'status': 'server_error',
            'error': str(exc)
        }), status=500, mimetype='application/json')
    
    
@app.route('/search', methods=['GET'])
def search():

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

        #Define the UNBXD API and parameters
        link = "https://search.unbxd.io/fb853e3332f2645fac9d71dc63e09ec1/demo-unbxd700181503576558/search?{}".format(params)
        #print(link)
        response = json.loads(requests.get(link).content)['response']

        final_response = {'products': [], 'TotalNumberOfPages': 0, 'ProductCount': 0, 'PageNumber': 0}
        for i in response['products']:
                try:
                        if database_connection.validate_data(i):
                            final_response['products'].append({'sku': i['sku'], 'title': i['title'], 'productdescription': i['productDescription'], 'price': i['price'], 'productimage': i['productImage'], 'catlevel1name': i['catlevel1Name'], 'catlevel2name': i['catlevel2Name']})
                except:
                        pass

        final_response['ProductCount'] = response['numberOfProducts']
        
        final_response['TotalNumberOfPages'] = math.ceil(int(response['numberOfProducts'])/10)
        
        final_response['PageNumber'] = page


        return Response(json.dumps(final_response), status=200, mimetype='application/json')

    except Exception as exc:
        # Server error
        return Response(json.dumps({
                'status': 'server_error',
                'error': str(exc)
        }), status=500, mimetype='application/json')


@app.route('/product/<sku>', methods=['GET'])
def product(sku = None):
    try:
        args = request.args.to_dict()
        database_connection.start_session()
        if sku != None:
            args['sku'] = sku
            result = database_connection.get_data(args)
            if result == None:
                return Response(json.dumps({
                    'status': 'bad_request',
                    'error': 'Product not found'
                }), status=400, mimetype='application/json')
            
            database_connection.close_session()
        else:
            return Response(json.dumps({
                'status': 'bad_request',
                'error': 'Missing required arguments'
            }), status=400, mimetype='application/json')
        
        return Response(json.dumps(Product.jsonformat(result)), status = 200, mimetype='application/json')

    except Exception as exc:
        return Response(json.dumps({
            'status': 'server_error',
            'error': str(exc)
        }), status=500, mimetype='application/json')
    
@app.route('/get_category', methods=['GET'])
def get_category():

    try:
        database_connection.start_session()
        cat_names = database_connection.get_categories()
        database_connection.close_session()
        return Response(json.dumps(cat_names), status = 200, mimetype='application/json')
    
    except Exception as exc:
        return Response(json.dumps({
            'status': 'server_error',
            'error': str(exc)
        }), status=500, mimetype='application/json')
    
if __name__ == '__main__':
        app.run(debug = True)