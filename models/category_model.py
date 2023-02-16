from models.database_model import Database_Model
from flask import Flask, request, Response
from models.table_model import Product, Base
import json
import requests
import math

class Category_Model:
    def __init__(self):
        self.database_model = Database_Model()
        #self.s  = self.database_model.start_session()

    '''Sort the query based on the query parameters (relevancy is arbitrary)'''
    def sort_by(self, request_params, query):
        if 'sort' in request_params:
            sort = request_params['sort']
            if sort == 'price asce':
                query = query.order_by(Product.price.asc())
            elif sort == 'price desc':
                query = query.order_by(Product.price.desc())
        return query

    '''Get the page number from the query parameters, and accordingly get the start and end index of the query result'''
    def get_page(self, request_params):
        if 'page' in request_params:
            page = int(request_params['page'])
        else:
            page = 1
        start = (page-1)*10
        end = page*10
        return start, end, page

    '''Format the response to include necessary information'''
    def format_response(self, query_result, count, page):
        result = []
        for i in query_result:
            result.append(i.jsonformat())
        numberOfPages = math.ceil(count/10)
        final_result = {'TotalNumberOfPages': numberOfPages, 'ProductCount': count, 'PageNumber': page,  'products':result}
        return final_result
