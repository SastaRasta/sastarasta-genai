import chatbot


print("Sherlock: Ask me anything!")
while True:
    user_input = input("You: ")

    response = chatbot.get_chatbot_response(user_input)
    print(f"Sherlock: {response['response']}")