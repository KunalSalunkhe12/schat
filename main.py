from fastapi import FastAPI, Request
from pydantic import BaseModel
import openai
import os

# Load the OpenAI API key from environment variable
openai.api_key = os.getenv("OPENAI_API_KEY")

app = FastAPI()

# Pydantic model for user input
class Message(BaseModel):
    user_message: str
    conversation_history: list  # List of previous messages (if any)

# Store the assistant instructions
instructions = '''You’re an expert matchmaking assistant whose job is to chat with a user and create a matchmaking profile for them...'''

def call_openai_assistant(messages):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages
    )
    return response.choices[0].message['content']

@app.get("/")
def read_root():
    return {"message": "Welcome to the matchmaking assistant API!"}

@app.post("/chat/")
async def chat(message: Message):
    # Initialize conversation if it's empty
    if len(message.conversation_history) == 0:
        # Add the system's instructions message to the conversation history
        message.conversation_history.append({
            "role": "system",
            "content": instructions
        })

    # Add the user's message to the conversation history
    message.conversation_history.append({
        "role": "user",
        "content": message.user_message
    })

    # Call the OpenAI API with the conversation history
    assistant_response = call_openai_assistant(message.conversation_history)

    # Append the assistant's response to the conversation history
    message.conversation_history.append({
        "role": "assistant",
        "content": assistant_response
    })

    # Return the assistant's response and the updated conversation history
    return {
        "assistant_response": assistant_response,
        "conversation_history": message.conversation_history
    }
