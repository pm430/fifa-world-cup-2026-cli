# ⚽ fifa-world-cup-2026-cli

> **2026 FIFA 북중미 월드컵, 터미널에서 문자중계로**

```
  대한민국         2  :  1        독일
                      ● 진행중
```

브라우저도, 영상도, 알림도 필요 없습니다. 경기만 있으면 됩니다.

---

## 이런 분들께

- 월드컵을 보고 싶은데 화면을 띄울 수 없는 상황이신 분
- 터미널 탭 하나로 조용히 경기를 따라가고 싶은 분
- 텍스트로도 충분히 설레는 분

```
 15:45  ⚽ 골!!! 이강인의 프리킥이 그대로 골문으로! 대한민국 1-0 독일!!
 23:00  🟡 파울! 크로스가 손흥민을 걷어찹니다. 경고카드!
 40:00  📺 VAR 판독 중... 핸드볼 여부 확인.
 42:15  ⚽ 골!!!! 손흥민!!! 노이어의 방향을 속이며 왼쪽 구석으로! 2-1!
```

---

## 설치

> 터미널(Terminal / 명령 프롬프트)이 처음이신 분도 아래 순서대로 따라오시면 됩니다.

### 1단계 — 터미널 열기

| 운영체제 | 방법 |
|---|---|
| **Mac** | `Cmd + Space` → "Terminal" 검색 → 실행 |
| **Windows** | `Win + R` → `cmd` 입력 → 확인 |

### 2단계 — Python 설치 확인

터미널에 아래 명령어를 입력하세요.

```bash
python3 --version
```

`Python 3.8.x` 이상이 출력되면 다음 단계로 이동하세요.

출력이 없거나 오류가 나면 Python을 먼저 설치해야 합니다.
- **Mac** → [python.org/downloads](https://www.python.org/downloads/) 에서 다운로드 후 설치
- **Windows** → [python.org/downloads](https://www.python.org/downloads/) 에서 다운로드. 설치 시 **"Add Python to PATH"** 체크 필수!

> Windows에서 `python3`이 안 되면 `python --version` 을 대신 써보세요.

### 3단계 — 다운로드 및 설치

아래 명령어를 터미널에 한 줄씩 순서대로 입력하세요.

**Mac / Linux**

```bash
git clone https://github.com/pm430/fifa-world-cup-2026-cli
cd fifa-world-cup-2026-cli
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

**Windows**

```cmd
git clone https://github.com/pm430/fifa-world-cup-2026-cli
cd fifa-world-cup-2026-cli
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

> `git` 명령어가 없다는 오류가 나오면 → [git-scm.com](https://git-scm.com/downloads) 에서 Git 설치 후 다시 시도하세요.
>
> `python` 명령어 실행 시 Microsoft Store로 연결되거나 오류가 나면 `py` 런처를 대신 사용하세요.
> ```cmd
> py -m venv .venv
> ```

설치가 끝나면 이런 메시지가 보입니다.

```
Successfully installed click-... requests-... rich-...
```

API 키 없음. 가입 없음. 이게 전부입니다.

### 4단계 — 데모로 확인

```bash
python fifa_wc.py watch --demo
```

아래와 같은 화면이 나오면 성공입니다!

```
╭──────── ⚽  FIFA 월드컵 2026 ─────────╮
│  대한민국    2  :  1    독일           │
│              ● 진행중                 │
╰────────────────────────────────────────╯
 15:45  ⚽ 골!!! 이강인의 프리킥이 그대로 골문으로!
```

---

## 사용법

```bash
# 문자중계 시작 — 경기 목록이 뜨고 번호로 선택
python fifa_wc.py watch

# 오늘 경기 일정만 보기
python fifa_wc.py list

# 특정 날짜 경기
python fifa_wc.py list -d 20260626

# 지금 진행 중인 경기
python fifa_wc.py live

# 데모 먼저 구경하기
python fifa_wc.py watch --demo
```

> **다음에 다시 열 때는** 터미널에서 프로젝트 폴더로 이동한 뒤, 가상환경을 다시 활성화해야 합니다.
> ```bash
> cd fifa-world-cup-2026-cli
> source .venv/bin/activate   # Windows는: .venv\Scripts\activate
> ```

---

## 명령어

| 명령어 | 설명 |
|---|---|
| `watch` | 오늘 경기 목록에서 번호로 선택 후 문자중계 시작 |
| `watch <경기ID>` | 특정 경기 ID로 바로 문자중계 시작 |
| `watch --refresh 30` | 새로고침 간격 설정 (기본: 15초) |
| `watch --demo` | 라이브 경기 없이 데모 화면 보기 |
| `list` | 오늘 월드컵 경기 일정 보기 |
| `list -d YYYYMMDD` | 특정 날짜 경기 일정 |
| `live` | 현재 진행 중인 경기 확인 |

---

## 어떻게 동작하나요?

네이버 스포츠의 일정 및 문자중계 API에서 데이터를 가져옵니다. 스크래핑이나 headless 브라우저 없이, HTTPS JSON 요청으로 빠르게 동작합니다.

기본 15초 간격으로 새 이벤트를 가져오며, 이벤트가 없으면 타임스탬프만 출력합니다. 종료는 Ctrl+C.

> **참고:** 비공식 API를 사용합니다. 오늘은 잘 되지만, 네이버가 API를 변경하면 동작하지 않을 수 있습니다.

---

## 요구 사항

- Python 3.8 이상
- `click`, `rich`, `requests`

---

## 데모 화면

```
python fifa_wc.py watch --demo --refresh 2
```

```
╭─────────────────── ⚽  FIFA 월드컵 2026 ────────────────────╮
│                                                              │
│          대한민국    2  :  1    독일                          │
│                                                              │
│                       ● 진행중                               │
╰──────────────────── 조별 예선 C조 ──────────────────────────╯

 ── 이전 중계 ──────────────────────────────────────────────────
  0:01  🏁 경기 시작! 대한민국의 킥오프로 시작됩니다.
 15:45  ⚽ 골!!! 이강인의 프리킥이 그대로 골문으로! 대한민국 1-0 독일!!
 23:00  🟡 파울! 크로스가 손흥민을 걷어찹니다. 경고카드!
 33:50  ⚽ 골! 독일이 동점골로 따라붙습니다. 1-1.
 42:15  ⚽ 골!!!! 손흥민!!! 노이어의 방향을 속이며 왼쪽 구석으로! 2-1!
 ── 실시간 ──────────────────────────────────────────────────────
 58:00  황인범이 측면을 뚫고 올라갑니다! 크로스!!
                                      ── 15:04:32 새로고침 ──
```

---

## 라이선스

MIT
