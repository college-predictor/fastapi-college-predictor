from fastapi import APIRouter, WebSocket, WebSocketDisconnect, HTTPException
from typing import Dict, List, Any
from app.services.discussion_forum_service import DiscussionForumService
from datetime import datetime, timezone

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
                try:
                    # Send current users count
                    await websocket.send_json({
                        "type": "users_count",
                        "count": await discussion_service.get_active_users_count(),
                        "timestamp": datetime.now(timezone.utc).isoformat()
                    })
                except Exception as e:
                    print(f"Error sending users count: {str(e)}")
                    # Send error response to client
                    await websocket.send_json({
                        "type": "error",
                        "message": "Failed to get users count",
                        "timestamp": datetime.timezome.isoformat()
                    })
            
            elif data.get("type") == "username_update":
                try:
                    # Update username
                    new_username = data.get("user").strip()
                    new_usern_color = data.get("userColor").strip()
                    if new_username:
                        username = new_username
                        await discussion_service.register_active_user(client_id, username, new_usern_color)
                except Exception as e:
                    print(f"Error updating username: {str(e)}")
                    # Send error response to client
                    await websocket.send_json({
                        "type": "error",
                        "message": "Failed to update username",
                        "timestamp": datetime.now(timezone.utc).isoformat()
                    })
            
            elif data.get("type") == "message":
                try:
                    # Process and broadcast new message
                    content = data.get("content", "").strip()
                    message_type = data.get("type", "text")
                    message_id = data.get("messageId")
                    question_id = data.get("questionId")
                    has_question = data.get("hasQuestion")
                    if content != None:
                        try:
                            # Add message to history with validation
                            message = await discussion_service.add_message(client_id, content, message_type, message_id, has_question, question_id)
                            
                            # Send validation status to the sender
                            await websocket.send_json({
                                "type": "validation",
                                "messageId": message["id"],
                                "status": message["status"],
                                "reason": message["reason"]
                            })
                            
                            # Only broadcast validated messages
                            if message["status"] == "validated":
                                try:
                                    # Broadcast message to all connected clients except sender
                                    print(f"Broadcasting message to {len(connected_clients)} clients")  # Debug log
                                    for broadcasting_client_id, conn in list(connected_clients.items()):
                                        if broadcasting_client_id != message["user_id"]:  # Skip sender
                                            try:
                                                # print(f"Sending to client {client_id}")  # Debug log
                                                await conn.send_json({
                                                    "type": "message",
                                                    "id": message["id"],
                                                    "user_id": message["user_id"],
                                                    "username": message["username"],
                                                    "color": message["color"],
                                                    "type": message["type"],
                                                    "content": message["content"],
                                                    "timestamp": message["timestamp"],
                                                    "has_question": message["has_question"],
                                                    "question_id": message["question_id"]
                                                })
                                                # print(f"Successfully sent to {client_id}")  # Debug log
                                            except Exception as e:
                                                # print(f"Error sending to client {client_id}: {str(e)}")  # Debug log
                                                # Remove disconnected client
                                                if broadcasting_client_id in connected_clients:
                                                    del connected_clients[broadcasting_client_id]
                                except Exception as e:
                                    print(f"Error broadcasting message: {str(e)}")
                        except Exception as e:
                            print(f"Error adding message to history: {str(e)}")
                            await websocket.send_json({
                                "type": "error",
                                "message": "Failed to process message",
                                "timestamp": datetime.now(timezone.utc).isoformat()
                            })
                except Exception as e:
                    print(f"Error processing message: {str(e)}")
                    await websocket.send_json({
                        "type": "error",
                        "message": "Failed to process message",
                        "timestamp": datetime.utcnow().isoformat()
                    })
            
            elif data.get("type") == "get_history":
                try:
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
                except Exception as e:
                    print(f"Error getting message history: {str(e)}")
                    await websocket.send_json({
                        "type": "error",
                        "message": "Failed to retrieve message history",
                        "timestamp": datetime.utcnow().isoformat()
                    })

            elif data.get("type") == "question":
                try:
                    # Process and broadcast new question
                    question_id = data.get("questionId", {})
                    question_data = data.get("data", {})
                    
                    if question_data:
                        try:
                            # Add question to history
                            question = await discussion_service.add_question(question_id, question_data)
                        except Exception as e:
                            print(f"Error adding question to history: {str(e)}")
                            await websocket.send_json({
                                "type": "error",
                                "message": "Failed to add question",
                                "timestamp": datetime.utcnow().isoformat()
                            })
                except Exception as e:
                    print(f"Error processing question: {str(e)}")
                    await websocket.send_json({
                        "type": "error",
                        "message": "Failed to process question",
                        "timestamp": datetime.utcnow().isoformat()
                    })
            
    except WebSocketDisconnect:
        try:
            # Remove client from active connections
            if client_id in connected_clients:
                del connected_clients[client_id]
            
            # Remove user from active users
            await discussion_service.remove_active_user(client_id)
            
            # Notify remaining clients about updated user count
            try:
                remaining_count = await discussion_service.get_active_users_count()
                for conn in list(connected_clients.values()):
                    try:
                        await conn.send_json({
                            "type": "users_count",
                            "count": remaining_count,
                            "timestamp": datetime.utcnow().isoformat()
                        })
                    except Exception as e:
                        print(f"Error notifying client about disconnection: {str(e)}")
            except Exception as e:
                print(f"Error getting active users count after disconnection: {str(e)}")
        except Exception as e:
            print(f"Error handling WebSocket disconnection: {str(e)}")

@router.get("/question/{question_id}")
async def get_question(question_id: str):
    """
    Get a question by its ID.
    
    Args:
        question_id: The ID of the question to retrieve
        
    Returns:
        The question object if found
    """
    try:
        question = await discussion_service.get_question(question_id)
        if not question:
            raise HTTPException(status_code=404, detail="Question not found")
        return question.get("data")
    except HTTPException:
        # Re-raise HTTP exceptions for proper error handling
        raise
    except Exception as e:
        print(f"Error retrieving question {question_id}: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to retrieve question")


