import re
from datetime import datetime
from typing import List

from rich import box
from rich.console import Console
from rich.markup import escape
from rich.panel import Panel
from rich.table import Table
from rich.text import Text

from .models import EventType, Match, MatchStatus, RelayEvent

# CSI sequences (\x1b[...m), OSC sequences (\x1b]...\x07 or \x1b]...\x1b\\), other C1
_ANSI_RE = re.compile(
    r"\x1b(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~]|\][^\x07]*(?:\x07|\x1b\\))"
)


def _strip_ansi(text: str) -> str:
    return _ANSI_RE.sub("", text)

console = Console()

_ICONS = {
    EventType.GOAL: "⚽",
    EventType.YELLOW_CARD: "🟡",
    EventType.RED_CARD: "🔴",
    EventType.SUBSTITUTION: "🔄",
    EventType.VAR: "📺",
    EventType.KICKOFF: "🏁",
    EventType.HALFTIME: "⏸ ",
    EventType.FULLTIME: "🏆",
    EventType.GENERAL: "  ",
}

_STYLES = {
    EventType.GOAL: "bold bright_yellow",
    EventType.YELLOW_CARD: "yellow",
    EventType.RED_CARD: "bold red",
    EventType.SUBSTITUTION: "cyan",
    EventType.VAR: "magenta",
    EventType.KICKOFF: "bold green",
    EventType.HALFTIME: "dim",
    EventType.FULLTIME: "bold white",
    EventType.GENERAL: "",
}

_STATUS_LABELS = {
    MatchStatus.BEFORE: "[dim]경기전[/dim]",
    MatchStatus.LIVE: "[bold green]● LIVE[/bold green]",
    MatchStatus.HALFTIME: "[yellow]하프타임[/yellow]",
    MatchStatus.FINAL: "[dim]종  료[/dim]",
    MatchStatus.UNKNOWN: "[dim] —— [/dim]",
}

_STATUS_TEXT = {
    MatchStatus.BEFORE: "경기 전",
    MatchStatus.LIVE: "● 진행중",
    MatchStatus.HALFTIME: "하프타임",
    MatchStatus.FINAL: "경기 종료",
    MatchStatus.UNKNOWN: "",
}


def render_match_list(matches: List[Match]) -> Table:
    table = Table(
        title="[bold cyan]⚽  FIFA 월드컵 2026  경기 일정[/bold cyan]",
        box=box.ROUNDED,
        border_style="cyan",
        header_style="bold cyan",
        show_lines=False,
        padding=(0, 1),
    )
    table.add_column("#", style="dim", width=3, justify="right")
    table.add_column("상태", width=10, justify="center")
    table.add_column("시간(KST)", width=10, justify="center")
    table.add_column("홈팀", min_width=12, justify="right")
    table.add_column("스코어", width=9, justify="center")
    table.add_column("원정팀", min_width=12, justify="left")
    table.add_column("경기ID", style="dim cyan", min_width=16, no_wrap=True)

    for i, m in enumerate(matches, 1):
        if m.status == MatchStatus.BEFORE:
            score_str = "[dim]  vs  [/dim]"
        else:
            hs = "bold bright_yellow" if m.home.score > m.away.score else "bold"
            as_ = "bold bright_yellow" if m.away.score > m.home.score else "bold"
            score_str = f"[{hs}]{m.home.score}[/{hs}] [dim]:[/dim] [{as_}]{m.away.score}[/{as_}]"

        table.add_row(
            str(i),
            _STATUS_LABELS.get(m.status, str(m.status)),
            m.time or "—",
            escape(m.home.name),
            score_str,
            escape(m.away.name),
            escape(m.game_id),
        )
    return table


def render_score_header(match: Match) -> Panel:
    hs = "bold bright_yellow" if match.home.score > match.away.score else "bold white"
    as_ = "bold bright_yellow" if match.away.score > match.home.score else "bold white"

    body = Text(justify="center")
    body.append("\n")
    body.append(f"{match.home.name:>14}", style=hs)
    body.append("    ")
    body.append(f"{match.home.score}", style=hs)
    body.append("  :  ")
    body.append(f"{match.away.score}", style=as_)
    body.append("    ")
    body.append(f"{match.away.name:<14}", style=as_)

    body.append(f"\n\n{_STATUS_TEXT.get(match.status, '')}\n", style="dim")

    subtitle = f"[dim]{escape(match.stage)}[/dim]" if match.stage else None
    return Panel(
        body,
        title="[bold cyan]⚽  FIFA 월드컵 2026[/bold cyan]",
        subtitle=subtitle,
        border_style="cyan",
        expand=True,
    )


def render_event(event: RelayEvent) -> Text:
    icon = _ICONS.get(event.event_type, "  ")
    style = _STYLES.get(event.event_type, "")
    time_col = f"{event.game_time:>5}" if event.game_time else " " * 5

    t = Text()
    t.append(f" {time_col}  ", style="dim")
    t.append(f"{icon} ")
    t.append(_strip_ansi(event.text), style=style)
    return t


def render_refresh_line() -> Text:
    now = datetime.now().strftime("%H:%M:%S")
    t = Text(justify="right")
    t.append(f" ── {now} 새로고침 ── ", style="dim")
    return t
