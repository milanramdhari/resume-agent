"""
Debug script to check environment variables and Gemini API connection.
"""

import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")
print(f"API Key found: {bool(api_key)}")

if api_key:
    try:
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-1.5-flash')
        response = model.generate_content("Hello, are you working?")
        print(f"Gemini Response: {response.text}")
    except Exception as e: # pylint: disable=broad-exception-caught
        print(f"Error connecting to Gemini: {e}")
