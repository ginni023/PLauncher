# TaskRunner

**작업 타입별 실행기 선택**

## 메서드

| 메서드 | 설명 |
|---|---|
| `run(oTask, oConfig, oStopEvent, oTaskManager)` | CRAWLING, VALIDATION → CrawlingRunner, 그 외(STANDARD, RESERVATION) → UiTestRunner |

## 참고

실행기는 oTask에 TEST_STATUS(CMP/FAIL)와 TEST_RESULT를 직접 넣는다. oTaskManager는 실행 중 UI 요청(로그인 안내 창)에 쓴다. oStopEvent가 set되면 가능한 빨리 끝내야 한다.

소스: [src/main/task/TaskRunner.py](../../../src/main/task/TaskRunner.py)
