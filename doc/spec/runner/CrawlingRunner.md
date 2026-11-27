# CrawlingRunner

**크롤링 실행 (CRAWLING · VALIDATION)**

크롤링은 `lib/`의 whl로 설치한 **`crawling` 패키지의 `CrawlerEngine`**(login · crawl · cancel)을 그대로 쓴다. 런처는 엔진을 만들지 않고, 서버 정보 받기 → 로그인 → 크롤링 → 결과 처리 순서만 관리한다.

작업마다 새 객체를 만들고 `initMembers()`로 멤버변수(서버 정보 map, 엔진, 종료 신호)를 초기화한다 — 업무가 바뀌면 이전 정보가 남지 않는다.

## 실행 순서 (`execute()`)

| 단계 | 내용 |
|---|---|
| 1 | TEST_STATUS = **WRK** — `ManageTestTaskList.startTask()`가 실행 전에 저장 |
| 2 | `SystemApiClient.getServerData(domain, systemId, TASK_TYPE)` — domain은 TASK_ADR의 `domain`, systemId는 CHORD_ID |
| 3 | 응답 JSON을 멤버변수 map(`m_mapServerData`)에 저장, 작업 객체에 CHORD_NM = `systemNm`, CHORD_SBST = `systemUrl` |
| 4 | `loginYn`에 따라 로그인 여부 결정. 엔진 설정은 런처 폴더의 `crawler.properties` |
| 4-1 | `loginYn` ≠ Y: 로그인 없이 TEST_COMM_LIST에 시스템 정보 저장 (META_VALUE `loginYn:N,expMin:0`, VALUE_DESC 없음) |
| 4-2 | `loginYn` = Y: `CrawlerEngine.login()` 실행 + 런처에 [로그인 안내](../ui/dialog/LoginGuideDialog.md) 창. [확인]을 누르면 로그인 완료 신호. 세션(json) 저장(`LoginResult.SAVED`)되면 시스템 정보 저장 (META_VALUE `loginYn:Y,expMin:20`, VALUE_DESC `sessionSaveDt:YYYY-MM-DD HH:MM:SS`) |
| 5 | `CrawlerEngine.crawl(systemUrl, 로그인 여부, system_name=systemId)` |
| 6 | 결과 보내기 — **현재는 "보내기 : domain (결과 폴더)"를 콘솔·로그에 찍기만** (서버 API 미구현: `sendCrawlingRslt`, `uploadMultiFiles` 예정) |
| 7 | TEST_RESULT = **Y**, TEST_STATUS = **CMP** |
| 8 | `startTask()` — 성공·실패와 상관없이 `ManageTestTaskList._finishTask`가 다음 업무로 넘어간다 |

**시스템 정보 저장 (TEST_COMM_LIST)** — META_KEY = systemId, UPR_DIV_KEY = `PL_UI_SYSTEM_INFO`, DIS_NM = systemNm, ALIAS_NM = systemUrl. 같은 키(UPR_DIV_KEY + META_KEY)가 있으면 수정(`updateTestComm`, 수정일 기록), 없으면 등록(`insertTestComm`, 등록일 기록).

**서버 응답(JSON 객체) 키** — 서버 API가 아직 없어 런처에서 먼저 정한 이름: `systemNm`(시스템 이름), `systemUrl`(시스템 URL, 필수), `loginYn`(Y/N). 그 외 키도 map에 그대로 담는다.

## 결과

| 경우 | TEST_RESULT | TEST_STATUS | ERR_MSG |
|---|---|---|---|
| 끝까지 성공 | Y | CMP | — |
| **서버 API 통신 실패** (연결 안 됨, HTTP 오류, JSON 아님) · 응답에 `systemUrl` 없음 · 그 밖의 예외 | N | **ERR** | 예외 메시지 (`ManageTestTaskList._runTask` 경계에서 처리) |
| 로그인 실패 (SAVED가 아님) | N | FAIL | `로그인 실패 : <LoginResult> <엔진 오류>` |
| 크롤링 실패 (COMPLETED · MAX_STATES가 아님) | N | FAIL | `크롤링 실패 : <Status> <메시지>` |
| 중지 (작업 중지 · 런처 종료) | — | STOP | — |

## 메서드

| 메서드 | 설명 |
|---|---|
| `run(oTask, oConfig, oStopEvent, oTaskManager) [static]` | 객체를 만들어 `execute()` |
| `initMembers()` | 멤버변수 초기화 |
| `execute()` | 위 순서 실행. 끝나면 중지 감시 스레드를 끝낸다 |

## 참고

- **경로:** `crawler.properties`의 `authDir`(세션 json) · `outputDir`(결과)가 상대 경로면 런처 폴더 기준으로 바꾼다 (웹에서 실행돼 작업 폴더가 달라도 같은 곳). 파일은 `authDir/{systemId}.json`, 결과는 `outputDir/{systemId}/`
- **중지:** 감시 스레드(`CrawlingCancelWatcher`)가 0.5초마다 중지 신호를 보고 `CrawlerEngine.cancel()`을 부른다
- 크롤링 엔진은 프로세스 전체에서 한 번에 하나만 돈다 (런처도 작업을 하나씩만 실행)

소스: [src/main/runner/CrawlingRunner.py](../../../src/main/runner/CrawlingRunner.py)
