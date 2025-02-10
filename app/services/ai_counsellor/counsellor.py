# main.py
import os
import time
import logging
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from session_manager import get_session, create_session, check_session, SyncRequired, compute_hash
from typing import Dict

# (Assume your OpenAI API key is set as needed.)
API_KEY = os.environ.get("OPENAI_API_KEY", "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") # sk-proj-h2ACTULQJBaXBC9K16gXT3BlbkFJVAHzm0cl1pUahrAz98Zi

app = FastAPI()

# Enable CORS for your SvelteKit frontend (adjust allowed origins)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Note: Here we use a default value of None for chat_hash (instead of False)
class ChatRequest(BaseModel):
    chat_id: str
    messages: list = []  # This can be the full conversation (sync) or the minimal update.
    prompt: str = None
    chat_hash: str = None
    sync_required: bool = False

@app.post("/api/chat/generate-text")
async def generate_text(chat_req: ChatRequest):
    # print(chat_req)
    logging.debug(f"Received generate-text request: {chat_req}")
    
    if check_session(chat_req.chat_id):
        print("Session exists")
        chatbot = get_session(chat_req.chat_id)

        if chat_req.sync_required:
            print("Sync required by client")
            # Client requested a full sync of the conversation.
            chatbot.conversation = chat_req.messages

        if not chat_req.chat_hash:
            print("No chat hash provided")
            # Session exists, but no hash was provided. Tell the client to do a full-sync.
            return JSONResponse(
                status_code=409,
                content={"detail": "Session exists but no hash provided. Please sync full conversation.", "sync_required": True}
            )
        if chat_req.chat_hash == compute_hash(chatbot.conversation):
            print("Session exists and messages are synced")
            response_text = chatbot.generate_text_response(chat_req.prompt)
            return {"response": response_text}
        else:
            print("Session exists but messages are not synced")
            # Session exists, but sync is different. Tell the client to do a full-sync.
            return JSONResponse(
                status_code=409,
                content={"detail": "Session exist but messages are not synced", "sync_required": True}
            )
    else:
        print("Session does not exist")
        # No (or expired) session exists – we expect a full conversation for initialization.
        chatbot = create_session(chat_id=chat_req.chat_id, api_key=API_KEY)
        return JSONResponse(
            status_code=409,
            content={"detail": "Session does not exist creating new session. Please send full conversation and with sync_required as 'True'", "sync_required": True}
        )