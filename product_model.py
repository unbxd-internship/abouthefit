from database_model import Database_Model
from flask import Flask, request, Response
from table import Product, Base
import json
import requests
import math

class Product_Model:
    def __init__(self):
        self.database_model = Database_Model()
        self.s  = self.database_model.start_session()
        self.product = Product()

    def get_product(self, sku):
        #print(sku)
        query = self.s.query(Product)
        query = query.filter(Product.sku == sku)
        product = self.database_model.execute_query(query)
        if product:
            return product
        return None