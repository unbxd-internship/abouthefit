from flask import Flask, request, Response
from table import Product, Base
import json
import requests
import math
import category_model

class Category_Controller:

    def __init__(self):
        self.category_model = category_model.Category_Model()
        self.s = self.category_model.database_model.start_session()

    def get_category(self):
        catlevels = {}
        for i in self.s.query(Product).all():
            if i.catlevel1name not in catlevels:
                catlevels[i.catlevel1name] = []
            else:
                if i.catlevel2name not in catlevels[i.catlevel1name]:
                    catlevels[i.catlevel1name].append(i.catlevel2name)
        self.category_model.database_model.close_session()
        return(list(catlevels.keys()),catlevels)
        
    def get_all(self, request_params):
        query = self.s.query(Product)
        query = self.category_model.sort_by(request_params, query)
        start, end, page = self.category_model.get_page(request_params)
        query_result = self.category_model.database_model.execute_query(query, start, end)
        count = self.category_model.database_model.get_count(query)
        final_result = self.category_model.format_response(query_result, count, page)
        self.category_model.database_model.close_session()
        return final_result

    def get_category1(self, request_params, catlevel1Name):
        query = self.s.query(Product)
        query = query.filter(Product.catlevel1name == catlevel1Name)
        query = self.category_model.sort_by(request_params, query)
        start, end, page = self.category_model.get_page(request_params)  
        query_result = self.category_model.database_model.execute_query(query, start, end)
        count = self.category_model.database_model.get_count(query)
        final_result = self.category_model.format_response(query_result, count, page)
        self.category_model.database_model.close_session()
        return final_result

    def get_category2(self, request_params, catlevel1Name, catlevel2Name):
        query = self.s.query(Product)
        query = query.filter(Product.catlevel2name == catlevel2Name and Product.catlevel1name == catlevel1Name)
        query = self.category_model.sort_by(request_params, query)
        start, end, page = self.category_model.get_page(request_params)
        query_result = self.category_model.database_model.execute_query(query, start, end)
        count = self.category_model.database_model.get_count(query)
        final_result = self.category_model.format_response(query_result, count, page)
        self.category_model.database_model.close_session()
        return final_result
