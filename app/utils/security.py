from fastapi import Header, HTTPException
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()
API_KEY = os.getenv("API_KEY")

def validate_api_key(x_api_key: str = Header(...)):
    """
    Validates the API key from the x-api-key header.
    Raises HTTPException if the key is invalid.
    """
    if x_api_key != API_KEY:
        raise HTTPException(status_code=403, detail="Forbidden: Invalid API Key")
