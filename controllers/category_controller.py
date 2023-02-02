from flask import Flask, request, Response
from models.table_model import Product, Base, Category
import json
import requests
import math
import models.category_model as category_model

class Category_Controller:

    def __init__(self):
        self.category_model = category_model.Category_Model()
        self.s = self.category_model.database_model.start_session()

    def get_category(self):
        catlevels = {}
        for i in self.s.query(Product.cat_id.distinct()).all():
            catlevel1name, catlevel2name = self.s.query(Category.catlevel1name, Category.catlevel2name).filter(Category.cat_id == i[0]).first()
            if catlevel1name not in catlevels:
                catlevels[catlevel1name] = []
            else:
                if catlevel2name not in catlevels[catlevel1name]:
                    catlevels[catlevel1name].append(catlevel2name)
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
        cat_query = self.s.query(Category)
        cat_query = cat_query.filter(Category.catlevel1name == catlevel1Name)
        cat_query = cat_query.with_entities(Category.cat_id)
        query = self.s.query(Product)
        query = query.filter(Product.cat_id.in_(cat_query))
        query = self.category_model.sort_by(request_params, query)
        start, end, page = self.category_model.get_page(request_params)  
        query_result = self.category_model.database_model.execute_query(query, start, end)
        count = self.category_model.database_model.get_count(query)
        final_result = self.category_model.format_response(query_result, count, page)
        self.category_model.database_model.close_session()
        return final_result

    def get_category2(self, request_params, catlevel1Name, catlevel2Name):
        cat_query = self.s.query(Category)
        cat_query = cat_query.filter(Category.catlevel1name == catlevel1Name)
        cat_query = cat_query.filter(Category.catlevel2name == catlevel2Name)
        cat_query = cat_query.with_entities(Category.cat_id)
        query = self.s.query(Product)
        query = query.filter(Product.cat_id.in_(cat_query))
        query = self.category_model.sort_by(request_params, query)
        start, end, page = self.category_model.get_page(request_params)  
        query_result = self.category_model.database_model.execute_query(query, start, end)
        count = self.category_model.database_model.get_count(query)
        final_result = self.category_model.format_response(query_result, count, page)
        self.category_model.database_model.close_session()
        return final_result