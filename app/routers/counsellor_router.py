from fastapi import APIRouter, Depends, File, UploadFile, HTTPException, status
from app.schemas.counsellor_schema import CounsellorRequest, CounsellorResponse
from app.models.counsellor_model import CounsellorModel
from app.services.counsellor_service import CounsellorService
from app.config.database import MongoDB
from typing import Optional
import shutil
import os
import uuid

router = APIRouter(prefix="/counsellor", tags=["Counsellor"])

def get_counsellor_service():
    db_client = MongoDB()
    db_client.connect()
    counsellor_model = CounsellorModel(db_client)
    return CounsellorService(counsellor_model)

@router.post("/interact", response_model=CounsellorResponse)
async def interact_counsellor(
    message: str,
    generate_research: Optional[bool] = False,
    file: Optional[UploadFile] = File(None),
    counsellor_service: CounsellorService = Depends(get_counsellor_service)
):
    """
    Interact with the AI counsellor by sending a message and optionally a file.
    """
    # Handle file if provided
    if file:
        file_path = save_upload_file(file)
    else:
        file_path = None

    # Create CounsellorRequest
    request = CounsellorRequest(message=message, generate_research=generate_research)

    # Process the request
    response = counsellor_service.process_request(request, file_path=file_path)

    return response

def save_upload_file(upload_file: UploadFile) -> str:
    """
    Saves the uploaded file to the 'uploads' directory and returns the file path.
    """
    upload_dir = "uploads"
    os.makedirs(upload_dir, exist_ok=True)
    file_extension = os.path.splitext(upload_file.filename)[1]
    if file_extension.lower() not in [".pdf", ".jpg", ".jpeg", ".png"]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Unsupported file type. Only PDF and image files are allowed."
        )
    unique_filename = f"{uuid.uuid4()}{file_extension}"
    file_path = os.path.join(upload_dir, unique_filename)
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(upload_file.file, buffer)
    return file_path