"""
CLI entry point for the Resume Tailor Agent.
"""

from pathlib import Path
import typer
from rich.console import Console
from resume_tailor import ResumeTailor

console = Console()

def tailor(
    resume: Path = typer.Option(..., help="Path to the input LaTeX resume file"),
    job_desc: Path = typer.Option(..., help="Path to the job description text file"),
    output: Path = typer.Option(..., help="Path to save the tailored LaTeX resume"),
    api_key: str = typer.Option(None, envvar="GEMINI_API_KEY", help="Gemini API Key")
):
    """
    Tailor a resume based on a job description using Google Gemini.
    """
    if not resume.exists():
        console.print(f"[bold red]Error:[/bold red] Resume file not found: {resume}")
        raise typer.Exit(code=1)
    if not job_desc.exists():
        console.print(f"[bold red]Error:[/bold red] Job description file not found: {job_desc}")
        raise typer.Exit(code=1)

    try:
        # Read input files
        with open(resume, "r", encoding="utf-8") as f:
            resume_content = f.read()
        with open(job_desc, "r", encoding="utf-8") as f:
            job_desc_content = f.read()

        console.print("[bold green]Reading files...[/bold green]")

        # Initialize agent
        agent = ResumeTailor(api_key=api_key)

        console.print("[bold blue]Tailoring resume with Gemini...[/bold blue]")
        tailored_content = agent.tailor(resume_content, job_desc_content)

        # Write output
        with open(output, "w", encoding="utf-8") as f:
            f.write(tailored_content)

        console.print(f"[bold green]Success![/bold green] Tailored resume saved to: {output}")

    except Exception as e:
        console.print(f"[bold red]An error occurred:[/bold red] {str(e)}")
        # raise e # Uncomment for full traceback during debugging
        raise typer.Exit(code=1)

if __name__ == "__main__":
    typer.run(tailor)
