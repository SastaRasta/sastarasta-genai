from openai import OpenAI

client = OpenAI(api_key="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")

def get_chatbot_response(user_message):
    completion = client.chat.completions.create(
        model = "gpt-3.5-turbo",
        messages = [
            {"role": "system", "content": "You are an experienced travel agent"}, 
            {"role": "user", "content": user_message}
            ]
        )
    return {"response": completion.choices[0].message.content}