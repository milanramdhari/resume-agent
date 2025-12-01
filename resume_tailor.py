import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

class ResumeTailor:
    def __init__(self, api_key: str = None):
        self.api_key = api_key or os.getenv("GEMINI_API_KEY")
        if not self.api_key:
            raise ValueError("API Key not found. Please set GEMINI_API_KEY environment variable or pass it to the constructor.")
        
        genai.configure(api_key=self.api_key)
        # Using gemini-2.0-flash as it is available in the user's list.
        self.model = genai.GenerativeModel('gemini-2.0-flash')

    def tailor(self, resume_latex: str, job_description: str) -> str:
        """
        Tailors the resume latex code to the job description using the LLM.
        """
        prompt = f"""
You are an expert resume consultant and LaTeX wizard.
Your task is to tailor the following LaTeX resume to better match the provided job description.
You should:
1. Analyze the job description for key skills, qualifications, and keywords.
2. Modify the resume content to highlight these relevant areas.
3. Adjust the summary/objective (if present) to align with the job role.
4. Rephrase bullet points to emphasize impact and relevance to the job.
5. MAINTAIN the exact LaTeX structure and formatting. Do not break the code.
6. Return ONLY the valid LaTeX code for the tailored resume. Do not include markdown code blocks (like ```latex ... ```), just the raw code.

Job Description:
{job_description}

Resume LaTeX:
{resume_latex}
"""
        response = self.model.generate_content(prompt)
        
        # Clean up response if it contains markdown code blocks
        text = response.text
        if text.startswith("```latex"):
            text = text[8:]
        elif text.startswith("```"):
            text = text[3:]
        if text.endswith("```"):
            text = text[:-3]
            
        return text.strip()
