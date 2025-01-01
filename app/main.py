from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import colleges_router
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
    allow_origins=["*"],  # Replace with your frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(colleges_router.router, prefix="/api", tags=["Colleges"])
# app.include_router(news_router.router, prefix="/api", tags=["News"])

# Health check endpoint
@app.get("/")
def read_root():
    return {"message": "Welcome to the College and News API!"}
