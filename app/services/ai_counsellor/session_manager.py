# session_manager.py
import time
import threading
import logging
import hashlib
import json
from chatbot import OpenAIChatbot  # your chatbot implementation

# Global dictionary to hold sessions:
# sessions: { chat_id: (chatbot_instance, last_used_timestamp) }
sessions = {}

# Custom exception to indicate that a full sync is required.
class SyncRequired(Exception):
    pass

# TTL for sessions (in seconds)
SESSION_TTL = 60 * 60  # 60 minutes

def compute_hash(messages: list) -> str:
    """
    Compute a simple hash (using MD5) of the conversation messages 
    but using a JSON stringification style closer to JavaScript's JSON.stringify().
    """
    messages_str = json.dumps(messages, separators=(',', ':'))  # No extra spaces
    return hashlib.md5(messages_str.encode('utf-8')).hexdigest()

def check_session(chat_id) -> bool:
    now = time.time()
    if chat_id in sessions:
        session, last_used = sessions[chat_id]
        # Check if the session is expired.
        if now - last_used > SESSION_TTL:
            return False
        return True
    return False

def get_session(chat_id: str):
    """
    Retrieves an existing session and verifies that the client’s hash
    matches the hash computed from the current conversation.
    """
    now = time.time()
    if chat_id in sessions:
        session, last_used = sessions[chat_id]
        # Update the timestamp for session activity.
        sessions[chat_id] = (session, now)
        return session
    else:
        raise SyncRequired("Session not found, please sync full conversation.")

def create_session(chat_id: str, client_messages: list=[], api_key: str=None):
    logging.debug(f"Creating new session for chat_id: {chat_id}")
    session = OpenAIChatbot(api_key)
    session.conversation = client_messages
    sessions[chat_id] = (session, time.time())
    return session

# Optionally, start a background thread to clean expired sessions periodically.
def cleanup_sessions():
    while True:
        now = time.time()
        expired = [chat_id for chat_id, (_, last_used) in sessions.items() if now - last_used > SESSION_TTL]
        for chat_id in expired:
            logging.info(f"Cleaning up session {chat_id} (expired)")
            del sessions[chat_id]
        time.sleep(300)  # Check every 5 minutes

# Start cleanup thread (if running in a single-process deployment)
cleanup_thread = threading.Thread(target=cleanup_sessions, daemon=True)
cleanup_thread.start()
