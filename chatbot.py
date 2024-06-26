from openai import OpenAI
import os

API_KEY = os.getenv("OPENAI_KEY")

client = OpenAI(api_key=API_KEY)

def get_chatbot_response(user_message):
    completion = client.chat.completions.create(
        model = "gpt-3.5-turbo",
        messages = [
            {"role": "system", "content": "You are an experienced travel agent. You goal is to comprehensively answer queries from the perspective of a travel guru. Provide detailed inisghts and crisp answers"}, 
            {"role": "user", "content": user_message}
            ]
        )
    return {"response": completion.choices[0].message.content}