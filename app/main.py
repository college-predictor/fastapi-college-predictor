from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import colleges_router, chat_router, discussion_forum_router, features_router, jee_main_router
from app.utils.security import validate_api_key

# Create FastAPI app instance
app = FastAPI(
    title="College and News API",
    description="API to fetch college information and news articles, secured with API key authentication.",
    version="1.0.0",
)

# Configure CORS if your frontend is hosted elsewhere
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://localhost:3000", "https://collegepredictor.in", "http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(colleges_router.router, prefix="/api", tags=["Colleges"])
# app.include_router(news_router.router, prefix="/api", tags=["News"])
# app.include_router(chat_router.router, prefix="/api", tags=["Chat"])
app.include_router(discussion_forum_router.router, prefix="/api", tags=["Discussion Forum"])
app.include_router(features_router.router, prefix="/api", tags=["Features"])
app.include_router(jee_main_router.router, prefix="/api", tags=["JEE-Mains"])

# Health check endpoint
@app.get("/")
def read_root():
    return {"message": "Welcome to the College and News API!"}
