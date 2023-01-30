from table import Base, Product
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

class database_connection:

    def __init__(self):
        self.db_string = "postgresql://unbxd:myPassword@localhost:5432/catalog"
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
            self.s.add(Product(**data))
            #self.commit()
            return True
        return False
    
    def delete_table(self):
        Base.metadata.drop_all(self.db)


    def get_data(self, request_params):

        query = self.s.query(Product)
        #print(request_params)
        if 'sku' in request_params:
            sku = request_params['sku']
            result = query.filter(Product.sku == sku).first()
            return result
        
        if 'catlevel1Name' in request_params:
            catlevel1Name = request_params['catlevel1Name']
            query = query.filter(Product.catlevel1name == catlevel1Name)

        if 'catlevel2Name' in request_params:
            catlevel2Name = request_params['catlevel2Name']
            query = query.filter(Product.catlevel2name == catlevel2Name)

        if 'sort' in request_params:
            sort = request_params['sort']
            if sort == 'price asce':
                query = query.order_by(Product.price.asc())
            elif sort == 'price desc':
                query = query.order_by(Product.price.desc())
            
        if 'page' in request_params:
            page = int(request_params['page'])
        else:
            page = 1

        start = (page-1)*10
        end = page*10

        result_count = query.count()
        result_temp = query.slice(start, end).all()
        
        results = (result_temp, result_count)
        
        return results

    def get_categories(self):
        catlevels = {}
        for i in self.s.query(Product).all():
            if i.catlevel1name not in catlevels:
                catlevels[i.catlevel1name] = []
            else:
                if i.catlevel2name not in catlevels[i.catlevel1name]:
                    catlevels[i.catlevel1name].append(i.catlevel2name)
        return(catlevels)
    
    def commit(self):
        self.s.commit()

    def start_session(self):
        self.s = self.Session()

    def close_session(self):
        self.s.close()

    