# type: ignore[attr-defined]
import os
import sys
from enum import Enum
from pathlib import Path

import typer
from ansify import __version__
from ansify import settings as conf
from ansify.ansify import ansi_art
from rich.console import Console

app = typer.Typer(
    name="ansify",
    help="CLI to create ANSI/ASCII art from images.",
    add_completion=False,
)
console = Console()
rows, cols = os.popen("stty size", "r").read().split()


class Grayscale(str, Enum):
    simple = "simple"
    morelevels = "morelevels"
    pixel = "pixel"
    dragon = "dragon"
    emoji = "emoji"


def version_callback(value: bool):
    """Prints the version of the package."""
    if value:
        console.print(f"[yellow]ansify[/] version: [bold blue]{__version__}[/]")
        raise typer.Exit()


@app.command(name="CLI to create ANSI/ASCII art from images.")
def main(
    image: str = typer.Argument(..., help="Image file PATH or URL."),
    columns: int = typer.Option(cols, "-c", "--columns", help="Output columns, number of characters per line."),
    output: Path = typer.Option(None, "-o", "--output", help="Save ANSI/ASCII art to the OUTPUT file."),
    scale: float = typer.Option(conf.SCALE, "-s", "--scale", help="The larger the scale, the thinner the art."),
    grayscale: Grayscale = typer.Option(Grayscale.simple, "-g", "--grayscale", help="Choose a built-in gray scale."),
    diy_grayscale: str = typer.Option(None, "-d", "--diy-grayscale", help="Customize your gray scale."),
    no_color: bool = typer.Option(False, "-n", "--no-color", help="Output a ANSI/ASCII art without color."),
    reverse_grayscale: bool = typer.Option(False, "-r", "--reverse-grayscale", help="Reverse the grayscale."),
    reverse_color: bool = typer.Option(False, "-R", "--reverse-color", help="Reverse the color."),
    quiet: bool = typer.Option(False, "-q", "--quite", help="Hide output information."),
    version: bool = typer.Option(
        None,
        "-v",
        "--version",
        callback=version_callback,
        is_eager=True,
        help="Prints the version of the ansify package.",
    ),
):
    """CLI to create ANSI/ASCII art from images."""
    try:
        ansi_art(
            src=image,
            columns=columns,
            output=output,
            scale=scale,
            grayscale=grayscale,
            diy_grayscale=diy_grayscale,
            no_color=no_color,
            reverse_grayscale=reverse_grayscale,
            reverse_color=reverse_color,
            quiet=quiet,
        )
    except Exception as e:
        console.print(f"[red]{e}[/]")
        sys.exit(1)
