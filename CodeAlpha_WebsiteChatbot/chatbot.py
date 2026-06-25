import json

with open("intents.json", "r") as file:
    data = json.load(file)

def get_response(user_input):

    user_input = user_input.lower()

    for intent in data["intents"]:

        for pattern in intent["patterns"]:

            if pattern.lower() in user_input:
                return intent["response"]

    return "Sorry, I don't understand that question."