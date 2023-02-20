from models.database_model import Database_Model
from flask import Flask, request, Response, jsonify
from models.table_model import Product, Base
import json
import requests
import math
import json
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel
import numpy as np


class rec_model:
    def __init__(self):
        self.database_model = Database_Model()
        self.s  = self.database_model.start_session()
        self.product = Product()

    def get_cosine(self):
        query = self.s.query(Product)

        products = query.all()
        ds = pd.DataFrame([(p.sku, p.productdescription) for p in products], columns=['sku', 'productDescription'])

        tf = TfidfVectorizer(analyzer='word', ngram_range=(2, 3), min_df=0, stop_words='english')
        tfidf_matrix = tf.fit_transform(ds['productDescription'].astype('U').values)

        cosine_similarities = linear_kernel(tfidf_matrix, tfidf_matrix)

        return cosine_similarities, ds

