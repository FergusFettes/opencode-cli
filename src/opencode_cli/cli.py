import typer
from typing import Optional
from rich.console import Console
from rich.table import Table
from rich.json import JSON

from .client import OpencodeClientWrapper

app = typer.Typer(
    help="CLI tool for opencode server API - interact with running opencode servers",
    epilog="Connects to opencode server at http://localhost:36000 by default"
)
console = Console()


def handle_error(e: Exception):
    console.print(f"[red]Error:[/red] {e}")
    raise typer.Exit(1)


@app.command()
def sessions(
    json: bool = typer.Option(False, "--json", help="Output raw JSON"),
):
    """
    List all sessions on the opencode server.
    
    Example: oc sessions
    """
    try:
        client = OpencodeClientWrapper()
        sessions_data = client.list_sessions()
        
        if json:
            console.print(JSON.from_data([s.model_dump() for s in sessions_data]))
            return
        
        if not sessions_data:
            console.print("[yellow]No sessions found[/yellow]")
            return
        
        table = Table(title="OpenCode Sessions")
        table.add_column("ID", style="cyan")
        table.add_column("Title", style="green")
        table.add_column("Created", style="yellow")
        
        for session in sessions_data:
            table.add_row(
                session.id or "",
                session.title or "Untitled",
                str(session.time.created if session.time else "")
            )
        
        console.print(table)
        
    except Exception as e:
        handle_error(e)


@app.command()
def messages(
    session_id: str = typer.Argument(..., help="Session ID or title"),
    json: bool = typer.Option(False, "--json", help="Output raw JSON"),
):
    """
    List all messages in a session.
    
    Example: oc messages abc123
    Example: oc messages headless-1
    """
    try:
        client = OpencodeClientWrapper()
        messages_data = client.list_messages(session_id)
        
        if json:
            console.print(JSON.from_data([{"info": m.info.model_dump(), "parts": [p.model_dump() for p in m.parts]} for m in messages_data]))
            return
        
        if not messages_data:
            console.print("[yellow]No messages found[/yellow]")
            return
        
        for msg in messages_data:
            info = msg.info
            parts = msg.parts
            
            role = info.role or "unknown"
            timestamp = info.time_created or ""
            
            console.print(f"\n[bold cyan]{role.upper()}[/bold cyan] [{timestamp}]")
            
            for part in parts:
                part_dict = part.model_dump()
                if part_dict.get("type") == "text":
                    console.print(part_dict.get("text", ""))
                elif part_dict.get("type") == "tool_use":
                    console.print(f"[yellow]Tool: {part_dict.get('name')}[/yellow]")
                elif part_dict.get("type") == "tool_result":
                    console.print(f"[green]Result: {str(part_dict.get('content', ''))[:100]}...[/green]")
        
    except Exception as e:
        handle_error(e)


@app.command()
def send(
    session_id: str = typer.Argument(..., help="Session ID or title"),
    message: str = typer.Argument(..., help="Message to send"),
):
    """
    Send a message to a session.
    
    Example: oc send abc123 "hello world"
    Example: oc send headless-1 "hello world"
    """
    try:
        client = OpencodeClientWrapper()
        result = client.send_message(session_id, message)
        console.print(f"[green]Message sent successfully[/green]")
        console.print(f"Message ID: {result.info.id if result.info else 'unknown'}")
        
    except Exception as e:
        handle_error(e)


@app.command()
def create(
    title: Optional[str] = typer.Option(None, "--title", "-t", help="Session title"),
):
    """
    Create a new session.
    
    Example: oc create --title "My new session"
    """
    try:
        client = OpencodeClientWrapper()
        result = client.create_session(title)
        console.print(f"[green]Session created successfully[/green]")
        console.print(f"Session ID: {result.id or 'unknown'}")
        console.print(f"Title: {result.title or 'Untitled'}")
        
    except Exception as e:
        handle_error(e)


@app.command()
def info(
    session_id: str = typer.Argument(..., help="Session ID or title"),
    json: bool = typer.Option(False, "--json", help="Output raw JSON"),
):
    """
    Get detailed info about a session.
    
    Example: oc info abc123
    Example: oc info headless-1
    """
    try:
        client = OpencodeClientWrapper()
        session_data = client.get_session(session_id)
        
        if json:
            console.print(JSON.from_data(session_data.model_dump()))
            return
        
        console.print(f"[bold]Session Info[/bold]")
        console.print(f"ID: {session_data.id or ''}")
        console.print(f"Title: {session_data.title or 'Untitled'}")
        if session_data.time:
            console.print(f"Created: {session_data.time.created or ''}")
            console.print(f"Updated: {session_data.time.updated or ''}")
        
    except Exception as e:
        handle_error(e)


if __name__ == "__main__":
    app()
