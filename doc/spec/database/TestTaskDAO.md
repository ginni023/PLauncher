# TestTaskDAO

**TEST_TASK_LIST 접근**

mainSql.xml의 SQL로 작업을 등록·변경·조회한다.

## 메서드

| 메서드 | 설명 |
|---|---|
| `insertTestTask(oTask)` | `insertTestTask` — 전체 컬럼 등록 |
| `updateTestTaskStatus(oTask)` | `updateTestTaskStatus` — TEST_STATUS, TEST_RESULT, ERR_MSG, RUN_DATE 변경 |
| `selectTaskList()` | `selectTaskList` — 예약이 아닌 작업, 최근 등록순 → TestTaskDTO 리스트 |
| `selectReservationList()` | `selectReservationList` — 예약 작업, 최근 등록순 |
| `selectReadyTaskList()` | `selectReadyTaskList` — 예약이 아닌 RDY 작업, 등록 오래된 순 (init 5단계) |
| `selectPendingReservationList()` | `selectPendingReservationList` — RDY·WAIT 예약 작업, 예약일시 순 (init 6단계) |

## 참고

DB 오류는 그대로 올린다.

소스: [src/main/database/TestTaskDAO.py](../../../src/main/database/TestTaskDAO.py)
