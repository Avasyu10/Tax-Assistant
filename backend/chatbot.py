from huggingface_hub import InferenceClient

import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Get the token
HUGGING_FACE_API_KEY = os.getenv("HUGGING_FACE_TOKEN")

# Initialize the client
client = InferenceClient(
    provider="sambanova",
    api_key=HUGGING_FACE_API_KEY,
)

def get_tax_advice(question):
    """Fetch tax advice using Hugging Face's Qwen/QwQ-32B model."""
    try:
        completion = client.chat.completions.create(
            model="Qwen/QwQ-32B",  # Change the model if needed
            messages=[
                {"role": "system", "content": "You are a tax advisor."},
                {"role": "user", "content": question}
            ],
            max_tokens=500,
        )

        return completion.choices[0].message.content if completion.choices else "No response received."

    except Exception as e:
        return f"Error: {e}"

# Example usage:
# print(get_tax_advice("What tax deductions are available for salaried employees?"))
