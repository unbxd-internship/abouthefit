from models.table_model import Base, Product, Category
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

class Database_Model:

    def __init__(self):
        self.db_string = "postgresql://unbxd:myPassword@database:5432/catalog"
        self.db = create_engine(self.db_string)
        self.Session = sessionmaker(bind=self.db)

    def create_table(self):
        Base.metadata.create_all(self.db)

    def validate_data(self, data):
        if not (
                'sku' in data and
                'title' in data and
                'productDescription' in data and
                'price' in data and
                'productImage' in data and
                'catlevel1Name' in data and
                'catlevel2Name' in data
        ):
            return False
        return True

    def insert_data(self, data):
        if self.validate_data(data):
            self.start_session()
            cat_id = data['catlevel1Name'] + data['catlevel2Name']
            cat_id = str(hash(cat_id))
            data_product = {'sku': data['sku'], 'title': data['title'], 'productdescription': data['productDescription'], 'price': data['price'], 'productimage': data['productImage'], 'cat_id': cat_id}
            try:
                self.s.add(Product(**data_product))
            except Exception as e:
                return False
            data_category = {'cat_id': cat_id, 'catlevel1name': data['catlevel1Name'], 'catlevel2name': data['catlevel2Name']}
            if self.s.query(Category).filter_by(cat_id = data_category['cat_id']).first() == None:
                self.s.add(Category(**data_category))
            self.commit()
            self.close_session()
            return True
        return False

    def delete_table(self):
        Base.metadata.drop_all(self.db)

    def execute_query(self, query, start = 0, end = 0):
        if start==end:
            result = query.first()
        else:
            result = query.slice(start, end).all()
        return result

    def get_count(self, query):
        count = query.count()
        return count

    def commit(self):
        self.s.commit()

    def start_session(self):
        self.s = self.Session()
        return self.s

    def close_session(self):
        self.s.close()

