from models.rec_model import rec_model
import json
import requests
import math
import json
import pandas as pd

class Rec_Controller:
    def __init__(self):
        self.rec_model_obj = rec_model()
        self.cosine_similarities, self.ds = self.rec_model_obj.get_cosine()

    def get_recs(self, sku):
        results = {}
        for idx, row in self.ds.iterrows():
            similar_indices = self.cosine_similarities[idx].argsort()[:-100:-1]
            similar_items = [(self.cosine_similarities[idx][i], self.ds['sku'][i]) for i in similar_indices]

            results[row['sku']] = similar_items[1:]

        recommended_items =  self.recommend(results,sku,5)
        return recommended_items

    def item(self, id):
        return self.ds.loc[self.ds['sku'] == id]['productDescription'].tolist()[0].split(' - ')[0]

    def recommend(self, results, item_id, num):
        recs = results[item_id][:num]
        recommended_items = []
        for rec in recs:
            sku = rec[1]
            desc = self.item(sku)
            score = rec[0]
            recommended_items.append({"sku": sku, "description": desc, "score": score})
        return recommended_items