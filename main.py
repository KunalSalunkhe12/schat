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

# Initial empty user profile structure
user_profile_template = {
    "relationship_goals": "",
    "appearance": {
        "personal_appearance": "",
        "appearance_preferred_in_partner": "",
        "importance_of_appearance_on_a_scale_of_1_to_10": None
    },
    "location": {
        "their_location": "",
        "willingness_to_relocate": ""
    },
    "spirituality": {
        "their_spirituality": "",
        "spirituality_preferred_in_partner": ""
    },
    "personality_attributes": {
        "their_personality_attributes": "",
        "personality_attributes_preferred_in_partner": ""
    },
    "age": {
        "their_age": None,
        "preferred_age_range_for_partner": ""
    },
    "interests": {
        "their_interests": "",
        "preferred_interests_in_partner": ""
    },
    "identity_and_preference": {
        "their_identity": "",
        "desired_identity_for_partner": ""
    },
    "kids": {
        "has_kids_or_wishes_to_have_kids": "",
        "preference_for_partner_having_kids": ""
    },
    "smoking": "",
    "pets": "",
    "career_goals": "",
    "annual_income": "",
    "willingness_to_travel": "",
    "special_requests": ""
}

# Function to call the OpenAI Chat API
def call_openai_assistant(all_messages):
    # Make the API call to OpenAI Chat Completions
    response = openai.chat.completions.create(
        model="gpt-4o-mini",
        messages=all_messages,
        response_format={
            "type": "json_schema",
            "json_schema": userInteractionResources.assistantJSONSchema
        }
    )
    
    # Extract the assistant's response content from the API response
    # assistant_response = response.choices[0].message.content.strip()  # Ensure clean formatting

    # Format the response for better readability
    # formatted_response = assistant_response.replace("**", "").replace("##", "").replace("•", "\n•").replace("1.", "\n1.").replace("2.", "\n2.")

    # Return the formatted response
    return response.choices[0].message.content  

# Function to update the user profile based on new data
def update_user_profile(existing_profile, new_data):
    for key, value in new_data.items():
        if isinstance(value, dict):
            existing_profile[key] = update_user_profile(existing_profile.get(key, {}), value)
        elif value:
            existing_profile[key] = value
    return existing_profile

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

    # Load the previous user profile (or start with an empty one)
    user_profile = message.conversation_history[-1].get('user_profile', user_profile_template.copy())

    # Update the profile with the new assistant response data
    updated_user_profile = update_user_profile(user_profile, assistant_response['user_profile'])

    # Append the assistant's response to the conversation history
    message.conversation_history.append({
        "role": "assistant",
        "content": assistant_response
    })

    # Return the assistant's response and the updated conversation history
    return {
        "assistant_response": assistant_response['response_to_user'],
        "user_profile": updated_user_profile
    }
