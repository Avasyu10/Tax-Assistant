import os
from dotenv import load_dotenv
import google.generativeai as genai

# Load environment variables from .env file
load_dotenv()

# Get the Gemini API key
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# Configure the Gemini client
genai.configure(api_key=GEMINI_API_KEY)

# Initialize the Gemini model
model = genai.GenerativeModel(model_name="models/gemini-1.5-flash")

def get_tax_advice(question):
    """Fetch tax advice using Gemini's Gemini-Pro model."""
    try:
        response = model.generate_content(
            f"You are a tax advisor.\nUser: {question}"
        )

        return response.text.strip() if response.text else "No response received."

    except Exception as e:
        return f"Error: {e}"


