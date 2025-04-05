# Discussion Forum WebSocket API Documentation

This document describes how to interact with the discussion forum WebSocket API. The API enables real-time chat functionality with features like user management, message broadcasting, and chat history.

## WebSocket Connection

### Connection URL
```
ws://your-domain/ws-discussion-forum/{client_id}
```
where `client_id` is a unique identifier for the client.

## Message Types

The API uses JSON messages with a `type` field to determine the message purpose. All timestamps are in ISO format.

### 1. Users Count Updates

Automatically sent when users connect/disconnect.

```json
{
    "type": "users_count",
    "count": 5,
    "timestamp": "2023-12-25T10:30:00.000Z"
}
```

### 2. Username Update

**Request:**
```json
{
    "type": "username_update",
    "content": "John Doe"
}
```

### 3. Chat Message

**Send Message:**
```json
{
    "type": "message",
    "content": "Hello everyone!"
}
```

**Receive Message:**
```json
{
    "type": "message",
    "message": {
        "id": "550e8400-e29b-41d4-a716-446655440000",
        "user_id": "client123",
        "username": "John Doe",
        "content": "Hello everyone!",
        "timestamp": "2023-12-25T10:30:00.000Z"
    }
}
```

### 4. Message History

**Request:**
```json
{
    "type": "get_history",
    "page": 0,
    "page_size": 20
}
```

**Response:**
```json
{
    "type": "history",
    "messages": [
        {
            "id": "550e8400-e29b-41d4-a716-446655440000",
            "user_id": "client123",
            "username": "John Doe",
            "content": "Hello everyone!",
            "timestamp": "2023-12-25T10:30:00.000Z"
        }
    ],
    "page": 0,
    "has_more": true
}
```

## Frontend Implementation Example

```javascript
// Connect to WebSocket
const clientId = 'unique-client-id'; // Generate or get from your auth system
const ws = new WebSocket(`ws://your-domain/ws-discussion-forum/${clientId}`);

// Handle connection open
ws.onopen = () => {
    console.log('Connected to discussion forum');
};

// Handle incoming messages
ws.onmessage = (event) => {
    const data = JSON.parse(event.data);
    
    switch(data.type) {
        case 'users_count':
            updateUserCount(data.count);
            break;
        case 'message':
            displayMessage(data.message);
            break;
        case 'history':
            displayMessageHistory(data.messages);
            break;
    }
};

// Send a chat message
function sendMessage(content) {
    ws.send(JSON.stringify({
        type: 'message',
        content: content
    }));
}

// Update username
function updateUsername(newUsername) {
    ws.send(JSON.stringify({
        type: 'username_update',
        content: newUsername
    }));
}

// Request message history
function loadHistory(page = 0) {
    ws.send(JSON.stringify({
        type: 'get_history',
        page: page,
        page_size: 20
    }));
}

// Handle disconnection
ws.onclose = () => {
    console.log('Disconnected from discussion forum');
    // Implement reconnection logic here
};
```

## Error Handling

1. The WebSocket connection automatically handles disconnections by removing the client from active users.
2. Messages that fail to send to specific clients are silently ignored to maintain service stability.
3. Invalid message formats or types will be ignored by the server.

## Best Practices

1. Implement reconnection logic on the frontend to handle temporary disconnections.
2. Validate message content before sending.
3. Handle all incoming message types, even if not all are used.
4. Store the client ID securely if it's tied to user authentication.
5. Implement proper error handling for WebSocket events.