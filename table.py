from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Float

Base = declarative_base()

class Product(Base):
    __tablename__ = 'products'
    sku = Column(String, primary_key=True)
    title = Column(String)
    productDescription = Column(String)
    price = Column(Float)
    productImage = Column(String)
    catlevel1Name = Column(String)
    catlevel2Name = Column(String)

    def __repr__(self):
        return "<Product(sku='{}', title='{}', productDescription='{}', price = '{}', productImage = '{}', catlevel1Name = '{}', catlevel2Name = '{}')>"\
                .format(self.sku, self.title, self.productDescription, self.price, self.productImage, self.catlevel1Name, self.catlevel2Name)

