"""
FastAPI server for the Resume Tailor Agent.
"""

import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from dotenv import load_dotenv
from resume_tailor import ResumeTailor

load_dotenv()

app = FastAPI()

_raw_origins = os.getenv("ALLOWED_ORIGINS", "http://localhost:3000")
allowed_origins = [o.strip() for o in _raw_origins.split(",") if o.strip()]

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
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


@app.get("/health")
async def health():
    """
    Health check endpoint for Render.
    """
    return {"status": "ok"}


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
    port = int(os.getenv("PORT", "8000"))
    uvicorn.run(app, host="0.0.0.0", port=port)
