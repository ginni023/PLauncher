# TaskHistoryDialog

**작업목록·예약목록 공통**

작업 목록 표(남색 머리글)와 건수, 닫기 버튼. `refresh()`가 불릴 때마다 다시 읽고, 선택한 행은 유지한다.

- 행 전체 글자색 = 작업 상태 색 (완료 초록, 오류·실패 빨강, 강제종료 주황, 작동중 파랑, 대기 회색 — [UiTheme](../UiTheme.md))
- 상태 칸은 `● 완료`처럼 점 + 상태 이름(`TaskStatus.getName`)
- No, 작업타입, 상태, 예약일시, 수행시간 칸은 가운데 정렬

## 메서드

| 메서드 | 설명 |
|---|---|
| `_loadTasks()` | 하위 클래스가 구현 — 목록 조회 |
| `_getColumnDefs()` | (컬럼키, 제목, 폭) 목록. 기본: 등록일시, 작업타입, 테스트명, 상태, 결과 |

소스: [src/main/ui/dialog/TaskHistoryDialog.py](../../../../src/main/ui/dialog/TaskHistoryDialog.py)
