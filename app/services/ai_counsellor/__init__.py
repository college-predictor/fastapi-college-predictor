import openai
import os

openai.api_key = os.getenv("OPENAI_API_KEY")  # Ensure this environment variable is set

def generate_response(message: str) -> str:
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are a helpful college counsellor."},
                {"role": "user", "content": message}
            ],
            max_tokens=150
        )
        return response.choices[0].message['content'].strip()
    except Exception as e:
        return "I'm sorry, but I couldn't process your request at the moment."

def generate_research(content: str) -> str:
    try:
        response = openai.Completion.create(
            model="text-davinci-003",
            prompt=f"Generate a detailed research document based on the following content:\n\n{content}",
            max_tokens=500
        )
        return response.choices[0].text.strip()
    except Exception as e:
        return "Research generation failed."