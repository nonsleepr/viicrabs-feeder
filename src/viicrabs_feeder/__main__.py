import asyncio
import sys
from pathlib import Path
import re

from rich.console import Console
from rich.text import Text
import typer
from typing_extensions import Annotated
import httpx

from . import SevenCrabsFeeder

app = typer.Typer()

def get_from_url(url: str) -> dict:
    response = httpx.get(url)
    if response.status_code != 200:
        raise typer.BadParameter(f"Failed to fetch content from {url}: {response.status_code}")
    # TODO: Simplify HTML, extract title and description, etc.
    return {"content": response.text, "file_type": "text/html", "url": url, "source": "url"}
    
def parse_content(content: str, filename: str = None) -> dict:
    # TODO: Only support plain text for now
    result = {"content": content, "file_type": "text/plain"}
    if filename:
        result["source"] = filename
    result["title"] = result["content"].split("\n")[0]
    return result

def expand_content(content: str) -> dict:
    if content == "-":
        if sys.stdin.isatty():
            raise typer.BadParameter("No content provided and stdin is a TTY")
        else:
            return parse_content(sys.stdin.read())
    elif content.startswith("http://") or content.startswith("https://"):
        return get_from_url(content)
    elif Path(content).exists():
        with open(content, "r") as f:
            return parse_content(f.read(), content)
    elif re.match(r"^[-_a-zA-Z0-9./]{1,100}$", content):
        raise typer.BadParameter(f"Looks like a filename, but it doesn't exist: {content}")
    return parse_content(content)
    
@app.command()
def login(username: Annotated[str, typer.Option(help="ElevenLabs account email", prompt=True)],
          password: Annotated[str, typer.Option(help="ElevenLabs account password", prompt=True, hide_input=True)]):
    feeder = SevenCrabsFeeder(username, password)
    #asyncio.run(feeder.login())

@app.command()
def add(
    content: Annotated[str, typer.Argument(help="Content to add")] = "-",
    title: str = None,
    description: str = None,
):
    content = expand_content(content)
    if title:
        content["title"] = title
    if description:
        content["description"] = description
    feeder = SevenCrabsFeeder()
    result = asyncio.run(feeder.add_article(**content))
    with Console() as console:
        text = Text("Added an article to ElevenLabs Reader: ")
        text.append(Text(result["read_id"], style="bold magenta"))
        console.print(text)


@app.command()
def add_podcast(
    content: Annotated[str, typer.Argument(help="Content to add")] = "-",
    title: str = None,
    description: str = None,
):
    content = expand_content(content)
    if title:
        content["title"] = title
    if description:
        content["description"] = description
    feeder = SevenCrabsFeeder()
    result = asyncio.run(feeder.add_podcast(**content))
    with Console() as console:
        text = Text("Added a podcast to ElevenLabs Reader: ")
        text.append(Text(result["read_id"], style="bold magenta"))
        console.print(text)

@app.command()
def delete(read_id: str):
    feeder = SevenCrabsFeeder()
    asyncio.run(feeder.delete_article(read_id))
    with Console() as console:
        text = Text("Deleted an article from ElevenLabs Reader: ")
        text.append(Text(read_id, style="bold magenta"))
        console.print(text)

if __name__ == "__main__":
    app()