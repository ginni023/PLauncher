# UiTheme

**화면 테마·글꼴·색 규칙 (한곳에 모음)**

ttkbootstrap의 **flatly**(밝은 테마)를 쓴다. 모든 창의 글꼴, 표 줄 높이, 버튼 크기, 상태 색을 여기서 정한다. 화면 모양을 바꿀 때는 이 클래스의 상수부터 고친다.

| 항목 | 값 |
|---|---|
| 테마 | `flatly` |
| 글꼴 | 맑은 고딕 9pt (제목·라벨은 굵게) |
| 표 줄 높이 | 26 |
| 버튼 안쪽 여백 | (10, 2) — 글자에 맞는 작은 버튼 |
| 표 머리글 | `primary` (남색) |
| 체크박스 | `primary-round-toggle` (켜고 끄는 스위치) |

**작업 상태 → 색**

| 상태 | 색 |
|---|---|
| RDY, WAIT | secondary (회색) |
| WRK | info (파랑) |
| CMP | success (초록) |
| FAIL, ERR | danger (빨강) |
| STOP | warning (주황) |

**동작 결과(ACT_RESULT) → 색·표시** — 결과값 형식이 아직 정해지지 않아 아래 단어로 판단한다 (대소문자 무시).
- 성공: `성공`, `SUCCESS`, `PASS`, `OK`, `Y`, `CMP` → 초록, 앞에 `✔`
- 실패: `실패`, `FAIL`, `ERROR`, `ERR`, `N` → 빨강, 앞에 `✖`
- 그 외: 기본 글자색

**버튼 스타일**

| 상수 | 용도 |
|---|---|
| `BUTTON_PRIMARY` | 주 버튼 (메인의 작업목록, 설정의 적용) |
| `BUTTON_SECONDARY` | 닫기 |
| `BUTTON_OUTLINE_SECONDARY` | 보조 (메인의 예약목록) |
| `BUTTON_OUTLINE_DANGER` | 오류 |
| `BUTTON_OUTLINE_PRIMARY` | 인증 |

## 메서드

| 메서드 | 설명 |
|---|---|
| `apply(oRoot)` | 글꼴·표 스타일 적용 (메인 창 생성 직후 한 번) |
| `getColor(strColorName)` | 테마 색 값 (`success`, `bg`, `fg`, `border`, `inputbg` …) |
| `getStatusColorName(strStatus)` | 작업 상태 → 색 이름 |
| `getResultColorName(strResult)` / `getResultText(strResult)` | 동작 결과 → 색 이름 / `✔`·`✖`를 붙인 표시 문자열 |
| `configureColorTags(oTree)` | 표에 색 이름과 같은 태그(`success` 등) 등록 → 행에 `tags=(색이름,)`으로 색 지정 |
| `createButton(oParent, strText, strBootstyle, fnCommand)` | 작은 버튼 생성 |

## 참고

창은 DPI 인식을 끈 상태(`high_dpi=False`)로 만든다. Windows 배율(예: 125%)에 맞춰 창 전체가 확대되므로, 창 크기 상수(640×480 등)는 100% 기준 크기다.

소스: [src/main/ui/UiTheme.py](../../../src/main/ui/UiTheme.py)
