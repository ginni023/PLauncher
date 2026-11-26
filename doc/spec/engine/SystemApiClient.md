# SystemApiClient

**시스템 도메인(RESERVATION_SYSTEM) API**

**현재 임시 구현.** 주소·요청·응답 형식이 정해지면 구현한다.

## 메서드

| 메서드 | 설명 |
|---|---|
| `fetchLatestVersion(strDomain, strCurrentVersion)` | 최신 런처 버전 (init 1단계). 현재는 받은 현재 버전을 그대로 돌려줌 → 업데이트 없음 |
| `fetchReservations(strDomain)` | 예약 작업 목록 (현재 빈 리스트) |
| `authenticate(strDomain, strTrtrId)` | 인증 결과 (현재 아이디가 비어 있지 않으면 True) |

소스: [src/main/engine/SystemApiClient.py](../../../src/main/engine/SystemApiClient.py)
