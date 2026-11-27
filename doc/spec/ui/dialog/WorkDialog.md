# WorkDialog

**메인 UI**

프로그램의 루트 창(`ttkbootstrap.Window`, 테마는 [UiTheme](../UiTheme.md)). 제목 "K-TOPIA Launcher", 640×480 고정(Windows 배율만큼 확대되어 보임), 최소화·닫기만 동작(최대화 비활성). 닫기를 누르면 숨기기만 한다(트레이에서 다시 열기). 창 아이콘은 IconFactory의 파란 K.

- 위: 테스트 명(CHORD_NM), 테스트 내용(CHORD_SBST, 3줄) — 굵은 라벨 + 내용
- 가운데 표(남색 머리글): 표시 중인 작업의 TEST_TASK_DTL — No(1~N), 테스트명(ACT_SBST), 결과(ACT_RESULT)
  - 결과가 성공이면 행 전체 초록 + `✔`, 실패면 빨강 + `✖` (판단 기준은 UiTheme)
- 아래: 상태 점(●, 작업 상태 색) + 상태 메시지, 버튼 [예약목록](회색 테두리) [작업목록](남색) [오류](빨간 테두리)
- 자식 Dialog는 한 번에 하나, 모달

**init 순서** (`init()`)
1. 런처 버전 체크 — 현재 버전은 `.launcher` 파일(`LauncherConfig.readLauncherVersion`), 최신 버전은 `SystemApiClient.fetchLatestVersion` (현재 임시: 항상 같은 버전). `.launcher`가 없으면 "버전 파일(.launcher) 없음"
2. `DatabaseUtil.initMappingQuery()` — selectQueryMap(type=S), executeQueryMap(I/U/D), systemQueryMap(initSql) 로딩
3. Node.js 설치 체크 — `NODEJS_PATH\node.exe`
4. Playwright 설치 체크 — `PLAYWRIGHT_PATH\node_modules\@playwright\test`
5. 지금 구동되어야 할 작업 체크 — `ManageTestTaskList.checkReadyTasks()` (DB의 RDY 작업)
6. 예약된 작업 체크 — `ManageTestTaskList.checkReservedTasks()` (DB의 RDY·WAIT 예약 작업)

## 메서드

| 메서드 | 설명 |
|---|---|
| `init()` | 런처 시작 시 한 번 (아래 init 순서). 결과는 로그(`init 1`~`init 6`)와 상태 표시에 남김 — 문제 없으면 "초기화 완료", 있으면 "초기화 완료 (Node.js 없음, …)" 주황 점 |
| `showWindow() / hideWindow()` | 보이기(열린 자식이 있으면 그 창을 앞으로) / 숨기기 |
| `setStatusMessage(strMessage, strStatus=None)` | 상태 메시지 표시. strStatus(작업 상태 코드)에 따라 점 색이 바뀜 (없으면 회색) |
| `displayTask(oTask) / refreshDisplayedTask()` | 작업 표시 / 다시 읽기 |
| `refreshActiveDialog()` | 열린 자식 Dialog 갱신 |
| `openReservationList() / openTaskList() / openErrorDialog() / openConfigDialog()` | 창을 보이게 한 뒤 자식 Dialog 열기 (이미 열려 있으면 그 창을 앞으로) |
| `openLoginGuide() / closeLoginGuide()` | [로그인 안내](LoginGuideDialog.md) 창 열기(다른 자식 Dialog가 열려 있으면 그 위에) / 닫기 |
| `report_callback_exception(...)` | UI 이벤트 예외 경계: 로그 + 오류 메시지 창 |

소스: [src/main/ui/dialog/WorkDialog.py](../../../../src/main/ui/dialog/WorkDialog.py)
