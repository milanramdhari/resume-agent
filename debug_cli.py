import typer
from pathlib import Path

app = typer.Typer()

@app.command()
def tailor(
    resume: Path = typer.Option(..., help="Path to resume"),
    job_desc: Path = typer.Option(..., help="Path to job desc"),
    output: Path = typer.Option(..., help="Path to output"),
    api_key: str = typer.Option(None, envvar="GEMINI_API_KEY")
):
    print(f"Resume: {resume}")
    print(f"Job Desc: {job_desc}")
    print(f"Output: {output}")
    print(f"API Key: {api_key}")

if __name__ == "__main__":
    app()
