from fastapi import FastAPI
from pydantic import BaseModel
import openai
import os

# Load the OpenAI API key from the environment variable
openai.api_key = os.getenv("OPENAI_API_KEY")

app = FastAPI()

# Pydantic model for the message request
class Message(BaseModel):
    user_message: str
    conversation_history: list  # List of previous messages (if any)

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

def call_openai_assistant(json_schema, all_messages):
    # Make the API call using the correct method and model
    response = openai.ChatCompletion.create(
        model="gpt-4o-2024-08-06",
        messages=all_messages,
        functions=[
            {
                "name": "matchmaking_chatbot",
                "parameters": {
                    "type": "json_schema",
                    "json_schema": json_schema
                }
            }
        ]
    )
    
    # Extract assistant's response
    assistant_response = response.choices[0].message['content']

    # Return the assistant's response
    return assistant_response

@app.get("/")
def read_root():
    return {"message": "Welcome to the matchmaking assistant API!"}

@app.post("/chat/")
async def chat(message: Message):
    # Initialize the conversation if it is the first message
    if len(message.conversation_history) == 0:
        # Add system's instructions message to the conversation history
        message.conversation_history.append({
            "role": "system",
            "content": instructions
        })

    # Add user's message to the conversation history
    message.conversation_history.append({
        "role": "user",
        "content": message.user_message
    })

    # Call the OpenAI assistant
    assistant_response = call_openai_assistant(json_schema, message.conversation_history)

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
