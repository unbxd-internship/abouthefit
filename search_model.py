from flask import Flask, request, Response
from table import Product, Base
import json
import requests
import math

class Search_Model:
    def __init__(self):
        self.link = "https://search.unbxd.io/fb853e3332f2645fac9d71dc63e09ec1/demo-unbxd700181503576558/search?"

    def validate(self, request_params):
        if 'q' in request_params:
            return True
        return False
    
    def sort_by(self, request_params):
        if 'sort' in request_params:
            sort = request_params['sort']
            if sort == 'price asce':
                self.link = self.link + "sort=price%20asce"
            elif sort == 'price desc':
                self.link = self.link + "sort=price%20desc"

    def get_page(self, request_params):
        if 'page' in request_params:
            page = int(request_params['page'])
        else:
            page = 1
        start_param = (page-1)*10
        self.link = self.link + "&start="+ str(start_param)+ "&rows=10"
        return page
    
    def validate_data(self, data):
        if not (
                'sku' in data and
                'title' in data and
                'productDescription' in data and
                'price' in data and
                'productImage' in data and
                'catlevel1Name' in data and
                'catlevel2Name' in data
        ):
            return False
        return True

    def format_response(self, response, page):
        result = {'products':[]}
        for i in response['products']:
            if Search_Model.validate_data(self, data = i):
                result['products'].append({'sku': i['sku'], 'title': i['title'], 'productdescription': i['productDescription'], 'price': i['price'], 'productimage': i['productImage'], 'catlevel1name': i['catlevel1Name'], 'catlevel2name': i['catlevel2Name']})
        count = response['numberOfProducts']
        numberOfPages = math.ceil(count/10)
        final_result = {'TotalNumberOfPages': numberOfPages, 'ProductCount': count , 'PageNumber': page,  'products':result}
        return final_result
    
    

        

