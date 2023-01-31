from table import Product
import json
from flask import Flask, request, Response
from flask_cors import CORS
import requests
import math
import category_controller
import search_controller
import product_controller
import json_to_db_pipeline
import database_model
# from category_controller import Category_Controller as category_controller
# from search_controller import Search_Controller as search_controller
# from product_controller import Product_Controller as product_controller

app = Flask(__name__)
CORS(app)

@app.route('/insert', methods=['POST'])
def insert():
    #print("insert")
    if request.json:
        json_data = request.json
        #print(json_data)
        database_model_obj = database_model.Database_Model()
        if database_model_obj.validate_data(json_data):
            try:
                #print("here")
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
    try:
        #print("get_category")
        category_controller_obj =  category_controller.Category_Controller()

        cat_headers, sub_cats = category_controller_obj.get_category()

        if cat_headers and sub_cats:
            return Response(json.dumps({"cat_headers": cat_headers, "sub_cats": sub_cats}), status = 200, mimetype='application/json')
        
        else:
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
    try:
        #print("category")
    
        category_controller_obj =  category_controller.Category_Controller()
        if categorylevel1 is None:
            result = category_controller_obj.get_all(request_params = request.args)
        elif categorylevel2 is None:
            result = category_controller_obj.get_category1(request_params = request.args, catlevel1Name = categorylevel1)
        else:
            result = category_controller_obj.get_category2(request_params = request.args, catlevel1Name=categorylevel1, catlevel2Name=categorylevel2)

        if result:
            return Response(json.dumps(result), status = 200, mimetype='application/json')
        
        else:
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
    try:
        #print("search")
        search_controller_obj =  search_controller.Search_Controller()
        result = search_controller_obj.get_search(request.args)
        if result:
            return Response(json.dumps(result), status = 200, mimetype='application/json')
        
        else:
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
    try:
        #print("product")
        product_controller_obj =  product_controller.Product_Controller()
        result = product_controller_obj.get_product(product_id)
        if result:
            return Response(json.dumps(result), status = 200, mimetype='application/json')
        
        else:
            return Response(json.dumps({
                'status': 'bad_request',
                'error': 'Missing required arguments'
            }), status=400, mimetype='application/json')
    
    except Exception as exc:
        return Response(json.dumps({
            'status': 'server_error',
            'error': str(exc)
        }), status=500, mimetype='application/json')

if __name__ == '__main__':
    app.run(debug=True)