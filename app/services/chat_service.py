# chatbot.py
import logging
from openai import OpenAI

class OpenAIChatbot:
    def __init__(self, api_key: str, model: str = "gpt-4o"):
        self.client = OpenAI(api_key=api_key)
        self.model = model
        # Initialize conversation with a system prompt.
        self.conversation = []
        logging.debug("Initialized OpenAIChatbot with default system prompt.")

    def add_message(self, role: str, content: str):
        self.conversation.append({"role": role, "content": content})
        logging.debug(f"Added message: role={role}, content={content}")

    def generate_text_response(self, prompt: str) -> str:
        self.add_message("user", prompt)
        try:
            logging.debug(f"Generating text response for prompt: {prompt}")
            response = self.client.chat.completions.create(
                model=self.model,
                messages=self.conversation,
                max_tokens=150,
            )
            assistant_response = response.choices[0].message.content
            self.add_message("assistant", assistant_response)
            logging.debug(f"Received text response: {assistant_response}")
            return assistant_response
        except Exception as e:
            logging.exception("Error generating text response")
            return f"Error generating response: {e}"

    def stream_response(self, prompt: str):
        self.add_message("user", prompt)
        try:
            logging.debug(f"Starting to stream response for prompt: {prompt}")
            completion = self.client.chat.completions.create(
                model=self.model,
                messages=self.conversation,
                stream=True
            )
            for chunk in completion:
                chunk_text = chunk.choices[0].delta.content
                logging.debug(f"Streaming chunk: {chunk_text}")
                yield chunk_text
        except Exception as e:
            logging.exception("Error streaming response")
            yield f"Error streaming response: {e}"