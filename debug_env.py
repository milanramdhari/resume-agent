import os
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()

key = os.getenv("GEMINI_API_KEY")
print(f"Key loaded: {bool(key)}")
if key:
    print(f"Key starts with: {key[:4]}...")

try:
    genai.configure(api_key=key)
    model = genai.GenerativeModel('gemini-1.5-flash')
    print("Model initialized successfully.")
except Exception as e:
    print(f"Error initializing model: {e}")
