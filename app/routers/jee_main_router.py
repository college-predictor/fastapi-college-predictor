from fastapi import APIRouter, Body, Request, HTTPException
import json
import asyncio
from app.services.jee_main_services import save_url_in_mongo, calculate_marks

router = APIRouter(prefix="/jee-main")


async def process_url(url: str):
    """
    Process the URL asynchronously
    
    Args:
        url: The URL to process
        
    Returns:
        None
    """
    # Empty function where URL can be processed freely
    # This function runs in the background and doesn't block the response
    try:
        # Process the URL (currently just saving to MongoDB)
        status = save_url_in_mongo(url)
        status.get("is_url_present", True)
        # Add any additional processing logic here
    except Exception as e:
        print(f"Error processing URL: {e}")


@router.post("/calculate-marks")
async def get_colleges(request: Request):
    """
    Calculate marks based on any payload
    
    Args:
        request: The full request object to access raw payload
        
    Returns:
        dict: Response containing the received payload and other information
    """
    try:
        body = await request.json()
    except json.JSONDecodeError:
        raise HTTPException(status_code=400, detail="Invalid JSON payload")
    
    url = body.get("url")
    if not url:
        raise HTTPException(status_code=400, detail="URL is required")
    
    # Start processing URL in the background without waiting for it to complete
    asyncio.create_task(process_url(url))

    return calculate_marks(url)
    