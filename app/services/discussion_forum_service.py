from typing import Dict, List, Any
from datetime import datetime
import uuid

class DiscussionForumService:
    """
    Service class for managing the JEE students discussion forum.
    Handles temporary message storage and active user tracking.
    """
    def __init__(self):
        # In-memory storage for active users and message history
        self.messages = []
        self.active_users = {}
        self.user_preferences = {}  # Store user preferences like username
    
    async def register_active_user(self, user_id: str, username: str, color: str = None) -> None:
        """
        Register a user as active in the forum.
        
        Args:
            user_id: Unique identifier for the user
            username: Display name of the user
            color: User's preferred color for chat messages
        """
        # Store the username and color in preferences if it's not a default one
        if not username.startswith("User-"):
            self.user_preferences[user_id] = {
                "username": username,
                "color": color or "#000000"  # Default to black if no color is provided
            }
            
        self.active_users[user_id] = {
            "username": username,
            "color": color or self.user_preferences.get(user_id, {}).get("color", "#000000"),
            "last_active": datetime.utcnow()
        }
    
    async def get_user_preferences(self, user_id: str) -> dict:
        return self.user_preferences.get(user_id, {})
    
    async def remove_active_user(self, user_id: str) -> None:
        """
        Remove a user from the active users list.
        
        Args:
            user_id: Unique identifier for the user
        """
        if user_id in self.active_users:
            del self.active_users[user_id]
    
    async def get_active_users_count(self) -> int:
        """
        Get the count of currently active users.
        
        Returns:
            Number of active users
        """
        return len(self.active_users)
    
    async def add_message(self, user_id: str, content: str, message_type: str = "text") -> Dict[str, Any]:
        """
        Add a new message to the chat history.
        
        Args:
            user_id: Unique identifier for the user
            content: Message content
            message_type: Type of the message (default: "text")
            
        Returns:
            The created message object
        """
        user_info = self.active_users.get(user_id, {})
        username = user_info.get("username", f"User-{user_id[:8]}")
        color = user_info.get("color", "#000000")
        
        message = {
            "id": str(uuid.uuid4()),
            "user_id": user_id,
            "username": username,
            "color": color,
            "type": message_type,
            "content": content,
            "timestamp": datetime.utcnow().isoformat()
        }
        
        self.messages.append(message)
        return message
    
    async def get_message_history(self, last_timestamp: str = None, limit: int = 200) -> List[Dict[str, Any]]:
        """
        Get message history newer than specified timestamp.
        
        Args:
            last_timestamp: ISO format timestamp to fetch messages after
            limit: Maximum number of messages to return
            
        Returns:
            List of message objects newer than the timestamp
        """
        if not last_timestamp:
            # Return most recent messages if no timestamp provided
            return self.messages[-limit:]
            
        # Filter messages newer than the given timestamp
        filtered = []
        for msg in reversed(self.messages):
            if msg["timestamp"] > last_timestamp:
                filtered.append(msg)
                if len(filtered) >= limit:
                    break
        
        return filtered