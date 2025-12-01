import typer
from rich.console import Console
from pathlib import Path
from resume_tailor import ResumeTailor

console = Console()

def tailor(
    resume: Path = typer.Option(..., help="Path to the input LaTeX resume file"),
    job_desc: Path = typer.Option(..., help="Path to the job description text file"),
    output: Path = typer.Option(..., help="Path to save the tailored LaTeX resume"),
    api_key: str = typer.Option(None, envvar="GEMINI_API_KEY", help="Gemini API Key")
):
    """
    Tailor a resume to a job description.
    """
    if not resume.exists():
        console.print(f"[bold red]Error:[/bold red] Resume file not found: {resume}")
        raise typer.Exit(code=1)
    
    if not job_desc.exists():
        console.print(f"[bold red]Error:[/bold red] Job description file not found: {job_desc}")
        raise typer.Exit(code=1)

    console.print("[yellow]Reading files...[/yellow]")
    resume_content = resume.read_text(encoding='utf-8')
    job_desc_content = job_desc.read_text(encoding='utf-8')

    console.print("[yellow]Initializing Resume Tailor...[/yellow]")
    tailor_agent = ResumeTailor(api_key=api_key)

    console.print("[green]Tailoring resume... (this may take a few seconds)[/green]")
    tailored_content = tailor_agent.tailor(resume_content, job_desc_content)

    console.print(f"[yellow]Saving to {output}...[/yellow]")
    output.write_text(tailored_content, encoding='utf-8')

    console.print(f"[bold green]Success![/bold green] Tailored resume saved to {output}")

if __name__ == "__main__":
    typer.run(tailor)
