from fastapi import FastAPI
from pydantic import BaseModel
import openai
import os
import userInteractionResources
import json

# Initialize OpenAI API with your API key
openai.api_key = os.getenv("OPENAI_API_KEY")  # You can also load this from environment or set it directly.

app = FastAPI()

# Pydantic model for the message request
class Message(BaseModel):
    user_message: str
    conversation_history: list  # List of previous messages (if any)

# Function to call the OpenAI Chat API
def call_openai_assistant(all_messages):
    # Make the API call to OpenAI Chat Completions
    response = openai.chat.completions.create(
        model="gpt-4o-mini",
        messages=all_messages,
          response_format = {
            "type": "json_schema",
            "json_schema": userInteractionResources.assistantJSONSchema
        }
    )
    
    # Extract the assistant's response content from the API response
    assistant_response = response.choices[0].message.content.strip()  # Ensure clean formatting

    # Format the response for better readability, removing `****` and adding new lines where necessary
    formatted_response = assistant_response.replace("**", "").replace("##", "").replace("•", "\n•").replace("1.", "\n1.").replace("2.", "\n2.")

    # Return the formatted response
    return formatted_response

@app.get("/")
def read_root():
    return {"message": "Welcome to the matchmaking assistant API!"}

@app.post("/chat/")
async def chat(message: Message):
    # Initialize the conversation if it is the first message
    print("Received MESSAGE START-----", message)
    print("MESSAGE END ------")

    if len(message.conversation_history) == 0:
        # Add system's instructions message to the conversation history
        message.conversation_history.append({
            "role": "system",
            "content": userInteractionResources.assistantInstructions
        })

    # Add user's message to the conversation history
    message.conversation_history.append({
        "role": "user",
        "content": message.user_message
    })

    # Call the OpenAI assistant using the same function as the working Streamlit code
    assistant_response = call_openai_assistant(message.conversation_history)
    print("assistant_response: ", assistant_response)
    assistant_response = json.loads(assistant_response)

    # Append the assistant's response to the conversation history
    message.conversation_history.append({
        "role": "assistant",
        "content": assistant_response
    })

    # Return the assistant's response and the updated conversation history
    return {
        "assistant_response": assistant_response['response_to_user'],
        "user_profile": assistant_response['user_profile'],
    }