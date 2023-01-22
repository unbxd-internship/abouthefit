from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Float

Base = declarative_base()

class Product(Base):
    __tablename__ = 'products'
    sku = Column(String, primary_key=True)
    title = Column(String)
    productdescription = Column(String)
    price = Column(Float)
    productimage = Column(String)
    catlevel1name = Column(String)
    catlevel2name = Column(String)

    def jsonformat(self):
        return {"sku": self.sku, "title": self.title, "productdescription": self.productdescription, "price": self.price, "productimage": self.productimage, "catlevel1name": self.catlevel1name, "catlevel2name": self.catlevel2name}

    def __repr__(self):
        return "<Product(sku='{}', title='{}', productdescription='{}', price = '{}', productimage = '{}', catlevel1name = '{}', catlevel2name = '{}')>"\
                .format(self.sku, self.title, self.productdescription, self.price, self.productimage, self.catlevel1name, self.catlevel2name)

