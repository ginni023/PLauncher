# KtopiaLauncher

**런처 전체 조립**

프로그램의 모든 구성요소를 만들고 연결한다. 백그라운드 스레드(작업 실행, 트레이, 중복 실행 서버)에서 오는 요청을 **UI 큐**에 담고, UI 스레드가 100ms마다 꺼내 처리한다. tkinter는 UI 스레드에서만 다뤄야 하기 때문이다.

**시작 순서** (`run`)
1. 로그 설정
2. 인자에서 `ktopia:` 주소 찾기
3. `SingleInstanceServer.start()` — 실패하면(이미 실행 중) 주소를 기존 런처에 넘기고 종료
4. 설정 로드 → API 토큰 적용(`SystemApiClient.setAuthToken`) → DB 초기화 → 레지스트리 등록/해제
5. `ManageTestTaskList`, `ReservationScheduler`, `WorkDialog` 생성 → **`WorkDialog.init()`** (버전·쿼리 매핑·Node·Playwright·남은 작업·예약 작업 확인) → `TrayIcon` 시작
6. 주소가 있으면 작업 등록 요청, 설정 파일을 새로 만들었으면 설정 창 열기 요청
7. UI 루프 시작

## 메서드

| 메서드 | 설명 |
|---|---|
| `run()` | 위 시작 순서 |
| `getConfig()` | LauncherConfig 반환 |
| `getTaskManager()` | ManageTestTaskList 반환 (WorkDialog.init에서 사용) |
| `postUiAction(strAction, oPayload)` | UI 큐에 요청 추가 (모든 스레드에서 호출 가능). strAction은 UiAction 상수 |
| `onRemoteMessage(strMessage)` | 다른 실행에서 받은 문자열. ktopia 주소면 작업 등록, 아니면 메인 창 열기 |
| `onTaskEvent(strEventType, oTask, strMessage)` | 작업 관리자 이벤트 → UI 큐 |
| `onConfigApplied()` | 설정 적용 후 API 토큰 다시 적용, 상태표시 갱신 |
| `exitApplication()` | 작업 중지(STOP 저장), 스케줄러·트레이·서버 정지, 창 닫기 |
| `_handleLaunchUrl(strUrl)` | 메인 창을 띄우고 주소를 해석해 작업 등록. 잘못된 주소는 상태표시에 안내 (경계) |
| `_handleTaskEvent(...)` | 상태표시 갱신, STARTED면 메인 화면에 작업 표시, LOGIN_REQUEST면 로그인 안내 창 열기, LOGIN_DONE이면 닫기, 열린 자식 Dialog 갱신 |

## 참고

`_pollUiQueue`는 처리 중 예외가 나도 `finally`에서 다음 폴링을 예약해 큐 처리가 멈추지 않게 한다.

소스: [src/main/KtopiaLauncher.py](../../src/main/KtopiaLauncher.py)
