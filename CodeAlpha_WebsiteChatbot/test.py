from chatbot import get_response

while True:

    message = input("You: ")

    print("Bot:", get_response(message))