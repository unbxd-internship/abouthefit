from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Float
import json

Base = declarative_base()

class Category(Base):
    __tablename__ = 'categories'
    catlevel1name = Column(String)
    catlevel2name = Column(String)
    cat_id = Column(String, primary_key=True)

    def __repr__(self):
        return "<Category(catlevel1name='{}', catlevel2name='{}', cat_id = '{}')>".format(self.catlevel1name, self.catlevel2name, self.cat_id)
    
    def jsonformat(self):
        return {"catlevel1name": self.catlevel1name, "catlevel2name": self.catlevel2name, "cat_id": self.cat_id}

class Product(Base):
    __tablename__ = 'products'
    sku = Column(String, primary_key=True)
    title = Column(String)
    productdescription = Column(String)
    price = Column(Float)
    productimage = Column(String)
    cat_id = Column(String)
    # catlevel1name = Column(String)
    # catlevel2name = Column(String)
    cat_id = Column(String)

    def jsonformat(self):
        return {"sku": self.sku, "title": self.title, "productdescription": self.productdescription, "price": self.price, "productimage": self.productimage, "cat_id": self.cat_id}

    def __repr__(self):
        #return {"sku": self.sku, "title": self.title, "productdescription": self.productdescription, "price": self.price, "productimage": self.productimage, "catlevel1name": self.catlevel1name, "catlevel2name": self.catlevel2name}
        return "<Product(sku='{}', title='{}', productdescription='{}', price='{}', productimage='{}', cat_id = '{}')>".format(self.sku, self.title, self.productdescription, self.price, self.productimage, self.cat_id)
