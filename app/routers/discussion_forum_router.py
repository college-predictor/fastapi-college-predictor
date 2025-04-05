from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from typing import Dict, List, Any
from app.services.discussion_forum_service import DiscussionForumService
from datetime import datetime

router = APIRouter()

# Store active connections
connected_clients: Dict[str, WebSocket] = {}

# Initialize the discussion forum service
discussion_service = DiscussionForumService()

@router.websocket("/ws-discussion-forum/{client_id}")
async def websocket_endpoint(websocket: WebSocket, client_id: str):
    await websocket.accept()
    
    # Register new client
    connected_clients[client_id] = websocket
    
    # Check for existing preferences
    user_prefs = await discussion_service.get_user_preferences(client_id)
    username = user_prefs.get("username", f"User-{client_id[:8]}")
    
    # Register user as active
    await discussion_service.register_active_user(client_id, username)
    
    # Get and broadcast active users count
    active_users_count = await discussion_service.get_active_users_count()
    
    # Notify all clients about the new connection
    for conn in list(connected_clients.values()):
        try:
            await conn.send_json({
                "type": "users_count",
                "count": active_users_count,
                "timestamp": datetime.utcnow().isoformat()
            })
        except Exception:
            pass
    
    try:
        while True:
            # Receive message from client
            data = await websocket.receive_json()
            # print(data)
            if data.get("type") == "get_users_count":
                # Send current users count
                await websocket.send_json({
                    "type": "users_count",
                    "count": await discussion_service.get_active_users_count(),
                    "timestamp": datetime.utcnow().isoformat()
                })
            
            elif data.get("type") == "username_update":
                # Update username
                new_username = data.get("user").strip()
                new_usern_color = data.get("userColor").strip()
                if new_username:
                    username = new_username
                    await discussion_service.register_active_user(client_id, username, new_usern_color)
            
            elif data.get("type") == "message":
                # Process and broadcast new message
                content = data.get("content", "").strip()
                message_type = data.get("type", "text")
                if content:
                    # Add message to history
                    message = await discussion_service.add_message(client_id, content, message_type)
                    
                    # Broadcast message to all connected clients except sender
                    for client_id, conn in list(connected_clients.items()):
                        if client_id != message["user_id"]:  # Skip sender
                            try:
                                await conn.send_json({
                                    "type": "message",
                                    "id": message["id"],
                                    "user_id": message["user_id"],
                                    "username": message["username"],
                                    "color": message["color"],
                                    "type": message["type"],
                                    "content": message["content"],
                                    "timestamp": message["timestamp"]
                                })
                            except Exception:
                                pass
            
            elif data.get("type") == "get_history":
                # Get message history newer than specified timestamp
                last_timestamp = data.get("last_timestamp")
                limit = data.get("limit", 20)
                
                # Retrieve messages newer than the timestamp
                messages = await discussion_service.get_message_history(last_timestamp, limit)
                
                # Send history to the requesting client
                await websocket.send_json({
                    "type": "history",
                    "messages": messages,
                    "has_more": len(messages) == limit
                })
    
    except WebSocketDisconnect:
        # Remove client from active connections
        if client_id in connected_clients:
            del connected_clients[client_id]
        
        # Remove user from active users
        await discussion_service.remove_active_user(client_id)
        
        # Notify remaining clients about updated user count
        remaining_count = await discussion_service.get_active_users_count()
        for conn in list(connected_clients.values()):
            try:
                await conn.send_json({
                    "type": "users_count",
                    "count": remaining_count,
                    "timestamp": datetime.utcnow().isoformat()
                })
            except Exception:
                pass
