import os

import openai
from dotenv import load_dotenv


class ChatGPT:
    
    def __init__(self, api_key):
        load_dotenv()
        # Fetch the API key from environment variables
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise ValueError("OPENAI_API_KEY not found in environment variables or .env file.")
        openai.api_key = api_key
        self.client = openai.OpenAI()

    def generate_help_text(self, task, task_description, model="gpt-3.5-turbo", temperature = 0):
        messages = [
            {"role": "system", "content": "You are an assistant that provides helpful advice on tasks."},
            {"role": "user", "content": f"Provide help for the following task:\n\nTitle: {task}\nDescription: {task_description}"},
        ]
        try:
            response = self.client.chat.completions.create(
                model = model,   # "gpt-3.5-turbo",  # Use "gpt-4" if available #
                messages= messages,
                temperature = temperature,
                max_tokens=150,
            )
            
            # response = openai.ChatCompletion.create(
            #     model="gpt-3.5-turbo",  # Use "gpt-4" if available
            #     messages=messages,
            #     temperature=0.7,
            #     max_tokens=150,
            # )
            return response.choices[0].message.content
        except Exception as e:
            return f"Error generating help text: {str(e)}"
