# chatbot.py
from typing import List, Union
import logging
from pydantic import BaseModel
from openai import OpenAI
import asyncio

class Decisions(BaseModel):
    search_online: bool
    generate_jee_list: bool
    write_notes: bool
    update_memory: bool

class SearchPrompts(BaseModel):
    prompts: List[str]

class GetCollegesList(BaseModel):
    jee_form_fields: List[str]

class OpenAIChatbot:
    def __init__(self, api_key: str, model: str = "gpt-4o"):
        self.client = OpenAI(api_key=api_key)
        self.model = model
        # Initialize conversation with a system prompt.
        self.conversation = []
        self.researches = []
        logging.debug("Initialized OpenAIChatbot with default system prompt.")
        self.memory = ""
        decision_instructions = [
            {
                "name": "search_online",
                "description": "Only search online if students wants latest information and explicitely asks for it then return tru else return false",
                "display_message": "Searching online for the answer..."
            },
            {
                "name": "generate_jee_list",
                "description": "To search colleges following fields are required: rank either jee mains or jee advanced or both of general category or reserved category rank with category(if applicable) or both. year of admission. set margin of opening closing rank and \
opening rank between 0 to 0.9 (0 to 90 percent) depending on the student query, default is 0.1 which is 10 percent but increase or decrease depending on student request",
            },
            {
                "name": "write_notes",
                "description": "Only write notes if student wants to detailed explanation for future reference such as: Detailed overview of the college, \
course offered, admission criteria, fee structure, facilities available, and any other relevant information.",
            },
            {
                "name": "update_memory",
                "description": "Only update memory if student provides new information or updates to existing information. You should consider to mention and update the following information: \
Name, Gender, Address, Phone number, Email, School, Class, Board, Subjects, Marks, competetive exams taken or appearing for this year and their ranks (in different categories if applicable for category wise), you should enter detail with precise understanding, do not mix ranks with different exams as all exams are different such as JEE main, JEE advanced, NEET, \
other competitive exams and their ranks.",
            }
        ]

    def add_message(self, role: str, content: str):
        self.conversation.append({"role": role, "content": content})
        logging.debug(f"Added message: role={role}, content={content}")

    def update_memory(self):
        system_prompt = """Analyze the conversation and identify if there is a change of interest, corrention,\
 or information of interest for counselling consideration of student missing in the profile.
If there is then update current profile with the new information.

Information to consider: Name, Gender, Address, Phone number, Email, School, Class, Board, \
Subjects, Marks, competetive exams taken or appearing for this year and their ranks (in different categories if applicable for category wise)

Current profile: ```{self.memory}```"""
        prompt = self.conversation
        response = self.generate_openai_response(prompt)
        self.memory = response
        return response

    def generate_openai_response(self, conversation: List[dict]) -> str:
        try:
            logging.debug(f"Generating text response")
            response = self.client.chat.completions.create(
                model=self.model,
                messages=conversation,
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
                        input= [{"role": "system", "content": "Keep all response less than 100 words"}]+ self.conversation,
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
