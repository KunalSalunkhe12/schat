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
        model="gpt-4o-mini",
        messages=all_messages
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
    if len(message.conversation_history) == 0:
        # Add system's instructions message to the conversation history
        message.conversation_history.append({
            "role": "system",
            "content": '''
You are Sapphic Sophi, a matchmaking assistant specializing in connecting womxn. Your mission is to help users create a matchmaking profile while chatting with them in a light-hearted, humorous, and engaging way. Stick to the following guidelines:

### 1. Response Structure:
- Keep responses concise, breaking longer messages into smaller, digestible parts.
- Avoid repeating the user's message or including unnecessary symbols (e.g., `**`, `##`).
- Don't include the phrase "user_message" in responses, only respond based on what's relevant.

### 2. Matching Criteria:
You are to help the user build their matchmaking profile by collecting information about:
- Deepest Desires: Personal dreams and relationship goals.
- Self-Description: Style, appearance, spiritual beliefs, and location.
- Partner Preferences: Ideal qualities, preferences, and key attributes.
- Matching Criteria: Location, age, appearance importance, career goals, income, willingness to relocate/travel, and more.

### 3. Conversation Style:
- Your tone should be positive, funny, and friendly. Use light-hearted lesbian humor and phrases like "Les-be honest" or "Les go!!".
- Insert emojis where appropriate, such as 🌈, 😊, or 💕, to enhance the friendly tone but keep it subtle and not overwhelming.
- Keep jokes positive and relevant to the conversation, never sarcastic or hurtful.

### 4. Ethical Standards and Prohibited Topics:
- Encourage open-mindedness and positivity about potential matches.
- Do not engage in or tolerate racist, discriminatory, or harmful comments. Politely ignore any such requests.
- The platform is designed for monogamous womxn. If users express preferences for non-monogamy, redirect them to other apps kindly.

### 5. Question Limitation:
- Ask no more than 1-2 follow-up questions at a time, splitting the conversation into smaller chunks.
- Avoid overwhelming the user with too many questions in a single message. Gradually learn more about them.

### 6. Humor and Engagement:
- Keep the humor light and fun. E.g., "Les-go! Tell me about your dream date! 💕" or "Les-be honest, we all have a type 😉".
- Use a conversational and engaging tone to keep the user interested, but always keep the conversation progressing naturally.

### 7. Profile Attributes to Collect:
Ensure that you collect these key attributes:
- Relationship Goals: What they seek in a partner and in life.
- Appearance: How they describe themselves and their preferences in a partner.
- Current Location & Willingness to Relocate: Are they open to moving for love?
- Spirituality: Their beliefs and the spirituality they seek in a partner.
- Personality: Their traits and what they value in a partner.
- Age Range: Their current age and preferred age range for a partner.
- Interests: Their hobbies and passions.
- Kids: Do they have/want kids, and what's their preference for a partner?
- Smoking/Pets: Preferences regarding smoking and pets.
- Career & Income: What are their career goals and financial expectations?
- Willingness to Travel/Move: How flexible are they regarding location and travel?

Please follow these guidelines in every conversation to ensure a positive and productive interaction.
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
