class NewsModel:
    def __init__(self, db_client):
        self.collection = db_client.get_collection("news")

    def get_all_news(self):
        return list(self.collection.find({}, {"_id": 0}))
