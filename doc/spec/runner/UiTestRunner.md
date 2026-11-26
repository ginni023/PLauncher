# UiTestRunner

**UI TEST(Playwright) 실행**

**현재 임시 구현.** 3초 기다린 뒤 CMP, 결과 "UI TEST(Playwright) 실행 기능 미구현".

## 메서드

| 메서드 | 설명 |
|---|---|
| `run(oTask, oConfig, oStopEvent)` | 중지 신호가 오면 상태를 바꾸지 않고 돌아간다 (관리자가 STOP 처리) |

## 참고

구현 예정: 웹에서 TypeScript 소스를 받아 NODEJS_PATH의 Node.js와 PLAYWRIGHT_PATH의 Playwright로 실행, MINIMIZE_IND=Y면 headless, 캡처는 SAVE_PATH, 동작별 결과는 TEST_TASK_DTL에 기록.

소스: [src/main/runner/UiTestRunner.py](../../../src/main/runner/UiTestRunner.py)
