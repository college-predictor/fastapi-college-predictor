from app.models.counsellor_model import CounsellorModel
from app.schemas.counsellor_schema import CounsellorRequest, CounsellorResponse
from app.services.ai_counsellor import generate_response, generate_research
import uuid
from datetime import datetime
from typing import List, Optional
import os
from PIL import Image
import pytesseract
import PyPDF2

class CounsellorService:
    def __init__(self, counsellor_model: CounsellorModel):
        self.counsellor_model = counsellor_model

    def process_request(self, request: CounsellorRequest, file_path: Optional[str] = None) -> CounsellorResponse:
        # Extract text from file if provided
        if file_path:
            extracted_text = self.extract_text_from_file(file_path)
            request.message += f"\n[Extracted File Content]: {extracted_text}"

        # Generate AI response
        ai_response = generate_response(request.message)

        # Extract questions from AI response
        questions = self.extract_questions(ai_response)

        # Determine if research needs to be generated
        generate_research_flag = request.generate_research

        research_id = None
        if generate_research_flag:
            research_content = generate_research(ai_response)
            if research_content and research_content != "Research generation failed.":
                research_id = str(uuid.uuid4())
                research = {
                    "research_id": research_id,
                    "content": research_content,
                    "generated_at": datetime.utcnow().isoformat()
                }
                self.counsellor_model.save_research(research)

        # Save interaction to the database
        interaction = {
            "message": request.message,
            "ai_response": ai_response,
            "questions": questions,
            "generate_research": generate_research_flag,
            "research_id": research_id,
            "timestamp": datetime.utcnow().isoformat()
        }
        self.counsellor_model.save_counsellor_interaction(interaction)

        return CounsellorResponse(
            message_response=ai_response,
            questions=questions,
            generate_research_generation=generate_research_flag
        )

    def extract_questions(self, text: str) -> List[str]:
        lines = text.split('\n')
        questions = [line.strip() for line in lines if line.strip().endswith('?')]
        return questions

    def extract_text_from_file(self, file_path: str) -> str:
        file_extension = os.path.splitext(file_path)[1].lower()
        text = ""
        try:
            if file_extension == ".pdf":
                with open(file_path, "rb") as file:
                    reader = PyPDF2.PdfReader(file)
                    for page in reader.pages:
                        extracted = page.extract_text()
                        if extracted:
                            text += extracted + "\n"
            elif file_extension in [".jpg", ".jpeg", ".png"]:
                image = Image.open(file_path)
                text = pytesseract.image_to_string(image)
        except Exception as e:
            text = "[Failed to extract text from the uploaded file.]"
        return text