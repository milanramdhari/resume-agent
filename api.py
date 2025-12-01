"""
FastAPI server for the Resume Tailor Agent.
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from dotenv import load_dotenv
from resume_tailor import ResumeTailor

load_dotenv()

app = FastAPI()

# Allow CORS for local development
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class TailorRequest(BaseModel):
    """
    Request model for tailoring a resume.
    """
    resumeLatex: str
    jobDescription: str

@app.post("/tailor")
async def tailor_resume(request: TailorRequest):
    """
    Endpoint to tailor a resume.
    """
    try:
        # Initialize the agent (it will pick up the API key from env)
        agent = ResumeTailor()

        tailored_content = agent.tailor(request.resumeLatex, request.jobDescription)

        return {"tailoredLatex": tailored_content}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) from e

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
