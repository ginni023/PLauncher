# SystemApiClient

**서버 API**

웹이 보낸 `domain`(또는 설정의 RESERVATION_SYSTEM) 서버와 통신한다. 실패(연결 안 됨, HTTP 오류, JSON 아님)는 예외로 올린다 → 작업이면 `ManageTestTaskList._runTask`에서 결과 N, 상태 ERR.

## 메서드

| 메서드 | 설명 |
|---|---|
| `setAuthToken(strToken) [static]` | 요청에 쓸 토큰 (앞뒤 공백 제거). 런처 시작·설정 적용 때 설정의 API_TOKEN으로 호출 |
| `hasAuthToken()` | 토큰이 있는지 |
| `getServerData(strDomain, strSystemId, strType)` | 업무 정보 요청. `POST {domain}/api/launcher/getServerData`, 본문 `{"systemId": …, "type": …}` (type = TASK_TYPE, 서버가 타입별로 다른 정보를 보낼 수 있게). 응답 JSON 객체(dict)를 돌려준다 |
| `buildUrl(strDomain, strPath)` | domain 끝의 `/`를 떼고 경로를 붙인다. domain이 없으면 ValueError |
| `postJson(strUrl, mapRequest)` | JSON POST (UTF-8, 제한 시간 10초). 토큰이 있으면 `Authorization: Bearer <토큰>` 헤더 추가. 요청·응답을 로그에 남김 (토큰 값은 남기지 않고 있음/없음만) |
| `fetchLatestVersion(strDomain, strCurrentVersion)` | 최신 런처 버전 (init 1단계). **임시:** 받은 현재 버전을 그대로 돌려줌 |
| `fetchReservations(strDomain)` | 예약 작업 목록. **임시:** 빈 리스트 |
| `authenticate(strDomain, strToken)` | API 토큰 인증 결과 (설정 창 [인증]). **임시:** 토큰이 비어 있지 않으면 True. 로그에 토큰 값은 남기지 않음 |

## 참고

- 서버 API는 아직 서버에 없다. 경로 `/api/launcher/getServerData`와 요청·응답 키는 런처에서 먼저 정한 것 — 서버가 만들어지면 맞춘다
- 예정: `sendCrawlingRslt(strDomain, strRequest)`(결과 json), `uploadMultiFiles(arrFiles, strDomain, strUser, strSystemId)`(결과 파일) — [CrawlingRunner](../runner/CrawlingRunner.md) 6단계

소스: [src/main/engine/SystemApiClient.py](../../../src/main/engine/SystemApiClient.py)
