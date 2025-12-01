"""
Script to list available Google Gemini models.
"""

import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    print("Error: GEMINI_API_KEY not found in environment variables.")
else:
    genai.configure(api_key=api_key)
    try:
        print("Listing available models that support generateContent:")
        models = []
        for m in genai.list_models():
            if 'generateContent' in m.supported_generation_methods:
                print(f"- {m.name}")
                models.append(m.name)

        with open("models.txt", "w", encoding="utf-8") as f:
            for model in models:
                f.write(f"{model}\n")
        print("Model list saved to models.txt")

    except Exception as e: # pylint: disable=broad-exception-caught
        print(f"An error occurred: {e}")
