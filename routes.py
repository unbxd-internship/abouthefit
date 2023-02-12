'''API Routes for the application'''
import pickle
import json
import redis
from flask import Flask, request, Response
from flask_cors import CORS
from controllers import category_controller, search_controller, product_controller
from models import database_model
import requests

app = Flask(__name__)
database_model_obj = database_model.Database_Model()
product_controller_obj = product_controller.Product_Controller()
category_controller_obj =  category_controller.Category_Controller()
CORS(app)
redis_cache = redis.Redis(host='redis', port=6379, db=0)

def cache(key, value= None, ttl= None):
    '''Function defining the cache'''
    if value:
        if ttl:
            redis_cache.setex(key, ttl, pickle.dumps(value))
        else:
            redis_cache.set(key, pickle.dumps(value))
    else:
        value = redis_cache.get(key)
        if value:
            return pickle.loads(value)
    return None


@app.route('/check', methods=['GET'])
def check():
    '''Check if the app is up and running on Docker'''
    return Response(json.dumps({
        'status': 'on docker'
    }), status=200, mimetype='application/json')


@app.route('/insert', methods=['POST'])
def insert():
    '''Insert json data into the database'''
    if request.json:
        json_data = request.json
        if database_model_obj.validate_data(json_data):
            try:
                database_model_obj.start_session()
                database_model_obj.insert_data(json_data)
                database_model_obj.commit()
                database_model_obj.close_session()
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
    else:
        return Response(json.dumps({
            'status': 'bad_request',
            'error': 'Missing payload'
        }), status=400, mimetype='application/json')



@app.route('/get_category', methods=['GET'])
def get_category():
    '''Get the category headers and sub categories'''
    try:
        cat_headers, sub_cats = category_controller_obj.get_category()

        if cat_headers and sub_cats:
            return Response(json.dumps(
                {"cat_headers": cat_headers, "sub_cats": sub_cats}),
                  status = 200, mimetype='application/json')

        return Response(json.dumps({
            'status': 'bad_request',
            'error': 'Missing required arguments'
        }), status=400, mimetype='application/json')

    except Exception as exc:
        return Response(json.dumps({
            'status': 'server_error',
            'error': str(exc)
        }), status=500, mimetype='application/json')

@app.route('/', methods=['GET'])
@app.route('/home', methods=['GET'])
@app.route('/category', methods=['GET'])
@app.route('/category/', methods=['GET'])
@app.route('/category/<categorylevel1>', methods=['GET'])
@app.route('/category/<categorylevel1>/', methods=['GET'])
@app.route('/category/<categorylevel1>/<categorylevel2>', methods=['GET'])
@app.route('/category/<categorylevel1>/<categorylevel2>/', methods=['GET'])
def category(categorylevel1=None, categorylevel2=None):
    '''Get product details based on category/categories selected'''
    try:
        cached = cache(request.url)
        if cached:
            return Response(json.dumps(cached), status = 200, mimetype='application/json')
        result = category_controller_obj.get(catlevel1Name = categorylevel1,catlevel2Name= categorylevel2,request_params = request.args)
        if result:
            cache(request.url, result, ttl = 3600)
            return Response(json.dumps(result), status = 200, mimetype='application/json')

        return Response(json.dumps({
            'status': 'bad_request',
            'error': 'Missing required arguments'
        }), status=400, mimetype='application/json')

    except Exception as exc:
        return Response(json.dumps({
            'status': 'server_error',
            'error': str(exc)
        }), status=500, mimetype='application/json')

@app.route('/search', methods=['GET'])
def search():
    '''Get product details based on search query'''
    search_controller_obj = search_controller.Search_Controller()
    try:
        result = search_controller_obj.get_search(request.args)
        if result:
            return Response(json.dumps(result), status = 200, mimetype='application/json')

        return Response(json.dumps({
            'status': 'bad_request',
            'error': 'Missing required arguments'
        }), status=400, mimetype='application/json')

    except Exception as exc:
        return Response(json.dumps({
            'status': 'server_error',
            'error': str(exc)
        }), status=500, mimetype='application/json')

@app.route('/product/<product_id>', methods=['GET'])
def product(product_id):
    '''Get product details based on product id'''
    try:
        result = product_controller_obj.get_product(product_id)
        if result:
            return Response(json.dumps(result), status = 200, mimetype='application/json')

        return Response(json.dumps({
            'status': 'bad_request',
            'error': 'Missing required arguments'
        }), status=400, mimetype='application/json')

    except Exception as exc:
        return Response(json.dumps({
            'status': 'server_error',
            'error': str(exc)
        }), status=500, mimetype='application/json')
