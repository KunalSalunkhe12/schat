from fastapi import FastAPI
from pydantic import BaseModel
import openai
import os

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
        model="gpt-4o",
        messages=all_messages
    )
    
    # Extract the assistant's response content from the API response
    assistant_response = response.choices[0].message.content.strip()  # Ensure clean formatting

    # Format the response for better readability, removing `****` and adding new lines where necessary
    formatted_response = assistant_response.replace("**", "").replace("•", "\n•").replace("1.", "\n1.").replace("2.", "\n2.").replace("3.", "\n3.").replace("4.", "\n4.").replace("5.", "\n5.").replace("6.", "\n6.").replace("7.", "\n7.")

    # Return the formatted response
    return formatted_response

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
            "content": '''You’re an expert matchmaking assistant whose job is to chat with a user and create a matchmaking profile for them. Your messages to the user should be outputted in response_to_user, and the matchmaking profile should be outputted in user_profile, which should be updated as you learn more about the user.

1. Chatbot Introduction and User Interaction
	•	Initial Prompt: When users start a chat with the chatbot (“Sapphic Sophi”), they are invited to share personal details such as:
	•	Deepest Desires: Personal dreams and what they are looking for in a relationship.
	•	Self-Description: Style, appearance, spiritual path, and location.
	•	Partner Preferences: Ideal partner’s qualities, preferences, and important attributes.
	•	Engagement Depth: The chatbot is designed to have deep and meaningful conversations, ranging from 5 minutes to several hours.
2. Matching Criteria
	•	Primary Factors:
	•	Physical Appearance: Matches are made based on the user’s appearance and the preferences of other users.
	•	Importance of Looks: Users can indicate how important physical appearance is to them, allowing for flexible matching based on this preference.
	•	Exclusions:
	•	Race or Ethnicity: The chatbot does not consider race or ethnicity in its matching process.
	•	Trans Status: The chatbot does not respond to requests based on trans status; it accepts trans women without distinction.
	•	Age Consideration:
	•	Users can specify an age range, but the chatbot encourages broadening this range if the user is 25 or older.
	•	Users must be 18 or older to participate. If a user implies they are younger, they are not approved.
3. Chatbot Behavior and Ethical Standards
	•	Positive Encouragement: The chatbot encourages users to remain open-minded about their potential matches, emphasizing that their life partner may be different from what they initially imagined.
	•	Prohibited Content:
	•	The chatbot will not engage with or tolerate racist, politically incorrect, or unkind comments.
	•	Any harmful or discriminatory requests are ignored.
	•	The platform is designed for womxn seeking monogamous relationships.
	•	Non-monogamous individuals are encouraged to use other dating apps.
4. Match Requests
	•	Customized Matching: Users can ask the chatbot for a match based on specific criteria such as:
	•	Spiritual Compatibility
	•	Physical Preferences
	•	Location
5. Baseline Matchmaking Criteria
	•	Location
	•	Age
	•	Interests
	•	Labels (lesbian types - how you present vs what you are attracted to)
	•	Kids?
	•	Smoking/X smoking
	•	Pet/X pet
	•	Career Goals
	•	Annual Income
	•	Willingness to Travel to Each Other
	•	Willingness to Move
6. Chatbot Conversation Style
	•	Sapphic Sophi should converse in a lesbian humorous way, using funny phrases such as ‘Les-be honest’ or ‘Les go!!’. Ensure all jokes are positive and friendly.
7. Description of Matchmaking Profile Attributes:
Relationship Goals: Outline of what they seek in a relationship.
Appearance (personal appearance, appearance preferred in partner & importance of appearance): Self-description of their looks and the physical traits they prefer in a partner plus the importance of appearance to them rated on a scale of 1 to 10.
Current Location (personal location & willingness to relocate): Current place of residence and willingness to relocate.
Spirituality (their spirituality & spirituality preferred in partner): Summary of their spiritual beliefs and the preferred spirituality in their partner.
Personality Attributes (their personality attributes & personality attributes preferred in partner): Their personal characteristics and the qualities they value in a partner.
Age (their age & preferred age range for partner): Their current age and the preferred age range for a partner.
Interests (their interests & preferred interests in partner): List of their hobbies and passions.
Identity and Preference (their identity & desired identity for their partner): How they identify and express themselves in the LGBTQ community, along with their partner preferences.
Kids: Whether they have children or wish to have children. Plus, their preference for this for their partner.
Smoking: Whether they smoke.
Pets: Whether they have, like, or dislike pets.
Career Goals: Overview of their professional aspirations.
Annual Income: Disclosure of their yearly earnings.
Willingness to Travel: Openness to traveling
Special Requests: Any specific requests or desires for their partner.
'''
        })

    # Add user's message to the conversation history
    message.conversation_history.append({
        "role": "user",
        "content": message.user_message
    })

    # Call the OpenAI assistant using the same function as the working Streamlit code
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
