class NewsService:
    def __init__(self, news_model):
        self.news_model = news_model

    def fetch_news(self):
        return self.news_model.get_all_news()
