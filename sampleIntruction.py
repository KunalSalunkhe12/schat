assistantInstructions = '''You’re an expert matchmaking assistant whose job is to chat with a user and create a matchmaking profile for them. Your messages to the user should be outputted in response_to_user, and the matchmaking profile should be outputted in user_profile, which should be updated as you learn more about the user.

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

assistantJSONSchema = {
  "name": "matchmaking_chatbot",
  "strict": True,
  "schema": {
    "type": "object",
    "properties": {
      "response_to_user": {
        "type": "string"
      },
      "user_profile": {
        "type": "object",
        "properties": {
          "relationship_goals": {
            "type": "string"
          },
          "appearance": {
            "type": "object",
            "properties": {
              "personal_appearance": {
                "type": "string"
              },
              "appearance_preferred_in_partner": {
                "type": "string"
              },
              "importance_of_appearance_on_a_scale_of_1_to_10": {
                "type": "integer"
              }
            },
            "required": [
              "personal_appearance",
              "appearance_preferred_in_partner",
              "importance_of_appearance_on_a_scale_of_1_to_10"
            ],
            "additionalProperties": False
          },
          "location": {
            "type": "object",
            "properties": {
              "their_location": {
                "type": "string"
              },
              "willingness_to_relocate": {
                "type": "string"
              }
            },
            "required": [
              "their_location",
              "willingness_to_relocate"
            ],
            "additionalProperties": False
          },
          "spirituality": {
            "type": "object",
            "properties": {
              "their_spirituality": {
                "type": "string"
              },
              "spirituality_preferred_in_partner": {
                "type": "string"
              }
            },
            "required": [
              "their_spirituality",
              "spirituality_preferred_in_partner"
            ],
            "additionalProperties": False
          },
          "personality_attributes": {
            "type": "object",
            "properties": {
              "their_personality_attributes": {
                "type": "string"
              },
              "personality_attributes_preferred_in_partner": {
                "type": "string"
              }
            },
            "required": [
              "their_personality_attributes",
              "personality_attributes_preferred_in_partner"
            ],
            "additionalProperties": False
          },
          "age": {
            "type": "object",
            "properties": {
              "their_age": {
                "type": "integer"
              },
              "preferred_age_range_for_partner": {
                "type": "string"
              }
            },
            "required": [
              "their_age",
              "preferred_age_range_for_partner"
            ],
            "additionalProperties": False
          },
          "interests": {
            "type": "object",
            "properties": {
              "their_interests": {
                "type": "string"
              },
              "preferred_interests_in_partner": {
                "type": "string"
              }
            },
            "required": [
              "their_interests",
              "preferred_interests_in_partner"
            ],
            "additionalProperties": False
          },
          "identity_and_preference": {
            "type": "object",
            "properties": {
              "their_identity": {
                "type": "string"
              },
              "desired_identity_for_partner": {
                "type": "string"
              }
            },
            "required": [
              "their_identity",
              "desired_identity_for_partner"
            ],
            "additionalProperties": False
          },
          "kids": {
            "type": "object",
            "properties": {
              "has_kids_or_wishes_to_have_kids": {
                "type": "string"
              },
              "preference_for_partner_having_kids": {
                "type": "string"
              }
            },
            "required": [
              "has_kids_or_wishes_to_have_kids",
              "preference_for_partner_having_kids"
            ],
            "additionalProperties": False
          },
          "smoking": {
            "type": "string"
          },
          "pets": {
            "type": "string"
          },
          "career_goals": {
            "type": "string"
          },
          "annual_income": {
            "type": "string"
          },
          "willingness_to_travel": {
            "type": "string"
          },
          "special_requests": {
            "type": "string"
          }
        },
        "required": [
          "relationship_goals",
          "appearance",
          "location",
          "spirituality",
          "personality_attributes",
          "age",
          "interests",
          "identity_and_preference",
          "kids",
          "smoking",
          "pets",
          "career_goals",
          "annual_income",
          "willingness_to_travel",
          "special_requests"
        ],
        "additionalProperties": False
      }
    },
    "required": [
      "response_to_user",
      "user_profile"
    ],
    "additionalProperties": False
  }
}