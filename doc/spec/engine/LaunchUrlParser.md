# LaunchUrlParser

**ktopia:// 주소 해석**

웹에서 부른 `ktopia://start?...` 문장 전체를 **주소**라고 한다. 주소를 받아 작업 객체(TestTaskDTO, 상태 RDY)를 만든다.

## 주소 저장 — 웹이 보낸 원래 모양

- TASK_ADR에는 **주소 전체**를 저장한다.
- Windows는 런처에 넘길 때 `ktopia://start?...`를 `ktopia://start/?...`로 바꿔 넘긴다(서버 이름 자리 뒤에 `/`를 넣는 표준화). 저장할 때 이 `/`만 빼서 웹이 보낸 모양으로 되돌린다(`restoreOriginalUrl`).
- 값의 인코딩(`%3A%2F%2F` 등)은 그대로 저장한다. 쓸 때 `parseParams`로 나눈 뒤 디코딩한다.

## 파라미터 파싱 규칙 (`parseParams`)

1. 주소에서 **첫 `?` 다음**부터 사용한다. `?`가 없으면 파라미터 없음.
2. 첫 번째 구분자 **`&`**로 나눈다. 빈 조각은 건너뛴다.
3. 두 번째 구분자 **`=`**로 이름과 값을 나눈다 — **첫 `=`에서만** 나누므로 값 안의 `=`는 그대로 남는다. `=`가 없으면 값은 빈 문자열.
4. 값만 퍼센트 디코딩한다(`urllib.parse.unquote`, `+`는 공백으로 바꾸지 않는다). 앞뒤 공백은 제거.
5. 이름은 대소문자를 가리지 않는다(대문자로 저장, `getParam`으로 꺼냄). 같은 이름이 여러 번 오면 처음 것만 쓴다.

예) `ktopia://start?domain=http%3A%2F%2Flocalhost%3A8082&systemId=UI_SYSTEM_1&mode=CRAWLING`
→ `DOMAIN = http://localhost:8082`, `SYSTEMID = UI_SYSTEM_1`, `MODE = CRAWLING`

## 작업 타입 결정 (위에서부터 먼저 맞는 것)

| 조건 | TASK_TYPE | 추가 저장 |
|---|---|---|
| `mode=CRAWLING` | CRAWLING | |
| reqProdSeq, exeSeq, chordId 모두 있음 | STANDARD, DTL_TYPE=PLAYWRIGHT | REQ_PROD_SEQ, EXE_CD, CHORD_ID |
| chordToken 있음 | VALIDATION | CHORD_ID=chordToken |
| 그 외 | 오류 (ValueError) | |

공통: TASK_ID=`Util.makeTaskId()`, TASK_ADR=주소 전체(원래 모양), TEST_STATUS=RDY, CHORD_TYPE=chordType, SYS_TRTR_ID=인증 아이디, SYS_RECD_CRET_DT=현재 시각. `domain`은 필수.

## 메서드

| 메서드 | 설명 |
|---|---|
| `isLaunchUrl(strValue)` | `ktopia:`로 시작하는지 |
| `parse(strUrl, strTrtrId)` | 작업 객체 반환 |
| `restoreOriginalUrl(strUrl)` | Windows가 넣은 `start/?`의 `/`를 빼서 원래 모양으로 |
| `parseParams(strUrl)` | 위 파싱 규칙대로 {대문자 이름: 디코딩된 값} — 실행기가 TASK_ADR을 다시 읽을 때도 사용 |
| `getParam(mapParams, strName)` | 이름(대소문자 무시)으로 값, 없으면 "" |

## 참고

ValueError: ktopia 주소가 아님 / start가 아님 / domain 없음 / 작업 타입을 알 수 없음.
`systemId` 등 위 표에 없는 파라미터는 TASK_ADR 안에만 남는다 (필요할 때 `parseParams`로 꺼낸다).

소스: [src/main/engine/LaunchUrlParser.py](../../../src/main/engine/LaunchUrlParser.py)
