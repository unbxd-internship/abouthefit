import models.product_model as product_model
from models.database_model import Database_Model
from flask import Flask, request, Response
from models.table_model import Product, Base
import json
import requests
import math

class Product_Controller:

    def __init__(self):
        self.product_model = product_model.Product_Model()
        self.s = self.product_model.database_model.start_session()

    '''get product in the database based on the sku'''
    def get_product(self, sku):
        product = self.product_model.get_product(sku)
        if product:
            return product.jsonformat()
        return None