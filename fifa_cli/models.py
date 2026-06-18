from dataclasses import dataclass
from enum import Enum


class MatchStatus(str, Enum):
    BEFORE = "BEFORE"
    LIVE = "LIVE"
    HALFTIME = "HALFTIME"
    FINAL = "FINAL"
    UNKNOWN = "UNKNOWN"


class EventType(str, Enum):
    GOAL = "GOAL"
    YELLOW_CARD = "YELLOW_CARD"
    RED_CARD = "RED_CARD"
    SUBSTITUTION = "SUBSTITUTION"
    VAR = "VAR"
    KICKOFF = "KICKOFF"
    HALFTIME = "HALFTIME"
    FULLTIME = "FULLTIME"
    GENERAL = "GENERAL"


@dataclass
class Team:
    name: str
    score: int = 0


@dataclass
class Match:
    game_id: str
    home: Team
    away: Team
    status: MatchStatus
    date: str   # YYYYMMDD
    time: str   # HH:MM (KST)
    stage: str = ""


@dataclass
class RelayEvent:
    event_id: str
    game_time: str
    text: str
    event_type: EventType = EventType.GENERAL
