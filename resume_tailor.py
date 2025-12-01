"""
Module for tailoring resumes using Google's Gemini AI.
"""

import os
import google.generativeai as genai

class ResumeTailor:
    """
    A class to interact with Google Gemini API for tailoring resumes.
    """
    def __init__(self, api_key: str = None):
        self.api_key = api_key or os.getenv("GEMINI_API_KEY")
        if not self.api_key:
            raise ValueError(
                "API Key not found. Please set GEMINI_API_KEY environment variable "
                "or pass it to the constructor."
            )

        genai.configure(api_key=self.api_key)
        self.model = genai.GenerativeModel('gemini-2.0-flash')

    def tailor(self, resume_latex: str, job_description: str) -> str:
        """
        Tailors the given LaTeX resume to the job description using Gemini.

        Args:
            resume_latex (str): The content of the resume in LaTeX format.
            job_description (str): The job description text.

        Returns:
            str: The tailored resume in LaTeX format.
        """
        prompt = f"""
You are an expert resume consultant and LaTeX wizard.
I will provide you with a resume in LaTeX format and a job description.
Your task is to modify the resume to better match the job description.

Specific Instructions:
1. Analyze the job description for key skills and requirements.
2. Update the "Skills" section (or equivalent) to highlight relevant skills found in the job description.
3. Adjust the "Summary" or "Objective" to align with the role.
4. Rephrase bullet points in the "Experience" section to emphasize achievements relevant to the job.
5. maintain the exact same LaTeX structure and formatting. Do not remove any sections unless explicitly necessary.
6. Return ONLY the valid LaTeX code. Do not include markdown code blocks (like ```latex ... ```) or any other text.

Resume LaTeX:
{resume_latex}

Job Description:
{job_description}
"""
        response = self.model.generate_content(prompt)
        text = response.text

        # Clean up if the model returns markdown code blocks despite instructions
        if text.startswith("```latex"):
            text = text.replace("```latex", "", 1)
        if text.startswith("```"):
            text = text.replace("```", "", 1)
        if text.endswith("```"):
            text = text[:-3]

        return text.strip()
