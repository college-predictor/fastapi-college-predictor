# app/routers/chat_router.py

import os
import logging
from fastapi import APIRouter
from fastapi.responses import JSONResponse
from pydantic import BaseModel

# Import our chat service and session manager utilities
from app.services.chat_service import OpenAIChatbot
from app.utils.session_manager import (
    check_session,
    get_session,
    create_session,
    compute_hash,
    SyncRequired,
)

# It’s common to retrieve sensitive keys from the environment.
API_KEY = os.environ.get("OPENAI_API_KEY", "your-default-openai-api-key")

router = APIRouter()


class ChatRequest(BaseModel):
    chat_id: str
    messages: list = []  # Full conversation (for sync)
    prompt: str = None
    chat_hash: str = None
    sync_required: bool = False


@router.post("/chat/generate-text")
async def generate_text(chat_req: ChatRequest):
    logging.debug(f"Received generate-text request: {chat_req}")

    # Check if a session for the given chat_id already exists
    if check_session(chat_req.chat_id):
        print("Session exists")
        chatbot = get_session(chat_req.chat_id)

        if chat_req.sync_required:
            print("Syncing full conversation")
            # Replace the conversation with the client’s full conversation if requested
            chatbot.conversation = chat_req.messages

        if not chat_req.chat_hash:
            print("No hash provided. Sync required.")
            return JSONResponse(
                status_code=409,
                content={
                    "detail": "Session exists but no hash provided. Please sync full conversation.",
                    "sync_required": True,
                },
            )

        # Verify that the client’s conversation hash matches our session’s conversation
        if chat_req.chat_hash == compute_hash(chatbot.conversation):
            print("Hash matched. Generating response.")
            response_text = chatbot.generate_text_response(chat_req.prompt)
            return {"response": response_text}
        else:
            print("Hash mismatch. Sync required.")
            print("Client hash:", chat_req.chat_hash)
            print("Server hash:", compute_hash(chatbot.conversation))
            print("Client conversation:", chat_req.messages)
            print("Server conversation:", chatbot.conversation)
            return JSONResponse(
                status_code=409,
                content={
                    "detail": "Session exists but messages are not synced.",
                    "sync_required": True,
                },
            )
    else:
        # No valid session exists, so create a new one.
        chatbot = create_session(chat_id=chat_req.chat_id, api_key=API_KEY)
        return JSONResponse(
            status_code=409,
            content={
                "detail": "Session does not exist. Creating new session. Please send full conversation with sync_required=True.",
                "sync_required": True,
            },
        )
