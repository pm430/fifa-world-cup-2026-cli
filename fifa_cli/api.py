import requests
from datetime import datetime
from typing import Dict, List, Optional, Any

from .models import EventType, Match, MatchStatus, RelayEvent, Team

NAVER_API = "https://api-gw.sports.naver.com"

_SCHED_HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/125.0.0.0 Safari/537.36"
    ),
    "Referer": "https://sports.naver.com/",
    "Accept": "application/json, text/plain, */*",
    "Accept-Language": "ko-KR,ko;q=0.9",
}

# API가 반환하는 statusCode 중 Enum 값과 이름이 다른 것만 매핑
_STATUS_ALIASES: Dict[str, MatchStatus] = {
    "RESULT": MatchStatus.FINAL,
    "STARTED": MatchStatus.LIVE,
    "SCHEDULED": MatchStatus.BEFORE,
}


def _relay_headers(game_id: str) -> Dict[str, str]:
    return {
        **_SCHED_HEADERS,
        "Referer": f"https://m.sports.naver.com/game/{game_id}",
        "Origin": "https://m.sports.naver.com",
    }


def _parse_time_kst(dt_str: str) -> str:
    """'2026-06-19T10:00:00' → '10:00'"""
    try:
        return dt_str[11:16]
    except Exception:
        return ""


def _parse_status(code: str) -> MatchStatus:
    if code in _STATUS_ALIASES:
        return _STATUS_ALIASES[code]
    try:
        return MatchStatus(code)
    except ValueError:
        return MatchStatus.UNKNOWN


def _parse_match(g: dict, game_id: str) -> Match:
    """dict → Match 파싱 공용 헬퍼"""
    game_date = g.get("gameDate", "").replace("-", "")
    return Match(
        game_id=game_id,
        home=Team(
            name=g.get("homeTeamName", "홈팀"),
            score=int(g.get("homeTeamScore") or 0),
        ),
        away=Team(
            name=g.get("awayTeamName", "원정팀"),
            score=int(g.get("awayTeamScore") or 0),
        ),
        status=_parse_status(g.get("statusCode", "")),
        date=game_date,
        time=_parse_time_kst(g.get("gameDateTime", "")),
        stage=g.get("categoryName", ""),
    )


def fetch_schedule(date: Optional[str] = None) -> List[Match]:
    """오늘(또는 지정 날짜)의 월드컵 경기 목록 조회"""
    if not date:
        date = datetime.now().strftime("%Y%m%d")

    url = f"{NAVER_API}/schedule/games"
    params: Dict[str, Any] = {"page": 1, "size": 100}

    resp = requests.get(url, params=params, headers=_SCHED_HEADERS, timeout=10)
    resp.raise_for_status()
    data = resp.json()

    matches: List[Match] = []
    for g in (data.get("result") or {}).get("games", []):
        if g.get("categoryId") != "worldcup":
            continue
        game_date = g.get("gameDate", "").replace("-", "")
        if date and (not game_date or game_date != date):
            continue
        try:
            matches.append(_parse_match(g, str(g["gameId"])))
        except (KeyError, ValueError, TypeError):
            continue
    return matches


def fetch_game(game_id: str) -> Optional[Match]:
    """단일 경기 최신 스코어 조회"""
    url = f"{NAVER_API}/schedule/games/{game_id}"
    resp = requests.get(url, headers=_SCHED_HEADERS, timeout=10)
    resp.raise_for_status()
    g = (resp.json().get("result") or {}).get("game") or {}
    if not g:
        return None
    try:
        return _parse_match(g, game_id)
    except (KeyError, ValueError):
        return None


def fetch_relay(game_id: str) -> List[RelayEvent]:
    """문자중계 이벤트 조회"""
    url = f"{NAVER_API}/schedule/games/{game_id}/relay"
    resp = requests.get(url, headers=_relay_headers(game_id), timeout=10)
    resp.raise_for_status()
    data = resp.json()

    relay_data = (data.get("result") or {}).get("textRelayData") or {}
    events: List[RelayEvent] = []

    for r in relay_data.get("textRelays", []):
        try:
            type_str = r.get("relayType", "GENERAL")
            try:
                event_type = EventType(type_str)
            except ValueError:
                event_type = EventType.GENERAL

            raw_id = r.get("id") or r.get("relayId")
            game_time = str(r.get("gameTime") or r.get("currentGameTime") or "")
            text = str(r.get("relayContents") or r.get("relayText") or "")
            # id가 없으면 내용 기반 키로 중복 방지
            event_id = str(raw_id) if raw_id is not None else f"_{game_time}_{text[:40]}"

            event = RelayEvent(
                event_id=event_id,
                game_time=game_time,
                text=text,
                event_type=event_type,
            )
            events.append(event)
        except (KeyError, ValueError, TypeError):
            continue
    return events
