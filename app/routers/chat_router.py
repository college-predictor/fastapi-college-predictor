from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from typing import List, Dict
from app.services.chat_service import OpenAIChatbot
import json
import logging
from fastapi import Depends

router = APIRouter()

class ConnectionManager:
    def __init__(self):
        self.active_connections: Dict[str, WebSocket] = {}
        self.chatbots: Dict[str, OpenAIChatbot] = {}

    async def connect(self, websocket: WebSocket, client_id: str):
        await websocket.accept()
        self.active_connections[client_id] = websocket
        self.chatbots[client_id] = OpenAIChatbot(api_key="None")

    def disconnect(self, client_id: str):
        if client_id in self.active_connections:
            del self.active_connections[client_id]
        if client_id in self.chatbots:
            del self.chatbots[client_id]

    async def send_message(self, message: str, client_id: str):
        if client_id in self.active_connections:
            await self.active_connections[client_id].send_text(message)

    def get_chatbot(self, client_id: str) -> OpenAIChatbot:
        return self.chatbots.get(client_id)

manager = ConnectionManager()

@router.websocket("/ws/{client_id}")
async def websocket_endpoint(websocket: WebSocket, client_id: str):
    try:
        await manager.connect(websocket, client_id)
        await manager.send_message(json.dumps({
            "type": "system",
            "message": "Connected to the chatbot server"
        }), client_id)

        while True:
            data = await websocket.receive_text()
            try:
                message_data = json.loads(data)
                user_message = message_data.get("message", "")
                
                chatbot = manager.get_chatbot(client_id)
                if not chatbot:
                    await manager.send_message(json.dumps({
                        "type": "error",
                        "message": "Chatbot not initialized"
                    }), client_id)
                    continue

                # Generate response using the chatbot
                response = chatbot.generate_text_response(user_message)
                
                await manager.send_message(json.dumps({
                    "type": "assistant",
                    "message": response
                }), client_id)

            except json.JSONDecodeError:
                await manager.send_message(json.dumps({
                    "type": "error",
                    "message": "Invalid message format"
                }), client_id)
            except Exception as e:
                logging.error(f"Error processing message: {str(e)}")
                await manager.send_message(json.dumps({
                    "type": "error",
                    "message": "Error processing your message"
                }), client_id)

    except WebSocketDisconnect:
        manager.disconnect(client_id)
    except Exception as e:
        logging.error(f"WebSocket error: {str(e)}")
        manager.disconnect(client_id)