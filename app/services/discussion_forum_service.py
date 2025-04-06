from typing import Dict, List, Any, Tuple
from datetime import datetime
import uuid
import re
from better_profanity import profanity  # Import the profanity filter

class DiscussionForumService:
    """
    Service class for managing the JEE students discussion forum.
    Handles temporary message storage and active user tracking.
    """
    def __init__(self):
        # In-memory storage for active users and message history
        self.messages = []
        self.questions = {}
        self.rejected_messages = []  # Store rejected messages
        self.active_users = {}
        self.user_preferences = {}  # Store user preferences like username
        
        # Initialize profanity filter
        profanity.load_censor_words()  # Load the default word list
        
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
    
    async def validate_message(self, content: str) -> Tuple[bool, str]:
        """
        Validate a message before adding it to the chat history.
        
        Args:
            content: Message content to validate
            
        Returns:
            Tuple of (is_valid, reason)
        """
        if content=="":
            return True, ""
        
        if len(content) > 1000:
            return False, "Message is too long (max 1000 characters)"
            
        # Use better-profanity to check for inappropriate content
        if profanity.contains_profanity(content):
            return False, "Message contains inappropriate content"
        
        # Additional regex checks for other patterns if needed
        inappropriate_patterns = [
            r'\b(hate|violent|offensive)\b',  # Example of basic inappropriate terms
        ]
        
        for pattern in inappropriate_patterns:
            if re.search(pattern, content, re.IGNORECASE):
                return False, "Message contains inappropriate content"
        
        return True, ""
    
    async def add_message(self, user_id: str, content: str, message_type: str = "text", message_id: str = None, has_question: bool = False, question_id: str = None) -> Dict[str, Any]:
        """
        Add a new message to the chat history.
        
        Args:
            user_id: Unique identifier for the user
            content: Message content
            message_type: Type of the message (default: "text")
            message_id: Optional message ID from frontend (default: None)
            
        Returns:
            The created message object with validation status
        """
        user_info = self.active_users.get(user_id, {})
        username = user_info.get("username", f"User-{user_id[:8]}")
        color = user_info.get("color", "#000000")
        
        # Use provided message ID or generate a new one
        if message_id is None:
            message_id = str(uuid.uuid4())
        
        # Create message object
        message = {
            "id": message_id,
            "user_id": user_id,
            "username": username,
            "color": color,
            "type": message_type,
            "content": content,
            "timestamp": datetime.utcnow().isoformat(),
            "has_question": has_question,
            "question_id": question_id
        }
        
        # Validate message
        is_valid, reason = await self.validate_message(content)
        message["status"] = "validated" if is_valid else "error"
        
        if is_valid:
            # Add valid message to history
            self.messages.append(message)
        else:
            # Store rejected message with reason
            message["rejection_reason"] = reason
            self.rejected_messages.append(message)
        
        return message
    
    async def get_rejected_message_history(self, last_timestamp: str = None, limit: int = 100) -> List[Dict[str, Any]]:
        """
        Get rejected message history newer than specified timestamp.
        
        Args:
            last_timestamp: ISO format timestamp to fetch messages after
            limit: Maximum number of messages to return
            
        Returns:
            List of rejected message objects newer than the timestamp
        """
        if not last_timestamp:
            # Return most recent rejected messages if no timestamp provided
            return self.rejected_messages[-limit:]
            
        # Filter rejected messages newer than the given timestamp
        filtered = []
        for msg in reversed(self.rejected_messages):
            if msg["timestamp"] > last_timestamp:
                filtered.append(msg)
                if len(filtered) >= limit:
                    break
        
        return filtered
    
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
    
    async def add_question(self, question_id: str, question_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Add a new question to the questions list.
        
        Args:
            user_id: Unique identifier for the user who posted the question
            question_data: Dictionary containing question details
            
        Returns:
            The created question object with additional metadata
        """
        
        # Create question object with only the essential data
        question = {
            "id": question_id,
            "timestamp": datetime.utcnow().isoformat(),
            "data": question_data
        }
        
        # Add question to questions list
        self.questions[question_id] = question
        
        return question_id
    
    async def get_questions(self, last_timestamp: str = None, limit: int = 50) -> List[Dict[str, Any]]:
        """
        Get questions newer than specified timestamp.
        
        Args:
            last_timestamp: ISO format timestamp to fetch questions after
            limit: Maximum number of questions to return
            
        Returns:
            List of question objects newer than the timestamp
        """
        if not last_timestamp:
            # Return most recent questions if no timestamp provided
            return self.questions[-limit:]
            
        # Filter questions newer than the given timestamp
        filtered = []
        for q in reversed(self.questions):
            if q["timestamp"] > last_timestamp:
                filtered.append(q)
                if len(filtered) >= limit:
                    break
        
        return filtered