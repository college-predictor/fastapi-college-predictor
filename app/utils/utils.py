from openai import OpenAI
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

def get_openai_response(api_key=None, model="gpt-4o-mini", messages=None):
    """
    This function sends a list of messages to OpenAI's GPT model and returns responses continuously.
    
    Parameters:
    - api_key (str): The OpenAI API key.
    - model (str): The GPT model to use (default is 'gpt-4o-mini').
    - messages (list): A list of messages where each message is a dictionary with 'role' and 'content'.
    
    Example of message structure:
    messages = [
        {"role": "system", "content": "Tell me about India"},
        {"role": "user", "content": "Tell me about India"}
    ]
    """
    
    # Use the provided API key or fall back to environment variable
    api_key = api_key or os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OpenAI API key not found in environment variables")
    
    # Initialize the OpenAI client with the API key
    client = OpenAI(api_key=api_key)
    
    # Make the API call to get the response stream
    stream = client.responses.create(
        model=model,
        input=messages,
        stream=True
    )
    
    # Iterate through the stream and yield the response continuously
    for event in stream:
        if hasattr(event, 'delta'):
            yield event.delta  # Yield the delta part of the response as it arrives