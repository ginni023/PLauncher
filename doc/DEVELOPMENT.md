# KTOPIA 런처 개발 문서

> 설계 내용(동작 원리·화면·흐름)은 [설계서](KTOPIA_설계서.md), 코드 작성 규칙은 [CodeConvention_python.md](CodeConvention_python.md), 클래스별 상세는 [spec/](spec/)를 본다. 이 문서는 **현재 상태와 개발 이력**을 기록한다.

## 개발 의의
이 런처는 **UI TEST**와 **DB 테스트**를 수행하기 위한 프로그램이다.

- **수행 작업:** 크롤링(crawling)과 UI TEST를 모두 런처에서 진행한다.
- **실행 방식:** 웹에서 `ktopia://` 주소를 호출하면 런처가 실행되고, 해당 동작을 자동으로 수행한다.
- **UI TEST 방식:** Playwright를 사용한다. 웹에서 Playwright **TypeScript** 소스를 받아서 실행한다.

## 개요
- **이름:** K-TOPIA Launcher (실행 파일: `KTOPIA.exe`)
- **형태:** GUI 데스크톱 프로그램 (Windows), 트레이 상주
- **언어/도구:** Python 3.12.10, tkinter 8.6, ttkbootstrap 2.2.7(화면 테마 flatly), PyInstaller 6.22.3, pystray(트레이), Pillow(아이콘)
- **DB:** SQLite (Python 내장 `sqlite3`, SQLite 3.49.1) — `resource\db\ktopia.db`
  - exe 실행 시: `KTOPIA.exe`가 있는 폴더 기준 (예: `dist\resource\db\ktopia.db`)
  - 시작 시 폴더·파일·테이블이 없으면 자동 생성, 연결마다 외래키 활성화
- **설정 파일:** `config.properties` (실행 파일과 같은 폴더)
- **로그:** `log\ktopia.log` (실행 파일과 같은 폴더, 5MB × 5개 순환)
- **현재 버전:** 0.1.0

## 폴더 구조
```
PLauncher/                         # 프로젝트 폴더 (D:\PLauncher, 가칭 — 이름 확정 시 다시 변경)
├─ main.py                         # 시작점: src/main을 import 경로에 넣고 KtopiaLauncher 실행
├─ build.bat                       # exe 빌드 스크립트 (+ XML을 dist로 복사)
├─ src/main/                       # 소스 (import 기준 경로)
│  ├─ KtopiaLauncher.py            # 전체 조립: 중복 실행 방지, 설정, DB, 작업관리, 트레이, 메인 UI
│  ├─ engine/                      # 런처 기반 — 웹 실행 주소, 설정, 시스템 서버 연동
│  │  ├─ LaunchUrlParser.py        #   ktopia:// 주소 → 작업 객체
│  │  ├─ ProtocolRegistry.py       #   레지스트리에 ktopia:// 등록/해제
│  │  ├─ SingleInstanceServer.py   #   중복 실행 방지, 두 번째 실행의 주소를 기존 런처로 전달
│  │  ├─ LauncherConfig.py         #   config.properties 관리, 런처 버전
│  │  ├─ LauncherEnvironment.py    #   Node.js·Playwright 설치 확인
│  │  └─ SystemApiClient.py        #   시스템 도메인 API (버전, 예약 조회, 인증) — 현재 임시 구현
│  ├─ task/                        # 작업 관리
│  │  ├─ ManageTestTaskList.py     #   기본/예약 QUEUE, INTERRUPT FLAG, startTask()
│  │  ├─ ReservationScheduler.py   #   예약 시간 확인, 예약 API 주기 조회
│  │  ├─ TaskRunner.py             #   작업 타입별 실행기 선택
│  │  └─ code/                     #   코드값: TaskStatus, TaskType, DtlType
│  ├─ runner/                      # 실행기
│  │  ├─ UiTestRunner.py           #   UI TEST(Playwright) — 현재 임시 구현
│  │  └─ CrawlingRunner.py         #   크롤링 — 현재 임시 구현
│  ├─ ui/                          # 화면
│  │  ├─ dialog/                   #   창: WorkDialog(메인), ChildDialog(모달 공통), TaskHistoryDialog(목록 공통),
│  │  │                            #       TaskListDialog, ReservationListDialog, ErrorDialog, ConfigDialog
│  │  ├─ TrayIcon.py               #   트레이
│  │  ├─ IconFactory.py            #   창·트레이 아이콘
│  │  ├─ UiAction.py               #   UI 요청 종류
│  │  └─ UiTheme.py                #   테마·글꼴·상태 색 규칙
│  ├─ dto/                         # 객체: TestTaskDTO, TestInfoDTO
│  ├─ database/                    # DB: DatabaseUtil, TestTaskDAO, TestInfoDAO
│  ├─ util/                        # 공통: Util(makeTaskId), PathUtil, StringUtil, DateUtil, LogUtil, PropertiesUtil
│  └─ secure/                      # 보안 (비어 있음 — 인증·암호화가 생기면 사용)
├─ lib/                           # 설치용 Python 패키지 원본(whl) — 실행 중에 읽지 않음, 배포 폴더에 넣지 않음
│  ├─ crawling-0.1.0-py3-none-any.whl          # 크롤러 (D:\pefer\crawling-py 에서 빌드)
│  └─ playwright-1.63.0…, greenlet-3.5.6-cp312…, pyee-13.0.1…, typing_extensions-4.16.0…
├─ resource/db/
│  ├─ ktopia.db                    # SQLite DB (소스 실행 시)
│  ├─ initSql.xml                  # 구조 변경 SQL
│  └─ mainSql.xml                  # 데이터 변경·조회 SQL
├─ doc/
│  ├─ DEVELOPMENT.md               # 이 문서
│  ├─ KTOPIA_설계서.md              # 설계서
│  ├─ CodeConvention_python.md     # 코드 규칙 (Python 적용판)
│  └─ spec/<폴더>/<클래스명>.md     # 클래스별 명세서 (소스와 같은 폴더 구조)
└─ dist/                           # 빌드 결과 (KTOPIA.exe, resource/db, config.properties, log)
```

**폴더 기준**
- 각 폴더에는 빈 `__init__.py`가 있다 (Python 패키지).
- `engine`: 런처가 돌아가기 위한 기반(실행 방법·설정·시스템 서버 연동). **작업을 실제로 실행하는 코드는 `task`·`runner`에 둔다.**
- 파일이 한두 개뿐인 폴더는 만들지 않는다. 파일이 늘어나면 그때 나눈다 (예: API가 늘면 `engine`에서 `api`로, 트레이 파일이 늘면 `ui`에서 `tray`로).
- 외부 라이브러리와 같은 이름의 폴더를 만들지 않는다 (예: `playwright`는 Python용 Playwright 패키지를 가리므로 `runner`로 지었다).

## 실행 / 빌드 방법
- 소스로 실행: `python main.py` (또는 `python main.py "ktopia://start?..."`)
- exe 빌드: `build.bat` 실행 → `dist\KTOPIA.exe` 생성
  - 옵션: `--onefile --noconsole --name KTOPIA --paths src\main --hidden-import pystray._win32`
  - `resource\db\initSql.xml`, `mainSql.xml`을 `dist\resource\db\`로 복사
  - XML만 고친 경우: 재빌드 없이 `dist\resource\db\`의 XML만 바꿔도 됨
- 필요한 패키지: `pip install pyinstaller pystray pillow ttkbootstrap`
- 크롤러 패키지 (인터넷 없이 `lib\`에서 설치):
  `pip install --no-index --find-links lib lib\crawling-0.1.0-py3-none-any.whl`
  - `greenlet`은 Python 3.12 전용(cp312) whl이다. Python 버전을 바꾸면 그 버전용 whl을 다시 받아야 한다

## SQL 작성 규칙
SQL은 Python 코드에 직접 쓰지 않고 XML 파일에 작성한다. 두 파일 모두 `resource\db`에 둔다.

| 파일 | 넣는 SQL | 사용 방식 |
|---|---|---|
| `initSql.xml` | CREATE, DROP, ALTER, 인덱스 생성/삭제 등 **테이블·인덱스 구조 변경** | 런처 시작 시 `DatabaseUtil.initDb()`가 자동 실행 |
| `mainSql.xml` | INSERT, UPDATE, DELETE, SELECT 등 **데이터 변경·조회** | `DatabaseUtil.executeUpdate(id, 파라미터)`, `DatabaseUtil.selectRows(id, 파라미터)` |

**XML 형식**
```xml
<sqls>
  <sql id="아이디" version="1"><![CDATA[
    SQL문
  ]]></sql>
</sqls>
```

**initSql.xml 규칙**
- `version`: DB에 기록된 버전(`PRAGMA user_version`)보다 큰 항목만 실행되고, 실행 후 DB 버전이 최댓값으로 올라간다.
- 이미 적용된 항목은 수정하지 않는다. 구조를 바꿀 때는 새 `<sql>`을 **아래에 추가**하고 `version`을 하나 올린다.
- 현재 DB 버전: **1**

**mainSql.xml 규칙**
- `id`는 파일 안에서 중복되지 않게 한다. `version`은 쓰지 않는다.
- **`type` 필수**: `S`(SELECT) → selectQueryMap, `I`/`U`/`D`(INSERT/UPDATE/DELETE) → executeQueryMap. 런처 시작 init 2단계 `DatabaseUtil.initMappingQuery()`가 나눠 담는다. type이 없거나 다르면 시작 오류
  - 예) `<sql id="selectTaskList" type="S">`, `<sql id="insertTestTask" type="I">`
- initSql.xml의 SQL은 systemQueryMap에 담긴다
- 바인드 변수는 **콜론 하나 + 영문 소문자로 시작**, 컬럼명 모양을 따른다: `TASK_ID` → `:task_Id`, `SYS_RECD_CRET_DT` → `:sys_Recd_Cret_Dt`
- DTO의 `toParams()`가 이 이름으로 값을 만들어 준다.
- 현재 등록된 SQL

| id | type | 내용 |
|---|---|---|
| `insertTestTask` | I | 작업 등록 (TEST_TASK_LIST 전체 컬럼) |
| `updateTestTaskStatus` | U | 작업 상태·결과·에러메시지·작업일 변경 |
| `selectTaskList` | S | 예약이 아닌 작업 전체, 최근 등록순 |
| `selectReservationList` | S | 예약 작업 전체, 최근 등록순 |
| `selectReadyTaskList` | S | 예약이 아닌 RDY 작업, 등록 오래된 순 (init 5단계) |
| `selectPendingReservationList` | S | RDY·WAIT 예약 작업, 예약일시 순 (init 6단계) |
| `selectTestInfoList` | S | 작업의 동작 목록 (TASK_ID, DATA_SEQ·ACT_NO 순) |

## DB 스키마 (`ktopia.db`)
정의 위치: [resource/db/initSql.xml](../resource/db/initSql.xml)

### TEST_TASK_LIST — 작업 테이블 (객체: TestTaskDTO)
런처에서의 모든 작업이 저장된다.
- **PK:** TASK_ID
- **NOT NULL:** TASK_ID, TASK_TYPE, SYS_RECD_CRET_DT, TASK_ADR, TEST_STATUS
- **INDEX:** `TEST_TASK_LIST_1IDX` (TASK_TYPE, TASK_ADR), `TEST_TASK_LIST_2IDX` (TASK_ID) UNIQUE

| 컬럼 | 타입 | 멤버변수 | 설명 |
|---|---|---|---|
| TASK_ID | VARCHAR | m_strTaskId | 작업아이디 |
| TASK_TYPE | VARCHAR | m_strTaskType | 작업 타입: STANDARD 기본수행, VALIDATION 검사, RESERVATION 예약 |
| DTL_TYPE | VARCHAR | m_strDtlType | 작업 TOOL 작동 방식: RECORD (XPATH 의존), STANDARD 기본, PLAYWRIGHT |
| DEVICE | VARCHAR | m_strDevice | UI 테스트 장치 (기본값 `PC`) |
| SYS_RECD_CRET_DT | VARCHAR | m_strSysRecdCretDt | 작업등록일(시간) |
| TASK_ADR | VARCHAR | m_strTaskAdr | 주소 (실행 주소의 domain) |
| TEST_STATUS | VARCHAR | m_strTestStatus | 작업 상태: RDY, WAIT, WRK, CMP, FAIL, ERR, STOP |
| TEST_RESULT | VARCHAR | m_strTestResult | 작업 결과 |
| ERR_MSG | VARCHAR | m_strErrMsg | 에러메시지 |
| RUN_DATE | VARCHAR | m_strRunDate | 작업일(시간) |
| REQ_PROD_SEQ | VARCHAR | m_strReqProdSeq | 수행 SR |
| EXE_CD | VARCHAR | m_strExeCd | 수행 INST NUMBER (실행 주소의 exeSeq) |
| PREF_RANK | VARCHAR | m_strPrefRank | 수행 INST 순서 |
| CHORD_ID | VARCHAR | m_strChordId | CHORD ID (크롤링은 chordToken) |
| CHORD_NM | VARCHAR | m_strChordNm | CHORD 명 |
| CHORD_TYPE | VARCHAR | m_strChordType | CHORD 타입 |
| CHORD_SBST | VARCHAR | m_strChordSbst | CHORD 상세정보 |
| RESERVE_DATE | VARCHAR | m_strReserveDate | 예약일(시간) (구 START_DATE) |
| RESOURCE | VARCHAR | m_strResource | (설명 미정) |
| SYS_TRTR_ID | VARCHAR | m_strSysTrtrId | 수행인 (설정의 인증 아이디) |

### TEST_TASK_DTL — 작업 동작 테이블 (객체: TestInfoDTO)
작업에서 필요한 테스트 동작들이 저장된다. TEST_TASK_LIST의 자식 테이블.
- **FK:** TASK_ID → TEST_TASK_LIST(TASK_ID)
- **NOT NULL:** TASK_ID, DATA_SEQ, ACT_NO, ACT_TYPE, ACT_STATE
- **INDEX:** `TEST_TASK_DTL_1IDX` (TASK_ID, DATA_SEQ, ACT_NO) UNIQUE

| 컬럼 | 타입 | 멤버변수 | 설명 |
|---|---|---|---|
| TASK_ID | VARCHAR | m_strTaskId | 작업아이디 (FK) |
| DATA_SEQ | INTEGER | m_nDataSeq | 작업 SEQ, 같은 작업을 여러 번 반복할 때 사용 (기본값 0) |
| ACT_TYPE | VARCHAR | m_strActType | 동작 타입 |
| ACT_RESULT | VARCHAR | m_strActResult | 동작 결과 (메인 UI 표의 "결과") |
| ACT_STATE | VARCHAR | m_strActState | 동작 상태 |
| ELM_ID | VARCHAR | m_strElmId | HTML ELEMENT 아이디 |
| INPUT_VALUE | VARCHAR | m_strInputValue | INPUT 값 |
| DELAY_TIME | INTEGER | m_nDelayTime | 지연 시간(초) (기본값 2) |
| CAPTURE_IND | VARCHAR | m_strCaptureInd | 캡처 여부 |
| ACT_SBST | VARCHAR | m_strActSbst | 동작 상세설명 (메인 UI 표의 "테스트명") |
| ACT_NO | INTEGER | m_nActNo | 동작 순서 |
| ACT_RST_SBST | VARCHAR | m_strActRstSbst | 동작 결과 상세 |
| ELM_TAG | VARCHAR | m_strElmTag | HTML ELEMENT TAG |
| ELM_NM | VARCHAR | m_strElmNm | HTML ELEMENT NAME |
| ELM_TYPE | VARCHAR | m_strElmType | HTML ELEMENT TYPE / XPATH |
| ELM_SEQ | VARCHAR | m_strElmSeq | HTML ELEMENT SEQ |
| ELM_CLASS | VARCHAR | m_strElmClass | HTML ELEMENT CLASS |
| INNER_TEXT | VARCHAR | m_strInnerText | HTML ELEMENT INNERTEXT |
| ERROR_CLASS | VARCHAR | m_strErrorClass | 에러 CLASS |
| ERROR_MSG | VARCHAR | m_strErrorMsg | 에러 메시지 |
| PAGE_NO | VARCHAR | m_strPageNo | 화면 번호 |
| TARGET | VARCHAR | m_strTarget | 화면 아이디 (MAIN, ...) |

- STEP_SEQ는 정의서의 "삭제할 것 → ACT_NO로 통합"에 따라 만들지 않음

### TEST_COMM_LIST — 공통 테이블
런처에서 필요한 정보들이 저장된다. (대응 객체는 아직 없음)
- **INDEX:** `TEST_COMM_LIST_1IDX` (UPR_DIV_KEY, META_KEY) UNIQUE

| 컬럼 | 타입 | 설명 |
|---|---|---|
| META_KEY | VARCHAR | KEY 아이디 |
| UPR_DIV_KEY | VARCHAR | 구분키/용도 |
| SYS_RECD_CRET_DT | VARCHAR | 등록일 |
| SYS_RECD_CHG_DT | VARCHAR | 수정일 |
| DIS_NM | VARCHAR | 제목 |
| ALIAS_NM | VARCHAR | 추가 제목 |
| META_VALUE | VARCHAR | 값 |
| VALUE_DESC | VARCHAR | 상세 설명 |

## 명세 해석 / 임시 결정 사항
사용자 확인 전까지 아래 기본안으로 구현했다. 확정되면 이 표를 고친다.

| 항목 | 현재 구현 |
|---|---|
| 실행 주소 → 컬럼 | **확정:** TASK_ADR = 주소 전체(웹이 보낸 원래 모양, 인코딩 유지). reqProdSeq→REQ_PROD_SEQ, exeSeq→EXE_CD, chordId→CHORD_ID, chordType→CHORD_TYPE |
| 주소 파싱 | **확정:** 첫 `?` 다음부터, `&`로 나누고 각 조각을 첫 `=`로 나눔, 값만 디코딩 (`LaunchUrlParser.parseParams`) |
| Windows가 넣는 `start/?` | **확정:** 저장할 때 `/`를 빼서 `start?`로 되돌림 |
| `mode=CRAWLING` | **확정:** TASK_TYPE=CRAWLING, 크롤링 실행기 사용 |
| `systemId` 등 그 밖의 파라미터 | 컬럼에 따로 저장하지 않음 (TASK_ADR에서 `parseParams`로 꺼내 씀) |
| `chordToken` 저장 위치 | CHORD_ID |
| UITEST 작업의 DTL_TYPE | PLAYWRIGHT |
| TASK_ID 생성 규칙 | **확정:** `Util.makeTaskId()` = `yyyyMMddHHmmss` + 순번(런처 시작 시 1000부터 1씩 증가), 예: `202611261839261000` |
| 메인 UI 표의 "테스트명" / "결과" | TEST_TASK_DTL.ACT_SBST / ACT_RESULT |
| 예약 작업 상태 흐름 | 등록 RDY → 예약 시간 도달 시 WAIT + 예약 QUEUE에 추가 → WRK → 종료 상태 |
| 예약 작업 실행기 | UI TEST 실행기 사용 |
| 메인 UI에 표시할 작업 | WRK 작업. 작업이 끝나도 다음 작업이 시작될 때까지 마지막 작업을 계속 보여줌 |
| 오류 Dialog 대상 | 메인 UI에 표시 중인 작업 (ERR_MSG + 동작별 ERROR_MSG) |
| 웹 실행 주소 등록 시점 | 런처 시작 시 LINK_REGST_IND=Y이면 등록, N이면 해제 (현재 사용자 레지스트리, 관리자 권한 불필요) |
| 중복 실행 | 두 번째 실행은 `127.0.0.1:47321`로 기존 런처에 주소를 넘기고 종료 |
| 설치 경로 계열(INSTALL/NODEJS/PLAYWRIGHT/SAVE_PATH) | 시작할 때마다 현재 폴더 기준으로 다시 계산해 저장 |
| Node.js | **확정:** 런처 폴더에 Node.js를 따로 넣어 배포한다 (`설치폴더\node`, NODEJS_PATH). PC에 설치된 Node.js는 쓰지 않는다 |

## 개발 이력

### 2026-11-06 — v0.1.0 기본 골격
- Python 3.12.10 설치 (winget, 사용자 범위)
- `main.py` 작성: 기능 없는 GUI 골격 (헤더 / 사이드바 / 콘텐츠 / 상태바)
- `build.bat` 작성, PyInstaller로 `dist\KTOPIA.exe` 빌드 (약 11MB)
- 실행 확인: "KTOPIA Launcher" 창이 정상적으로 열림
- `doc/DEVELOPMENT.md` 개발 문서 생성
- DB로 SQLite 사용 결정: Python 내장 `sqlite3` 모듈 동작 확인 (추가 설치 없음)
- DB 파일명 `ktopia.db`로 결정, `db.py` 추가 (연결 함수 `connect()`, 초기화 `init_db()`)
- `main.py` 시작 시 `db.init_db()` 호출 → exe 옆에 `ktopia.db` 자동 생성
- exe 재빌드 및 실행 확인: `dist\ktopia.db` 생성됨 (KTOPIA.exe 약 12MB)
- DB 위치를 `resource\db\ktopia.db`로 변경 (`db.py`의 `DB_DIR`, 폴더 자동 생성)
  - `resource\db` 폴더 생성, 기존 `dist\ktopia.db`(빈 파일) 삭제
  - exe 재빌드 및 실행 확인: `dist\resource\db\ktopia.db` 생성됨
- 테이블 3개 생성: TEST_TASK_LIST, TEST_TASK_DTL, TEST_COMM_LIST (+ 인덱스 4개)
  - 외래키 활성화 (`PRAGMA foreign_keys = ON`)
  - TEST_TASK_DTL의 STEP_SEQ는 정의서 지시대로 제외 (ACT_NO로 통합)
  - 검증: 부모 없는 TEST_TASK_DTL 입력이 외래키 오류로 거부됨, 기본값 DEVICE=PC / DATA_SEQ=0 / DELAY_TIME=2 확인
  - exe 재빌드 및 실행 확인: `dist\resource\db\ktopia.db`에 테이블 3개 생성됨
- SQL을 XML로 분리
  - `resource\db\initSql.xml` 생성: 테이블 3개 + 인덱스 4개 생성 SQL을 `db.py`에서 옮김 (version 1)
  - `resource\db\mainSql.xml` 생성: 데이터 변경 SQL용
  - `build.bat` 수정: 빌드 후 XML 두 개를 `dist\resource\db\`로 복사
  - 빈 DB 두 개(소스용, exe용)를 지우고 XML로 다시 생성해 확인: 테이블 3개, 인덱스 4개, 외래키, DB 버전 1
- 개발 의의 정리 (UI TEST·DB 테스트·크롤링, 웹 주소로 실행, Playwright TypeScript)

### 2026-11-06 — 기본 명세 구현 (객체·실행 방법·작업 원리·UI·설정)
- **코드 규칙 적용:** `D:\pefer\bchord_202608\doc\CodeConvention_java.md`를 Python에 맞춰 적용 → [CodeConvention_python.md](CodeConvention_python.md)
  - camelCase 메서드, 헝가리언 접두사(`str`, `n`, `lst`, `map`, `o` …), 멤버 `m_`, 클래스 변수 `s_`, 탭 들여쓰기
  - 클래스당 파일 1개(파일명 = 클래스명), 람다·메서드 체이닝 금지, 소스 주석 없이 `doc/spec/<클래스명>.md`에 명세
  - 예외는 경계(작업 1건 실행, UI 이벤트, 스레드 루프, 시작점)에서 받아 처리
  - 기존 `db.py` → `DatabaseUtil.py`, 기존 화면 골격(`main.py`의 Launcher) → `WorkDialog.py` 등으로 재작성
- **객체:** `TestTaskDTO`, `TestInfoDTO` — 컬럼별 멤버변수(`m_strTaskId`, `m_nActNo`)와 get/set 함수
- **DB 접근:** `TestTaskDAO`, `TestInfoDAO`, mainSql.xml에 SQL 5개 추가 (바인드 변수 `:task_Id` 형식)
- **실행 방법:** `ktopia://start?...` 레지스트리 등록(`ProtocolRegistry`), 주소 해석(`LaunchUrlParser`), 중복 실행 시 기존 런처로 전달(`SingleInstanceServer`)
  - reqProdSeq·exeSeq·chordId → STANDARD(UI TEST), chordToken → VALIDATION(크롤링)
- **작업 원리:** `ManageTestTaskList` — 기본/예약 QUEUE 2개, INTERRUPT FLAG, `startTask()`, 한 번에 하나만 실행, 상태 RDY/WAIT/WRK/CMP/FAIL/ERR/STOP
  - `ReservationScheduler`: 10초마다 예약 시간 확인, RESERVATION_USE=Y이면 RESERVATION_CHECK_TIME(분)마다 예약 API 조회
- **UI:** `WorkDialog`(메인, 크기 고정, 최소화·닫기만, 닫아도 트레이에 남음), `TaskListDialog`, `ReservationListDialog`, `ErrorDialog`, `ConfigDialog`, `TrayIcon`(열기(O)/작업목록(T)/설정(C)/종료)
  - 자식 Dialog는 모달: 열려 있는 동안 부모 조작 불가
  - 작업 상태가 바뀌면 상태표시·메인 화면·열린 목록이 자동 갱신
- **설정:** `LauncherConfig` — `config.properties`, 없으면 기본값으로 생성하고 첫 실행 시 설정 창을 띄움
  - 적용 버튼은 변경이 있을 때만 활성화, 인증 아이디는 인증 후에만 적용 가능
- **임시 구현(내용 미정):** UI TEST(Playwright) 실행, 크롤링 실행, 예약 조회 API, 인증 API
  - 실행기는 3초 기다린 뒤 결과 "…미구현"으로 CMP 처리, 예약 API는 빈 목록, 인증은 아이디가 있으면 성공
- **검증:** 임시 폴더 복사본으로 기능 검사 22개 통과
  - 설정 기본값 생성·재로딩, 주소 해석(두 예시 주소 + 잘못된 주소 3종), TASK_ID 1000개 중복 없음
  - 실행 순서: 진행 중 작업 → 예약 QUEUE → 기본 QUEUE, INTERRUPT FLAG 설정·해제
  - 강제종료 → STOP, 실행 중 예외 → ERR + 에러메시지, 목록 조회 정렬, 외래키
  - 메인/작업목록/오류/설정 화면 캡처 확인
- **exe 빌드·실행 확인:** `build.bat`에 pystray 모듈 포함, `dist\KTOPIA.exe` 약 20MB
  - 첫 실행: `dist\config.properties` 기본값 생성, `HKCU\Software\Classes\ktopia` 등록 (`"D:\ktopiaLauncher\dist\KTOPIA.exe" "%1"`)
  - Windows에서 `ktopia://` 예시 주소 2개 호출 → 새 실행이 주소를 기존 런처로 넘기고 종료 → STANDARD/PLAYWRIGHT, VALIDATION 작업으로 등록·CMP 처리 확인
  - Windows가 주소를 `ktopia://start/?...` 형태로 넘기는 것 확인 (처리됨)
- **실행 주소 파라미터 확정:** UI TEST의 chord ID는 `chordId`만 받는다 (예시 주소의 `chord=`는 명세 오기로 확인, 별칭 처리 제거). `chord=`만 있으면 작업 타입을 알 수 없다는 안내가 나온다
- **소스 정리 시작:** `src/main` 아래 `ui`, `playwright`, `util`, `secure`, `dto`, `database` 폴더 생성 (아직 비어 있음, 소스 이동 전)
  - `src/main/ui` 아래 `dialog`(창), `tray`(트레이), `common`(dialog와 tray가 함께 쓰는 것만 — IconFactory, UiAction 예정) 생성
- **소스 정리 완료:** 루트의 소스 35개를 `src/main` 아래 폴더로 이동 (구조는 위 "폴더 구조")
  - 파일이 하나뿐인 폴더는 두지 않기로 함: `config`·`api` 대신 `engine`, `ui/tray`·`ui/common` 대신 `ui` 바로 아래 (빈 폴더 삭제)
  - 폴더마다 `__init__.py` 추가, import를 `from util.DateUtil import DateUtil` 형태로 변경 (74곳)
  - `main.py`는 루트에 두고 `src/main`을 import 경로에 추가
  - `PathUtil.getAppDir()`: 소스 실행 시 `src/main/util`에서 세 단계 위(프로젝트 루트)를 기준으로 계산 → `resource/db`, `config.properties`, `log` 위치는 그대로
  - `ProtocolRegistry`: 소스 실행 시 등록 명령이 루트의 `main.py`를 가리키도록 수정
  - `build.bat`: `--paths src\main` 추가
  - 명세서를 `doc/spec/<폴더>/<클래스명>.md`로 이동, 링크 수정
  - 검증: 기능 검사 22개 통과, exe 재빌드 후 `ktopia://` 주소 호출 → 작업 등록·CMP 확인, 로그 이름이 `playwright.UiTestRunner`처럼 폴더 포함으로 바뀜
- **`playwright` 폴더 → `runner`로 이름 변경:** Python용 Playwright 패키지(`pip install playwright`)와 이름이 겹쳐 import가 꼬일 수 있어서. `TaskRunner` import, 명세서 폴더(`doc/spec/runner`) 함께 변경
- **Node.js 배포 방식 확정:** 런처 폴더에 Node.js를 따로 넣어 배포 (PC에 설치된 Node.js v24.13.1은 쓰지 않음)

### 2026-11-09
- **작업목록 컬럼 변경:** 등록일시 대신 작업일(RUN_DATE)을 **"수행시간"**으로 표시 (`TaskListDialog._getColumnDefs`, `TaskHistoryDialog`에 `COLUMN_RUN_DATE` 추가). 정렬은 그대로 최근 등록순. 예약목록은 변경 없음
  - 처음엔 "수행완료시간"으로 했으나 RUN_DATE는 작업 **시작** 시각이라 "수행시간"으로 바꿈. RUN_DATE 저장 시점과 테이블 구조는 바꾸지 않기로 결정
  - 대기(RDY) 중인 작업은 수행시간이 비어 있다
  - 화면 캡처 확인, exe 재빌드 후 `ktopia://` 호출로 작업 등록·RUN_DATE 저장 확인
- **예약목록 컬럼 변경:** 등록일시 제거, 순서를 **No, 테스트명, 상태, 결과, 예약일시, 수행시간**으로 변경. No는 화면 순서 1~N (`TaskHistoryDialog.COLUMN_NO`, 가운데 정렬). 정렬은 그대로 최근 등록순
- **작업목록 컬럼 순서 변경:** **No, 테스트명, 작업타입, 상태, 결과, 수행시간** (No는 예약목록과 같은 방식)
- **중복 실행 시 메인 창 열기 확인 (코드 변경 없음):** 이미 실행 중일 때 `KTOPIA.exe`를 다시 실행하면 새 런처는 뜨지 않고 기존 런처의 메인 창(WorkDialog)이 열림
  - 확인: 메인 창이 닫기 버튼으로 숨겨진 상태 / 최소화 상태 / 다른 창 뒤에 있는 상태 모두 다시 보임, 프로세스는 늘지 않음 (onefile exe라 원래 2개)
  - 숨겨졌거나 다른 창 뒤에 있던 경우 Windows 정책상 맨 앞(포커스)까지는 오지 않을 수 있음 → 사용자 결정으로 맨 앞으로 올리는 처리는 넣지 않음

### 2026-11-25
- **화면 디자인 변경 (ttkbootstrap, 밝은 테마 flatly)**
  - 견본 비교: ① sv-ttk(테마만) ② ttkbootstrap(테마 + 꾸밈) → ② 밝은 테마 선택
  - 사용자 조정: 상단 남색 머리글 띠 제거, 테스트 명·내용은 원래 배치 유지, 창 크기 유지, 글자 10pt → 9pt, 버튼 작게(고정 폭 제거, 여백 (10,2))
  - `ui/UiTheme.py` 추가: 테마·글꼴·표 줄 높이·버튼·상태 색 규칙을 한곳에 모음
  - WorkDialog: `ttkbootstrap.Window`로 변경, 표 머리글 남색, 동작 결과 성공/실패 색과 `✔`/`✖`, 하단 상태 점(●) 색, 버튼 구분(작업목록 강조, 오류 빨간 테두리, 예약목록 회색 테두리)
  - `setStatusMessage(strMessage, strStatus)`: 작업 상태에 따라 점 색 변경 (KtopiaLauncher가 상태 전달, 잘못된 실행 주소는 빨강)
  - ChildDialog: `ttkbootstrap.Toplevel`로 변경 (메인의 K 아이콘 그대로 사용)
  - 작업목록·예약목록: 행 글자색 = 작업 상태 색, 상태 칸 `● 완료` 형식(`TaskStatus.getName` 추가), 일부 칸 가운데 정렬
  - 오류: 텍스트 영역 테두리·여백, 설정: Y/N 항목을 켜고 끄는 스위치로, 버튼 스타일 통일
  - DPI: 지금처럼 Windows 배율(이 PC 125%)로 창 전체를 확대 (`high_dpi=False`). 견본 캡처는 배율을 끈 상태로 찍어서 실제보다 작게 보였음
  - `build.bat`에 ttkbootstrap 설치 추가, exe 약 21MB
  - 검증: 코드 규칙 점검(람다·체이닝·주석·탭) 이상 없음, 기능 검사 22개 통과, 5개 창 캡처 확인, exe 실행 후 `ktopia://` 작업 등록·CMP 및 화면 확인
  - ⚠ 동작 결과(ACT_RESULT)의 성공/실패 판단은 결과값 형식이 정해지지 않아 `성공/SUCCESS/PASS/OK/Y/CMP`, `실패/FAIL/ERROR/ERR/N` 단어로 임시 판단

### 2026-11-26
- **크롤러 패키지(crawling) 설치** — 크롤링은 Java판 jar 대신 Python판 `crawling`(D:\pefer\crawling-py)을 쓰기로 함 (Java 설치 불필요, 콘솔 입력 없는 `CrawlerEngine` API)
  - `D:\pefer\crawling-py\dist`의 whl 5개를 프로젝트 `lib\`로 복사: crawling 0.1.0, playwright 1.63.0, greenlet 3.5.6(cp312), pyee 13.0.1, typing_extensions 4.16.0
  - `lib\`에서만 설치(`--no-index`, 인터넷 사용 안 함) → Python 3.12 환경에 설치됨
  - 확인: `src\main`을 import 경로에 넣은 상태에서 `crawling`, `playwright` 정상 import (런처 폴더와 이름 겹침 없음), Playwright 드라이버(node.exe) 포함, crawling 리소스(js, prompt) 포함
  - Java판 jar(`D:\pefer\crowling\target\lib`)는 복사하지 않음
  - **아직 하지 않은 것:** `CrawlingRunner` 연결, exe 빌드 옵션(crawling 리소스·Playwright 드라이버 포함), `requirements.txt`
- **리허설 문제 수정: `ktopia://start?...` 호출 시 작업이 add되지 않음**
  - 원인: 리허설 주소 `ktopia://start/?domain=…&systemId=UI_SYSTEM_261126141219738&mode=CRAWLING`의 `mode=CRAWLING`을 몰라 "작업 타입을 알 수 없습니다"로 거부 → insert 안 됨 (로그로 확인)
  - TaskType에 **CRAWLING** 추가 (`mode=CRAWLING` → CRAWLING, CrawlingRunner로 실행)
  - TASK_ADR에 **주소 전체** 저장 (이전: domain 값만). Windows가 `start?`를 `start/?`로 바꿔 넘기므로 저장 때 원래 모양으로 되돌림 (`restoreOriginalUrl`)
  - 주소 파싱을 직접 구현: 첫 `?` 다음 → `&` → 첫 `=` → 값 디코딩 (`parseParams`, 실행기에서도 쓰도록 공개)
- **`Util.makeTaskId()` 추가** (`util/Util.py`): `yyyyMMddHHmmss` + `digit_seq`(클래스 변수 `s_nDigitSeq`, 1000부터, 호출마다 +1). 기존 `TaskIdGenerator` 삭제, `DateUtil.getNowTimestamp()`로 변경
- **런처 시작 init 추가** (`WorkDialog.init()`, 메인 창 생성 직후 KtopiaLauncher가 호출)
  1. 런처 버전 체크 — `SystemApiClient.fetchLatestVersion` (임시: 항상 최신), 버전 상수 `LauncherConfig.LAUNCHER_VERSION = 0.1.0`
  2. `DatabaseUtil.initMappingQuery()` — mainSql `type` S → selectQueryMap, I/U/D → executeQueryMap, initSql → systemQueryMap. `selectRows`/`executeUpdate`는 각 맵에서만 찾음. 기존 `getSql` 삭제
  3. Node.js 설치 체크 — `NODEJS_PATH\node.exe` (`engine/LauncherEnvironment.py`)
  4. Playwright 설치 체크 — `PLAYWRIGHT_PATH\node_modules\@playwright\test\package.json`
  5. 구동할 작업 체크 — `checkReadyTasks()`: DB의 RDY 작업을 기본 QUEUE로 (런처 재시작 시 남은 작업 처리)
  6. 예약 작업 체크 — `checkReservedTasks()`: DB의 RDY·WAIT 예약 작업을 불러와 시간이 된 것은 실행
  - 결과는 로그 `init 1`~`init 6`과 상태 표시("초기화 완료 (Node.js 없음, Playwright 없음)")
- mainSql.xml: `selectTaskList`에 빠져 있던 `type="S"` 추가, `selectReadyTaskList`·`selectPendingReservationList` 추가
- 검증: 기능 검사 22개 통과 (쿼리 맵 분류, makeTaskId 형식·순번, 리허설 주소 → CRAWLING·RDY·insert·실행, 주소 복원, 파싱 규칙, 재시작 시 남은 RDY·예약 작업 처리·중복 없음), 코드 규칙 점검 이상 없음
  - exe: Windows로 리허설 주소와 UI TEST 주소 호출 → 두 작업 모두 insert·CMP, TASK_ADR이 `ktopia://start?…`(웹이 보낸 모양)로 저장, 로그에 init 1~6 확인
- **문서:** [KTOPIA_설계서.md](KTOPIA_설계서.md), [CodeConvention_python.md](CodeConvention_python.md), 클래스별 명세서 36개 [spec/](spec/)

### 2026-11-26 — 프로젝트 이름 가칭 변경
- **프로젝트 폴더 `D:\ktopiaLauncher` → `D:\PLauncher`** (PLauncher는 가칭. 이름이 확정되면 그때 전부 바꾼다)
  - 바꾼 범위: 프로젝트 폴더 이름, 문서 속 폴더 이름·경로 (폴더 구조 그림, 설계서 설정 화면 그림)
  - 그대로 둔 것: 실행 파일 `KTOPIA.exe`, 창·트레이 이름 "K-TOPIA Launcher", 웹 실행 주소 `ktopia://`, `ktopia.db`·`ktopia.log`, 클래스 이름 `KtopiaLauncher`, 개발 이력 속 당시 경로
  - 코드는 폴더 이름을 쓰지 않아 수정 없음. `config.properties` 경로와 `ktopia://` 레지스트리 등록은 새 위치에서 처음 실행할 때 자동으로 다시 잡힌다
  - 설계서 5.6 설정 화면 그림이 뒤섞여 있던 것(Playwright 경로·캡처 저장 경로 줄)을 원래 순서로 복구
- **GitHub 저장소 첫 커밋:** https://github.com/ginni023/PLauncher (`main` 브랜치, 첫 커밋 `b8c3c1a`)
  - `.gitignore`로 제외: `__pycache__`, `build/`·`dist/`·`*.spec`(빌드 결과), `log/`, `config.properties`(PC마다 다름), `resource/db/ktopia.db`(로컬 데이터 — 테이블은 initSql.xml로 다시 생성), 배포 때 넣는 `node/`·`playwright/`·`screenShot/`·`auth/`·`crawl-output/`
  - `lib/`의 whl(약 37MB, 대부분 Playwright)은 오프라인 설치용이라 저장소에 포함

## 다음 할 일
- [ ] UI TEST 실행 구현: 런처 폴더의 Node.js(`NODEJS_PATH`) + `@playwright/test`로 웹에서 받은 TypeScript 소스 실행, 결과를 TEST_TASK_DTL에 기록
- [ ] Node.js 배포 방식: 런처 폴더 `node\`에 넣을 Node.js 버전과 넣는 시점(설치 파일에 포함 / 첫 실행 때 시스템 도메인에서 내려받기) 결정
- [ ] 크롤링 실행 구현: `CrawlingRunner`에서 `crawling.CrawlerEngine` 사용 (설치 완료). 로그인 완료 처리 방식(화면 버튼 / 로그인 창 닫기), 결과·쿠키 저장 위치, exe 빌드 옵션 결정 필요
- [ ] 시스템 도메인 API 연동: 예약 조회, 인증 (주소·요청·응답 형식 필요)
- [ ] 설치 과정: Node.js·Playwright 자동 설치, 버전 확인·업데이트
- [ ] DB 관련 개발: 사용자가 다음 차수에 내용 전달 예정
- [ ] "명세 해석 / 임시 결정 사항" 표의 항목 확정
- [ ] TEST_TASK_LIST.RESOURCE 컬럼 설명 확정
- [ ] TEST_TASK_DTL 삭제 시 동작 확정 (부모 작업 삭제 시 자식 동작 함께 삭제 여부)
- [ ] 런처가 실행 중(WRK)에 비정상 종료되어 WRK로 남은 작업 처리 방법 결정 (RDY·WAIT는 init에서 다시 불러옴, WRK는 그대로 남음)
- [ ] 런처 버전 확인·업데이트 API 구현 (지금은 임시)
- [ ] Node.js·Playwright가 없을 때 처리 (지금은 상태 표시만, UI TEST는 아직 임시 실행기)
