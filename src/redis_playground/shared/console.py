"""Rich-based structured console logging for Redis exercises.

Mirrors flink-playground's Console.java, using Rich for beautiful output
with colored sections, command highlights, tables, and panels.
"""

from rich.console import Console as RichConsole
from rich.table import Table
from rich.panel import Panel
from rich import box

_console = RichConsole()


class Console:
    """Structured logger for exercise output with Rich formatting."""

    def __init__(self, module_id: str):
        self.module_id = module_id

    @staticmethod
    def for_module(module_id: str) -> "Console":
        return Console(module_id)

    def header(self, text: str) -> None:
        _console.print()
        _console.print(Panel(text, style="bold cyan", box=box.HEAVY))

    def section(self, text: str) -> None:
        _console.print()
        _console.print(f"[bold blue]── {text} ──[/bold blue]")

    def step(self, number: int, description: str) -> None:
        _console.print(
            f"  [bold yellow]Step {number}:[/bold yellow] [dim]{description}[/dim]"
        )

    def concept(self, text: str) -> None:
        _console.print(f"  [dim italic]💡 {text}[/dim italic]")

    def command(self, cmd: str, comment: str = "") -> None:
        suffix = f"  [dim]# {comment}[/dim]" if comment else ""
        _console.print(f"  [bold green]$[/bold green] [white]{cmd}[/white]{suffix}")

    def info(self, text: str) -> None:
        _console.print(f"  [cyan]ℹ {text}[/cyan]")

    def success(self, text: str) -> None:
        _console.print(f"  [green]✓ {text}[/green]")

    def warn(self, text: str) -> None:
        _console.print(f"  [yellow]⚠ {text}[/yellow]")

    def error(self, text: str) -> None:
        _console.print(f"  [red]✗ {text}[/red]")

    def output(self, text: str) -> None:
        _console.print(f"    [dim white]→ {text}[/dim white]")

    def key_value(self, key: str, value: str) -> None:
        _console.print(f"  [bold]{key}:[/bold] {value}")

    def table(self, headers: list[str], rows: list[list[str]], title: str = "") -> None:
        t = Table(title=title, box=box.SIMPLE, header_style="bold cyan")
        for h in headers:
            t.add_column(h)
        for row in rows:
            t.add_row(*[str(c) for c in row])
        _console.print(t)

    def separator(self) -> None:
        _console.print("  [dim]─" * 40 + "[/dim]")

    def summary(self, text: str) -> None:
        _console.print()
        _console.print(Panel(text, style="bold green", box=box.SQUARE))
