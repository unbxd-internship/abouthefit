from database_model import Database_Model

class Database_Controller:
    def __init__(self):
        self.database_model = Database_Model()

    def insert(self, data):
        self.database_model.start_session()
        self.database_model.insert(data)
        self.database_model.commit()
        self.database_model.close_session()
        return {"status": "success"}