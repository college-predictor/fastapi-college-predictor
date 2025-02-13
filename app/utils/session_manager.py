# app/utils/session_manager.py

import time
import threading
import logging
import hashlib
import json
from app.services.chat_service import OpenAIChatbot

# Dictionary to hold sessions: { chat_id: (chatbot_instance, last_used_timestamp) }
sessions = {}

# Custom exception to indicate that a full sync is required.
class SyncRequired(Exception):
    pass

# Time-to-live for sessions (in seconds)
SESSION_TTL = 60 * 60  # e.g., 60 minutes


def compute_hash(messages: list) -> str:
    """
    Compute a hash of the conversation using a consistent serialization format.
    """
    messages_str = json.dumps(messages, ensure_ascii=False, separators=(',', ':'), sort_keys=True)  # Enforce consistent order
    return hashlib.md5(messages_str.encode("utf-8")).hexdigest()



def check_session(chat_id) -> bool:
    now = time.time()
    if chat_id in sessions:
        _, last_used = sessions[chat_id]
        # Check if the session is expired.
        if now - last_used > SESSION_TTL:
            return False
        return True
    return False


def get_session(chat_id: str) -> OpenAIChatbot:
    """
    Retrieve an existing session and update its last-used timestamp.
    """
    now = time.time()
    if chat_id in sessions:
        session, _ = sessions[chat_id]
        sessions[chat_id] = (session, now)
        return session
    else:
        raise SyncRequired("Session not found, please sync full conversation.")


def create_session(chat_id: str, client_messages: list = [], api_key: str = None):
    logging.debug(f"Creating new session for chat_id: {chat_id}")
    session = OpenAIChatbot(api_key)
    session.conversation = client_messages
    sessions[chat_id] = (session, time.time())
    return session


def cleanup_sessions():
    while True:
        now = time.time()
        expired = [
            chat_id
            for chat_id, (_, last_used) in sessions.items()
            if now - last_used > SESSION_TTL
        ]
        for chat_id in expired:
            logging.info(f"Cleaning up session {chat_id} (expired)")
            del sessions[chat_id]
        time.sleep(300)  # Clean up every 5 minutes


# Start a background cleanup thread.
cleanup_thread = threading.Thread(target=cleanup_sessions, daemon=True)
cleanup_thread.start()
