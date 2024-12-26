from fastapi import APIRouter
from app.schemas.news_today_schema import NewsSchema
from app.config.database import MongoDB
from app.models.news_today_model import NewsModel
from app.services.news_today_service import NewsService

router = APIRouter()

db_client = MongoDB()
db_client.connect('college-predictor-dev')
news_model = NewsModel(db_client)
news_service = NewsService(news_model)

@router.get("/news", response_model=list[NewsSchema])
def get_news():
    return news_service.fetch_news()
