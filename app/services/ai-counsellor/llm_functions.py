# import google.generativeai as genai
# from dotenv import load_dotenv
# import os
#
# load_dotenv()
# api_key = os.getenv('GEMINI_API_KEY')
# print("API KEY: ", api_key)
# genai.configure(api_key=api_key)
# model = genai.GenerativeModel("gemini-1.5-flash")
# response = model.generate_content("Explain how AI works")
# print(response.text)


from openai import OpenAI
from typing import List, Dict, Union

class OpenAIChatbot:
    """
    OpenAI Chatbot with functionalities for:
    - Text-based responses
    - JSON-based outputs
    - Image analysis
    - Tool-based reasoning
    """

    def __init__(self, api_key: str, model: str = "gpt-4o"):
        """
        Initialize the chatbot with an API key and model.
        """
        self.client = OpenAI(api_key=api_key)
        self.model = model
        self.conversation = [{"role": "system", "content": "You are a helpful assistant."}]

    def add_message(self, role: str, content: Union[str, Dict]):
        """
        Adds a message to the conversation history.
        """
        if isinstance(content, dict):
            self.conversation.append({"role": role, "content": content})
        else:
            self.conversation.append({"role": role, "content": content})

    def generate_text_response(self, prompt: str) -> str:
        """
        Generate a text-based response from the model.
        """
        self.add_message("user", prompt)
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=self.conversation
            )
            # print("Assistant response: ", response)
            assistant_response = response.choices[0].message.content
            self.add_message("assistant", assistant_response)
            return assistant_response
        except Exception as e:
            return f"Error generating response: {e}"

    def generate_json_response(self, prompt: str) -> Dict:
        """
        Generate a structured JSON response.
        """
        self.add_message("user", prompt)
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=self.conversation,
                response_format={"type": "json_object"}
            )
            # print("Assistant response json: ", response)
            assistant_response = response.choices[0].message.content
            self.add_message("assistant", assistant_response)
            return assistant_response
        except Exception as e:
            return {"error": f"Error generating JSON response: {e}"}

    def analyze_image(self, image_url: str, prompt: str = "What's in this image?") -> Dict:
        """
        Analyze an image and return the response.
        """
        # Add user message with both text and image content
        self.add_message("user", f"{prompt} Here's the image: {image_url}")

        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=self.conversation,
                max_completion_tokens=300
            )
            # print("Assistant response image: ", response)
            # Extract the response content
            assistant_response = response.choices[0].message.content
            self.add_message("assistant", assistant_response)
            return {"response": assistant_response}
        except Exception as e:
            return {"error": f"Error analyzing image: {e}"}

    def stream_response(self, prompt: str):
        """
        Stream a response from the model.
        """
        self.add_message("user", prompt)
        try:
            completion = self.client.chat.completions.create(
                model=self.model,
                messages=self.conversation,
                stream=True
            )
            for chunk in completion:
                yield chunk.choices[0].delta.content
        except Exception as e:
            yield f"Error streaming response: {e}"


# Example usage
if __name__ == "__main__":
    import os
    from dotenv import load_dotenv

    load_dotenv()
    api_key = os.getenv('OPENAI_API_KEY')
    bot = OpenAIChatbot(api_key=api_key, model="gpt-4o")

    # Example: Text-based response
    # text_response = bot.generate_text_response("Tell me a joke.")
    # print("Text Response:", text_response)
    #
    # # Example: JSON-based response
    # json_response = bot.generate_json_response("Summarize the latest news in JSON format.")
    # print("JSON Response:", json_response)

    # # Example: Image analysis
    # image_url = "https://upload.wikimedia.org/wikipedia/commons/thumb/d/dd/Gfp-wisconsin-madison-the-nature-boardwalk.jpg/2560px-Gfp-wisconsin-madison-the-nature-boardwalk.jpg"
    # image_response = bot.analyze_image(image_url)
    # print("Image Analysis Response:", image_response)

    # Example: Stream response
    for chunk in bot.stream_response("Explain quantum mechanics briefly."):
        print(chunk, end="")
