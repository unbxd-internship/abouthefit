from flask import Flask, request, Response
from models.table_model import Product, Base
import json
import requests
import math

'''Search model - contains formatting and validation functions'''
class Search_Model:
    def __init__(self):
        self.link = "https://search.unbxd.io/fb853e3332f2645fac9d71dc63e09ec1/demo-unbxd700181503576558/search?"

    '''Funtction to validate the search query'''
    def validate(self, request_params):
        if 'q' in request_params:
            return True
        return False

    '''Function to format the search query with sort'''
    def sort_by(self, request_params):
        if 'sort' in request_params:
            sort = request_params['sort']
            if sort == 'price asce':
                self.link = self.link + "&sort=price asce"
            elif sort == 'price desc':
                self.link = self.link + "&sort=price desc"

    '''Function to format the search query with pagination'''
    def get_page(self, request_params):
        if 'page' in request_params:
            page = int(request_params['page'])
        else:
            page = 1
        start_param = (page-1)*10
        self.link = self.link + "&start="+ str(start_param)+ "&rows=10"
        return page

    '''Function to validate the data from the response'''
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

    '''Function to format the response'''
    def format_response(self, response, page):
        result = []
        for i in response['products']:
            if Search_Model.validate_data(self, data = i):
                result.append({'sku': i['sku'], 'title': i['title'], 'productdescription': i['productDescription'], 'price': i['price'], 'productimage': i['productImage'], 'catlevel1name': i['catlevel1Name'], 'catlevel2name': i['catlevel2Name']})
        count = response['numberOfProducts']
        numberOfPages = math.ceil(count/10)
        final_result = {'TotalNumberOfPages': numberOfPages, 'ProductCount': count , 'PageNumber': page,  'products':result}
        return final_result
