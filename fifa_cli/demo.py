"""--demo 플래그용 모의 데이터"""
from .models import EventType, Match, MatchStatus, RelayEvent, Team

DEMO_MATCH = Match(
    game_id="DEMO_2026_KOR_GER",
    home=Team(name="대한민국", score=2),
    away=Team(name="독일", score=1),
    status=MatchStatus.LIVE,
    date="20260619",
    time="21:00",
    stage="조별 예선 C조",
)

DEMO_EVENTS = [
    RelayEvent("1", "0:01", "경기 시작! 대한민국의 킥오프로 시작됩니다.", EventType.KICKOFF),
    RelayEvent("2", "3:22", "이강인이 왼쪽 측면에서 드리블을 시작합니다.", EventType.GENERAL),
    RelayEvent("3", "8:44", "뮐러가 헤더 슛! 조현우 선방!", EventType.GENERAL),
    RelayEvent("4", "15:10", "손흥민이 페널티 박스 부근에서 파울을 얻어냅니다.", EventType.GENERAL),
    RelayEvent("5", "15:30", "프리킥 상황. 이강인이 키커로 나섭니다.", EventType.GENERAL),
    RelayEvent("6", "15:45", "골!!! 이강인의 프리킥이 그대로 골문으로! 대한민국 1-0 독일!!", EventType.GOAL),
    RelayEvent("7", "23:00", "파울! 크로스가 손흥민을 걷어찹니다. 경고카드!", EventType.YELLOW_CARD),
    RelayEvent("8", "31:15", "독일이 역습! 뮐러 - 그나브리 - 하버츠로 이어지는 패스.", EventType.GENERAL),
    RelayEvent("9", "33:50", "하버츠 슛! 골! 독일이 동점골로 따라붙습니다. 1-1.", EventType.GOAL),
    RelayEvent("10", "40:00", "VAR 판독 중... 핸드볼 여부 확인.", EventType.VAR),
    RelayEvent("11", "41:10", "VAR 판독 결과: 페널티킥! 대한민국에게 기회가 왔습니다!", EventType.GENERAL),
    RelayEvent("12", "42:00", "손흥민이 페널티킥 키커로 나섭니다.", EventType.GENERAL),
    RelayEvent("13", "42:15", "골!!!! 손흥민!!! 노이어의 방향을 속이며 왼쪽 구석으로! 2-1!", EventType.GOAL),
    RelayEvent("14", "45:00", "전반전 종료. 대한민국 2-1 독일", EventType.HALFTIME),
    RelayEvent("15", "45:01", "하프타임. 15분간의 휴식 시간입니다.", EventType.GENERAL),
    RelayEvent("16", "46:00", "후반전 시작! 독일의 킥오프.", EventType.KICKOFF),
    RelayEvent("17", "52:30", "교체: 독일 — 뮐러 아웃, 자네 인.", EventType.SUBSTITUTION),
    RelayEvent("18", "58:00", "황인범이 측면을 뚫고 올라갑니다! 크로스!!", EventType.GENERAL),
    RelayEvent("19", "67:00", "현재 상황: 대한민국 2-1 독일 | 후반 22분 경과", EventType.GENERAL),
]
