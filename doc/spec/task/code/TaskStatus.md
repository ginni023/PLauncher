# TaskStatus

**작업 상태 코드**

| 코드 | 이름 | 종료 상태 |
|---|---|---|
| RDY | 대기중 | |
| WAIT | 작업준비중 (예약 전용) | |
| WRK | 작동중 | |
| CMP | 완료 | ✔ |
| FAIL | 실패 | ✔ |
| ERR | 오류 | ✔ |
| STOP | 강제종료 | ✔ |

## 메서드

| 메서드 | 설명 |
|---|---|
| `isFinished(strStatus)` | 종료 상태인지 |
| `getName(strStatus)` | 상태 이름만 ("완료") — 목록 화면 상태 칸에 사용 |
| `getLabel(strStatus)` | "완료(CMP)" 형식 표시 문자열 — 메인 상태 메시지에 사용 |

소스: [src/main/task/code/TaskStatus.py](../../../../src/main/task/code/TaskStatus.py)
