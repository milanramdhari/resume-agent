"""
Debug script for Typer CLI argument parsing.
"""

from pathlib import Path
import typer

app = typer.Typer()

@app.command()
def main(
    name: str = typer.Option(..., help="Name to greet"),
    age: int = typer.Option(None, help="Age of the person"),
    file: Path = typer.Option(None, help="A file path")
):
    """
    A simple debug command.
    """
    print(f"Hello {name}")
    if age:
        print(f"You are {age} years old")
    if file:
        print(f"File path: {file}")

if __name__ == "__main__":
    app()
