import uvicorn
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

if __name__ == "__main__":
    # Configure and run the FastAPI application using Uvicorn
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",  # Allows external access
        port=8000,       # Default port
        reload=True,     # Enable auto-reload for development
        workers=1        # Number of worker processes
    )