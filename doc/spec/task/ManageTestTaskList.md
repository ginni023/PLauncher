# ManageTestTaskList

**작업 관리**

작업 등록·순서·실행을 관리한다. 자세한 흐름은 [설계서 §4](../../KTOPIA_설계서.md#4-작동-원리-작업) 참고.

- **기본 QUEUE**: STANDARD, VALIDATION, CRAWLING 작업 (선입선출)
- **예약 QUEUE**: 예약 시간이 된 RESERVATION 작업
- **예약 대기 목록**: 시간이 아직 안 된 예약 작업
- **INTERRUPT FLAG**: 예약 작업이 QUEUE에 들어오면 True, 예약 QUEUE가 비면 False
- 한 번에 하나만 실행. 실행은 별도 스레드(`TaskWorker`)
- 모든 메서드는 RLock으로 보호

## 메서드

| 메서드 | 설명 |
|---|---|
| `getTaskName(oTask) [static]` | 표시용 이름: CHORD_NM → CHORD_ID → TASK_ID |
| `addTask(oTask)` | RDY로 DB 등록 → 예약이면 대기 목록, 아니면 기본 QUEUE → ADDED 이벤트 → startTask() |
| `checkReadyTasks()` | init 5단계. DB에 남아 있는 **RDY 작업**(예약 제외, 등록 오래된 순)을 기본 QUEUE에 넣고 startTask(). 이미 QUEUE·실행 중인 작업은 건너뜀. 불러온 수 반환 |
| `checkReservedTasks()` | init 6단계. DB의 **RDY·WAIT 예약 작업**을 불러옴: WAIT는 예약 QUEUE(FLAG=True), RDY는 예약 대기 목록 → checkReservations() → startTask(). 불러온 수 반환 |
| `checkReservations()` | 예약 시간이 지난 대기 작업을 WAIT로 바꿔 예약 QUEUE에 넣고 FLAG=True → startTask() |
| `startTask()` | 실행 중 작업이 있으면 False. 예약 QUEUE 앞 → (비면 FLAG=False) 기본 QUEUE 앞 순으로 골라 WRK 저장 후 실행. 시작하면 True |
| `stopTask()` | 실행 중 작업에 중지 신호 → STOP |
| `shutdown()` | 더 이상 시작하지 않음. 실행 중 작업은 STOP 저장 |
| `requestLogin(oTask)` | 실행기가 로그인 대기를 시작할 때. 완료 신호(threading.Event)를 만들어 돌려주고 LOGIN_REQUEST 이벤트 → 로그인 안내 창 |
| `confirmLogin()` | 로그인 안내 창 [확인] → 완료 신호 set |
| `finishLogin(oTask)` | 로그인이 끝나면(성공·실패·중지) 신호를 지우고 LOGIN_DONE 이벤트 → 안내 창이 열려 있으면 닫음 |
| `getCurrentTask() / isInterrupted()` | 현재 작업 / FLAG |
| `_runTask(...)` | 실행 경계. TaskRunner 예외(서버 API 통신 실패 등) → TEST_RESULT **N** + **ERR** + ERR_MSG. 중지 신호 → STOP. 실행기가 종료 상태를 안 정하면 CMP |
| `_finishTask(...)` | 결과 저장 → QUEUE에서 pop → FINISHED 이벤트 → startTask(), 시작할 게 없으면 IDLE 이벤트 |

## 참고

작업 추가(add) = 작업 객체를 만들어 DB의 TEST_TASK_LIST에 insert(mainSql `insertTestTask`)하는 것.

실행 중(WRK)에 런처가 비정상 종료되어 WRK로 남은 작업은 init에서 다시 불러오지 않는다.

이벤트(`EVENT_ADDED/RESERVED/STARTED/FINISHED/IDLE/LOGIN_REQUEST/LOGIN_DONE`)는 생성자에서 받은 `fnOnEvent(strEventType, oTask, strMessage)`로 알린다. 이 콜백은 작업 스레드에서 불리므로 UI를 직접 건드리면 안 된다.

소스: [src/main/task/ManageTestTaskList.py](../../../src/main/task/ManageTestTaskList.py)
