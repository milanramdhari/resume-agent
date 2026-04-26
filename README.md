# Resume Tailor Agent

An AI-powered tool that tailors LaTeX resumes to a given job description using Google Gemini. Paste in your resume and a job posting — the agent rewrites bullet points, the summary, and skills section to better match the role while preserving your LaTeX formatting exactly.

## Architecture

```
resume-agent/
├── resume_tailor.py   # Core: ResumeTailor class, Gemini API calls
├── api.py             # FastAPI server (POST /tailor)
├── main.py            # Typer CLI
├── requirements.txt   # Python dependencies
└── web-app/           # Next.js frontend
    └── app/
        └── page.tsx   # Single-page UI with diff viewer
```

**Data flow:**
1. User inputs LaTeX resume + job description (via web UI or CLI)
2. `ResumeTailor.tailor()` sends both to Gemini with a structured prompt
3. Gemini returns modified LaTeX (raw, no markdown fences)
4. Result is displayed / written to file; web UI shows a side-by-side diff

## Stack

| Layer | Tech |
|---|---|
| AI | Google Gemini (`gemini-2.5-flash` by default) |
| Backend API | FastAPI + Uvicorn |
| CLI | Typer + Rich |
| Frontend | Next.js (TypeScript, Tailwind CSS) |
| Diff viewer | `react-diff-viewer-continued` |

## Setup

### Prerequisites
- Python 3.9+
- Node.js 18+
- A [Google Gemini API key](https://aistudio.google.com/app/apikey)

### Backend

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

# Set your API key
echo "GEMINI_API_KEY=your_key_here" > .env

# Start the API server
uvicorn api:app --reload
# Runs on http://localhost:8000
```

### Frontend

```bash
cd web-app
npm install
npm run dev
# Runs on http://localhost:3000
```

## Usage

### Web UI

1. Start both backend and frontend (see above)
2. Open `http://localhost:3000`
3. Paste your LaTeX resume and a job description
4. Click **Tailor My Resume**
5. Use **Preview Changes** to see a word-level diff, or **Copy Code** to grab the output

### CLI

```bash
python main.py --resume my_resume.tex --job-desc job.txt --output tailored.tex
```

| Flag | Description |
|---|---|
| `--resume` | Path to your input `.tex` resume |
| `--job-desc` | Path to the job description text file |
| `--output` | Output path (default: `tailored_resume.tex`) |
| `--api-key` | Gemini API key (falls back to `GEMINI_API_KEY` env var) |

## Environment Variables

| Variable | Required | Default | Description |
|---|---|---|---|
| `GEMINI_API_KEY` | Yes | — | Google Gemini API key |
| `GEMINI_MODEL` | No | `gemini-2.5-flash` | Gemini model to use |

## Development

```bash
# Lint
pylint resume_tailor.py api.py main.py

# Tests
pytest
```

The CORS policy in `api.py` allows `localhost:3000` only. Update `allow_origins` there if you deploy the frontend elsewhere.
