from pydantic import BaseModel
from openai import OpenAI
import logging

class MessageValidation(BaseModel):
    validated: bool
    reason: str

class OpenAIDecisions:
    def __init__(self, api_key: str):
        self.client = OpenAI(api_key=api_key)

    async def message_validator(self, message: str):
        """
        Validates a message content using OpenAI's moderation API.
        
        Args:
            message: The message text to validate
            
        Returns:
            bool: True if message is valid, False otherwise
            
        Raises:
            Exception: Logs any API errors but returns False to maintain flow
        """
        try:
            logging.debug(f"Validating message content")
            completion = self.client.beta.chat.completions.parse(
                model="gpt-4o",
                messages=[
                    {"role": "system", "content": "Analyze the given message ensure given message does not contain adultry, offensive, abusing, threating kind of message and do not share or request mobile number, etc in the message also return the reason validation failure in less than 6 words."},
                    {"role": "user", "content": f"validate the message: {message}"},
                ],
                max_tokens=50,
                response_format=MessageValidation,
            )
            validation: MessageValidation = completion.choices[0].message.parsed
            if not validation.validated:
                logging.warning(f"Message validation failed for content: {message}")
            return validation.validated, validation.reason 
        except Exception as e:
            logging.exception(f"Error during message validation: {str(e)}")
            return False, "Connection failed with OpenAI"