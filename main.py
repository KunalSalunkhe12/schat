from fastapi import FastAPI, Request
from pydantic import BaseModel
import openai
import os

# Load the OpenAI API key from environment variable
openai.api_key = os.getenv("OPENAI_API_KEY")

app = FastAPI()

class Message(BaseModel):
    user_message: str

# Store the assistant instructions and JSON schema
instructions = '''You’re an expert matchmaking assistant whose job is to chat with a user and create a matchmaking profile for them...'''
json_schema = {
    "name": "matchmaking_chatbot",
    "schema": {
        "type": "object",
        "properties": {
            "response_to_user": {"type": "string"},
            "user_profile": {
                "type": "object",
                "properties": {
                    "relationship_goals": {"type": "string"},
                    "appearance": {
                        "type": "object",
                        "properties": {
                            "personal_appearance": {"type": "string"},
                            "appearance_preferred_in_partner": {"type": "string"},
                            "importance_of_appearance_on_a_scale_of_1_to_10": {"type": "integer"}
                        },
                        "required": ["personal_appearance", "appearance_preferred_in_partner", "importance_of_appearance_on_a_scale_of_1_to_10"]
                    }
                }
            }
        },
        "required": ["response_to_user", "user_profile"]
    }
}

# Define the list to hold all messages in the conversation
all_messages = [
    {
        "role": "system",
        "content": instructions
    }
]

def call_openai_assistant(all_messages):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=all_messages
    )
    return response.choices[0].message['content']

@app.post("/chat/")
async def chat(message: Message):
    # Append user message
    all_messages.append({"role": "user", "content": message.user_message})

    # Call OpenAI API
    assistant_response = call_openai_assistant(all_messages)

    # Append assistant response
    all_messages.append({"role": "assistant", "content": assistant_response})

    return {"assistant_response": assistant_response, "conversation_history": all_messages}

