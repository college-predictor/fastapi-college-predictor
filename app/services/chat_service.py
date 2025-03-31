# chatbot.py
import logging
import os
from openai import OpenAI
import asyncio

class OpenAIChatbot:
    def __init__(self, api_key: str, model: str = "gpt-4o-mini"):
        self.client = OpenAI(api_key=api_key)
        self.model = model
        # Initialize conversation with a system prompt.
        self.conversation = []
        self.researches = []
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
                max_tokens=300,
            )
            assistant_response = response.choices[0].message.content
            self.add_message("assistant", assistant_response)
            logging.debug(f"Received text response: {assistant_response}")
            return assistant_response
        except Exception as e:
            logging.exception("Error generating text response")
            return f"Error generating response: {e}"
        
    def generate_research_response(self, prompt: str) -> str:
        self.add_message("user", prompt)
        try:
            logging.debug(f"Generating research response for prompt: {prompt}")
            response = self.client.chat.completions.create(
                model=self.model,
                messages=self.conversation,
                max_tokens=300,
            )
            assistant_response = response.choices[0].message.content
            self.add_message("assistant", assistant_response)
            logging.debug(f"Received research response: {assistant_response}")
            return assistant_response
        except Exception as e:
            logging.exception("Error generating research response")
            return f"Error generating response: {e}"

    async def generate_streaming_response(self, prompt: str):
        """
        Generates a streaming response for chat interactions.
        
        Parameters:
        - prompt (str): The user's input prompt
        
        Yields:
        - str: Chunks of the response as they arrive
        """
        self.add_message("user", prompt)
        try:
            logging.debug(f"Generating streaming response for prompt: {prompt}")
            stream = self.client.responses.create(
                        model=self.model,
                        input=self.conversation,
                        stream=True,
                    )
            
            collected_response = []
            for event in stream:
                if event.type =='response.created':
                    logging.debug(f"Received streaming response event: {event}")
                elif event.type == 'response.output_text.delta':
                    text_content = event.delta
                    yield event.delta  # Yield the delta part of the response as it arrives
                elif event.type == 'response.output_text.done':
                    logging.debug("Streaming response complete")
                    complete_response = event.text
                    self.add_message("assistant", complete_response)
                    logging.debug(f"Completed streaming response: {complete_response}")
                await asyncio.sleep(0.01)  # 10ms delay between chunks
            
            # Add the complete response to conversation history
            complete_response = "".join(collected_response)
            self.add_message("assistant", complete_response)
            logging.debug(f"Completed streaming response: {complete_response}")
            
        except Exception as e:
            logging.exception("Error generating streaming response")
            yield f"Error generating response: {e}"

    async def generate_streaming_response2(self, prompt: str):
        """
        A mock streaming response function that simulates streaming by yielding words with delays
        
        Parameters:
        - prompt (str): The user's input prompt (not used in this mock version)
        
        Yields:
        - str: Words of the hardcoded response with delays
        """
        
        # Hardcoded response of approximately 100 words
        response = """Artificial Intelligence has transformed the technology landscape significantly. 
        Machine learning algorithms now power numerous applications in our daily lives. 
        From recommendation systems to autonomous vehicles, AI continues to evolve rapidly. 
        Deep learning models have achieved remarkable success in image recognition and natural language processing. 
        The future holds exciting possibilities as researchers develop more sophisticated neural networks. 
        Ethical considerations and responsible AI development remain crucial topics of discussion.
        Artificial Intelligence has transformed the technology landscape significantly. 
        Machine learning algorithms now power numerous applications in our daily lives. 
        From recommendation systems to autonomous vehicles, AI continues to evolve rapidly. 
        Deep learning models have achieved remarkable success in image recognition and natural language processing. 
        The future holds exciting possibilities as researchers develop more sophisticated neural networks. 
        Ethical considerations and responsible AI development remain crucial topics of discussion."""
        
        # Split response into words and stream them with delays
        words = response.split()
        for word in words:
            yield word + " "
            await asyncio.sleep(0.01)  # 200ms delay between words
