from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from typing import Dict
from app.services.chat_service import OpenAIChatbot
import json
import os

router = APIRouter()

# Store active connections
connected_clients: Dict[str, WebSocket] = {}

# Initialize chatbot with API key
chatbot = OpenAIChatbot(api_key=os.getenv("OPENAI_API_KEY", None))

@router.websocket("/ws/{client_id}")
async def websocket_endpoint(websocket: WebSocket, client_id: str):
    await websocket.accept()
    
    # Register new client
    connected_clients[client_id] = websocket
    
    try:
        while True:
            # Receive message from client
            data = await websocket.receive_json()
            # print(data)
            message_type = data.get("type", "text")
            content = data.get("content", "")
            
            # Process message based on type
            if message_type not in ["text", "research"]:
                await websocket.send_json({
                    "type": "error",
                    "message": "Invalid message type",
                    "sender": "bot"
                })
                continue
            
            async for text in chatbot.generate_streaming_response(content):
                # print(text)
                # Use streaming response for both text and research
                await websocket.send_json({
                    "type": message_type,
                    "message": text,
                    "is_chunk": True,
                    "sender": "bot"
                })
            
            # Send completion message
            await websocket.send_json({
                "type": message_type,
                "message": "DONE",
                "is_chunk": False,
                "sender": "bot"
            })
    
    except WebSocketDisconnect:
        # Remove client from active connections
        if client_id in connected_clients:
            del connected_clients[client_id]
            
        # Notify remaining clients about the disconnection
        for cid, conn in connected_clients.items():
            await conn.send_json({
                "type": "system",
                "message": f"Client {client_id} has left",
                "clients": list(connected_clients.keys())
            })
    except Exception as e:
        # Handle any other exceptions
        await websocket.send_json({
            "type": "error",
            "message": str(e)
        })
