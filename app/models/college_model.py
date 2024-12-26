from app.config.database import MongoDB

class CollegeModel:
    def __init__(self, db_client: MongoDB):
        self.collection = db_client.get_collection("colleges")

    def get_colleges(self, criteria: dict):
        return list(self.collection.find(criteria, {"_id": 0}))
