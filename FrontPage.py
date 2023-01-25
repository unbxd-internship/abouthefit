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

@app.route('/get_category', methods = ['GET'])
def get_category():
        #get all the categories
        try:
                s = Session()
                result_temp = s.query(Product).all()
                s.close()
                #response = []
                catlevel1 = []
                catlevel2 = []
                for row in result_temp:
                        if row.catlevel1name not in catlevel1:
                                catlevel1.append(row.catlevel1name)
                        if row.catlevel2name not in catlevel2:
                                catlevel2.append(row.catlevel2name)
                return Response(json.dumps({'catlevel1Name': catlevel1, 'catlevel2Name': catlevel2}), status = 200, mimetype='application/json')
        
        except Exception as exc:
                #server error
                return Response(json.dumps({
                        'status': 'server_error',
                        'error': str(exc)
                }), status=500, mimetype='application/json')
        
@app.route("/", methods=["GET"])
def start():
    if 'page' in request.args:
        page = int(request.args['page'])
    else:
        page = 1
    start = (page-1)*10
    end = page*10
    s = Session()
    if 'sort' in request.args:
        sort = request.args['sort']    
    
        if sort == 'price asc':
            result_temp = s.query(Product).order_by(Product.price).slice(start, end).all()
        elif sort == 'price desc':
            result_temp = s.query(Product).order_by(Product.price.desc()).slice(start, end).all()
        else:
            result_temp = s.query(Product).slice(start, end).all()
    else:
          result_temp = s.query(Product).slice(start, end).all()
    count_products = s.query(Product).count()
    s.close()
    result_products = []
    for product in result_temp:
          result_products.append(Product.jsonformat(product))

    numberOfPages = math.ceil(count_products/10)
    
    return Response(json.dumps({'TotalNumberOfPages': numberOfPages, 'ProductCount': count_products, 'PageNumber': page,  'products':result_products}), status = 200, mimetype='application/json')

    #return Response(, mimetype="application/json")

if __name__ == '__main__':
        app.run(debug = True)
