"""
Simple debug script using typer.run.
"""

import typer

def main(name: str):
    """
    Simple greeting function.
    """
    print(f"Hello {name}")

if __name__ == "__main__":
    typer.run(main)
