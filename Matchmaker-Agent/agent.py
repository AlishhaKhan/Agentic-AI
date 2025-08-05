from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def get_match_recommendation(user_input: str) -> str:
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {
                "role": "system",
                "content": (
                    "You are a thoughtful and respectful AI matchmaker. "
                    "Your job is to find a compatible partner based on the user's personality, interests, and preferences. "
                    "Make it warm, empathetic, and romantic."
                ),
            },
            {"role": "user", "content": user_input},
        ],
        temperature=0.8,
    )
    return response.choices[0].message.content
