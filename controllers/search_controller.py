
from flask import Flask, request, Response
from models.table_model import Product, Base
import json
import requests
import math
import models.search_model as search_model

class Search_Controller:
    def __init__(self):
        self.search_model = search_model.Search_Model()
        
    def get_search(self, request_params):
        if 'q' in request_params:
            query = request_params['q']
            self.search_model.link = self.search_model.link + "q=" + query
        
        self.search_model.sort_by(request_params)
        page = self.search_model.get_page(request_params)

        response = json.loads(requests.get(self.search_model.link).content)['response']

        final_result = self.search_model.format_response(response, page)
        return final_result