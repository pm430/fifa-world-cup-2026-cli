#!/usr/bin/env python3
"""FIFA 월드컵 2026 문자중계 CLI — 직장인을 위한 조용한 터미널 관람"""
import sys
import time
from datetime import datetime
from typing import List, Optional, Set

import click
import requests

from fifa_cli.api import fetch_game, fetch_relay, fetch_schedule
from fifa_cli.display import (
    console,
    render_event,
    render_match_list,
    render_refresh_line,
    render_score_header,
)
from fifa_cli.models import Match, MatchStatus, RelayEvent


# ── 공통 오류 처리 ──────────────────────────────────────────────────────────

def _handle_api_error(e: Exception) -> None:
    console.print(f"\n[red]API 오류:[/red] {e}")
    console.print(
        "[dim]네이버 스포츠 API에 접근할 수 없습니다.\n"
        "  • 네트워크 연결 확인\n"
        "  • 잠시 후 재시도\n"
        "  • --demo 플래그로 데모 화면 확인 가능 (watch 명령)[/dim]"
    )


# ── CLI 그룹 ────────────────────────────────────────────────────────────────

@click.group()
@click.version_option("1.0.0", prog_name="fifa-wc")
def cli() -> None:
    """⚽  FIFA 월드컵 2026 문자중계 CLI

    \b
    사용 예시:
      python fifa_wc.py list              # 오늘 경기 목록
      python fifa_wc.py list -d 20260626  # 특정 날짜 경기
      python fifa_wc.py live              # 현재 LIVE 경기
      python fifa_wc.py watch <경기ID>    # 문자중계 시작
      python fifa_wc.py watch --demo      # 데모 화면 보기
    """


# ── list ────────────────────────────────────────────────────────────────────

@cli.command("list")
@click.option("--date", "-d", default=None, metavar="YYYYMMDD", help="날짜 (기본값: 오늘)")
def cmd_list(date: Optional[str]) -> None:
    """경기 일정 목록 보기"""
    target = date or datetime.now().strftime("%Y%m%d")
    fmt = f"{target[:4]}-{target[4:6]}-{target[6:]}"
    console.print(f"\n[dim]  {fmt} 경기 일정 조회 중...[/dim]\n")

    try:
        matches = fetch_schedule(target)
    except requests.RequestException as e:
        _handle_api_error(e)
        sys.exit(1)

    if not matches:
        console.print(f"[yellow]  {fmt}에 예정된 경기가 없습니다.[/yellow]\n")
        return

    console.print(render_match_list(matches))
    console.print(
        "\n[dim]  💡  python fifa_wc.py watch <경기ID>  로 문자중계를 시작하세요[/dim]\n"
    )


# ── live ────────────────────────────────────────────────────────────────────

@cli.command("live")
def cmd_live() -> None:
    """현재 진행 중인 경기 확인"""
    today = datetime.now().strftime("%Y%m%d")
    console.print("\n[dim]  진행 중인 경기 확인 중...[/dim]\n")

    try:
        matches = fetch_schedule(today)
    except requests.RequestException as e:
        _handle_api_error(e)
        sys.exit(1)

    live = [m for m in matches if m.status == MatchStatus.LIVE]

    if not live:
        console.print("[yellow]  현재 진행 중인 경기가 없습니다.[/yellow]")
        upcoming = [m for m in matches if m.status == MatchStatus.BEFORE]
        if upcoming:
            nxt = upcoming[0]
            console.print(
                f"[dim]  다음 예정: {nxt.home.name} vs {nxt.away.name}  ({nxt.time} KST)[/dim]"
            )
        console.print()
        return

    console.print(render_match_list(live))
    console.print(
        "\n[dim]  💡  python fifa_wc.py watch <경기ID>  로 문자중계를 시작하세요[/dim]\n"
    )


# ── watch ───────────────────────────────────────────────────────────────────

@cli.command("watch")
@click.argument("game_id", required=False, default=None)
@click.option("--refresh", "-r", default=15, show_default=True, help="새로고침 간격 (초)")
@click.option("--demo", is_flag=True, default=False, help="데모 모드 (모의 경기 데이터)")
def cmd_watch(game_id: Optional[str], refresh: int, demo: bool) -> None:
    """문자중계 보기

    \b
    GAME_ID: 경기 고유 번호 (list 명령으로 확인)
    데모:    python fifa_wc.py watch --demo
    """
    if demo:
        _run_demo(refresh)
        return

    if not game_id:
        console.print("[red]오류:[/red] 경기 ID를 입력하세요.\n")
        console.print("[dim]  예시: python fifa_wc.py watch 2026WFOOTBALL001[/dim]")
        console.print("[dim]  목록: python fifa_wc.py list[/dim]\n")
        sys.exit(1)

    console.print(f"\n[cyan]  경기 ID:[/cyan] {game_id}")
    console.print(f"[dim]  {refresh}초 자동 새로고침  |  Ctrl+C 종료[/dim]\n")

    match: Optional[Match] = None
    seen: Set[str] = set()
    events: List[RelayEvent] = []

    # 초기 경기 정보 로드
    try:
        match = fetch_game(game_id)
        if match:
            console.print(render_score_header(match))
    except requests.RequestException:
        pass

    # 초기 문자중계 이벤트 로드
    try:
        initial = fetch_relay(game_id)
        for e in initial:
            seen.add(e.event_id)
            events.append(e)
        if events:
            console.rule("[dim]이전 중계[/dim]", style="dim")
            for e in events:
                console.print(render_event(e))
            console.rule("[dim]실시간[/dim]", style="dim green")
    except requests.RequestException as e:
        console.print(f"[red]  초기 중계 로드 실패:[/red] {e}\n")

    try:
        while True:
            time.sleep(refresh)
            try:
                updated = fetch_game(game_id)
                if updated:
                    if match is None or (
                        updated.home.score != match.home.score
                        or updated.away.score != match.away.score
                        or updated.status != match.status
                    ):
                        match = updated
                        console.print(render_score_header(match))

                new_events = fetch_relay(game_id)
                added = 0
                for e in new_events:
                    if e.event_id not in seen:
                        seen.add(e.event_id)
                        events.append(e)
                        console.print(render_event(e))
                        added += 1

                if not added:
                    console.print(render_refresh_line())

            except requests.RequestException as e:
                console.print(f"[dim red]  새로고침 실패: {e}[/dim red]")

            if match and match.status == MatchStatus.FINAL:
                console.print("\n[bold]  경기가 종료되었습니다. 수고하셨습니다! ⚽[/bold]\n")
                break

    except KeyboardInterrupt:
        console.print("\n[dim]  종료합니다. ⚽[/dim]\n")


# ── 데모 모드 ────────────────────────────────────────────────────────────────

def _run_demo(refresh: int) -> None:
    from fifa_cli.demo import DEMO_EVENTS, DEMO_MATCH

    console.print("\n[dim]  ── 데모 모드 ──  실제 API 미사용  ──[/dim]\n")
    console.print(render_score_header(DEMO_MATCH))
    console.rule("[dim]이전 중계[/dim]", style="dim")

    # 이전 이벤트 즉시 출력
    for e in DEMO_EVENTS[:-3]:
        console.print(render_event(e))

    console.rule("[dim]실시간[/dim]", style="dim green")

    # 마지막 3개 이벤트를 refresh 간격으로 하나씩 출력
    remaining = list(DEMO_EVENTS[-3:])
    try:
        for i, e in enumerate(remaining):
            time.sleep(min(refresh, 5))
            console.print(render_event(e))
            console.print(render_refresh_line())

        console.print(
            "\n[dim]  데모가 끝났습니다. list / watch 명령으로 실제 경기를 보세요.[/dim]\n"
        )
    except KeyboardInterrupt:
        console.print("\n[dim]  종료합니다. ⚽[/dim]\n")


# ── 엔트리포인트 ─────────────────────────────────────────────────────────────

if __name__ == "__main__":
    cli()
