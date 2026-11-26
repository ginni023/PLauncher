# Python Code Convention (KTOPIA 런처)

원본: `D:\pefer\bchord_202608\doc\CodeConvention_java.md` (bchord Java 규약)
이 문서는 원본을 **Python에 맞게 옮긴 적용판**이다. 원본과 같은 항목은 원본을 따르고, Python 문법 때문에 달라지는 부분만 아래에 적는다.

## 1. 파일 구성
- **파일 하나에 클래스 하나**, 파일명 = 클래스명 (`TestTaskDTO.py` → `class TestTaskDTO`)
- 소스는 `src/main/<폴더>/` 아래에 둔다 (Java의 패키지 경로에 해당). 폴더 이름은 모두 소문자, 폴더마다 빈 `__init__.py`
- 시작점 `main.py`만 예외 (프로젝트 루트, 클래스 없이 `main()` 함수, `src/main`을 import 경로에 추가)
- 인코딩 UTF-8, 줄바꿈 LF
- 임포트: `from 폴더.클래스명 import 클래스명` 형태로 한 줄에 하나 (기준은 `src/main`). 순서는 표준 라이브러리 → 외부 라이브러리 → 프로젝트 클래스
  - 예) `from util.DateUtil import DateUtil`, `from ui.dialog.WorkDialog import WorkDialog`

## 2. 명명 규칙
| 대상 | 규칙 | 예 |
|---|---|---|
| 클래스 | PascalCase | `ManageTestTaskList`, `WorkDialog` |
| 메서드 | camelCase, 동사로 시작 | `startTask()`, `getStrTaskId()` |
| 내부용 메서드 | 앞에 `_` + camelCase (Java의 private) | `_runTask()` |
| 상수 | 대문자 + `_` | `MAX_BYTES`, `EVENT_STARTED` |
| 인스턴스 변수 | `m_` + 헝가리언 | `m_oCurrentTask`, `m_lstPendingReservations` |
| 클래스(static) 변수 | `s_` + 헝가리언 | `s_mapMainSql`, `s_oLock` |
| 지역 변수·인자 | 헝가리언 | `strUrl`, `nIndex`, `oTask` |
| 루프 인덱스 | `nIndex` (다중이면 `nIndex1`, `nIndex2`) | |

> Python 라이브러리를 상속하면서 반드시 그 이름을 써야 하는 메서드(`__init__`, tkinter의 `report_callback_exception`)는 예외다.

### 헝가리언 접두사
| 접두사 | 타입 | 비고 |
|---|---|---|
| `str` | str | 원본 bchord 적용(§0.2)과 같이 `s` 대신 `str` |
| `n` | int | |
| `l` | 큰 정수(Java long 의미) | |
| `d` | float | Python float는 Java double과 같다 |
| `b` | bool | |
| `c` | 한 글자 str (Java char 의미) | |
| `by` | bytes | |
| `o` | 일반 객체 | 스레드, 락, 위젯, DTO 등 |
| `lst` | list | |
| `map` | dict | |
| `set` | set | |
| `arr` | tuple | 고정 길이 묶음 |
| `fn` | 호출 가능한 객체(함수·메서드) | **Python 추가** — 콜백 전달용 |

## 3. DTO
- 테이블 대응 객체는 이름 끝에 `DTO` (TEST_TASK_LIST → `TestTaskDTO`, TEST_TASK_DTL → `TestInfoDTO`)
- 멤버변수: `m_` + 타입 접두사 + 컬럼명 PascalCase
  - VARCHAR → `m_strTaskId`, INTEGER → `m_nActNo`
- 값은 필드에 직접 넣고 빼지 않고 **get/set 함수**로만 다룬다: `getStrTaskId()`, `setStrTaskId(strValue)`, `getNActNo()`
- `fromRow(oRow)`(DB 조회 결과 → 객체), `toParams()`(객체 → SQL 바인드 dict)를 둔다. 둘 다 내부에서 get/set 함수를 거친다.

## 4. SQL 바인드 변수 (원본 §0.8)
- 콜론 하나 + 영문 소문자로 시작, 컬럼명 모양 유지: `TASK_ID` → `:task_Id`, `SYS_RECD_CRET_DT` → `:sys_Recd_Cret_Dt`

## 5. 들여쓰기 (원본 §4)
- **탭**으로 들여쓴다. 스페이스와 섞지 않는다.
- 한 줄 120자 이내, 연산자 앞뒤·콤마 뒤 공백

## 6. 클래스 구조 (원본 §6)
1. 상수 → 2. 클래스 변수(`s_`) → 3. `__init__`(인스턴스 변수 `m_` 선언) → 4. `@staticmethod` → 5. 인스턴스 메서드 → 6. 내부용 메서드(`_`)

## 7. 주석 (원본 §0.3)
- **소스에 주석·docstring을 쓰지 않는다.**
- 클래스의 책임·동작·인자·반환값·예외는 `doc/spec/<폴더>/<클래스명>.md`에 쓴다 (소스와 같은 폴더 구조, 예: `doc/spec/util/DateUtil.md`).
- 소스를 고치면 대응하는 명세서도 함께 고친다.
- SQL XML(`initSql.xml`, `mainSql.xml`)의 주석은 소스가 아니라 SQL 데이터 설명이므로 둔다.

## 8. 예외 (원본 §0.4)
- 개별 메서드에서 잡지 않고 **위로 올린다.** Python에는 `throws` 선언이 없으므로 선언 규칙은 해당 없다.
- 받는 곳(경계)은 아래 다섯 곳이다. 여기서 로그를 남기고 상태를 정리한다.

| 경계 | 처리 |
|---|---|
| 작업 1건 실행 (`ManageTestTaskList._runTask`) | 작업을 ERR로 저장, ERR_MSG에 메시지 |
| UI 이벤트 (`WorkDialog.report_callback_exception`) | 로그 + 오류 메시지 창 |
| 백그라운드 스레드 루프 (`ReservationScheduler._loop`, `SingleInstanceServer._acceptLoop`) | 로그 후 계속 |
| 실행 주소 처리 (`KtopiaLauncher._handleLaunchUrl`) | 잘못된 주소(ValueError)는 상태표시에 안내 |
| 시작점 (`main.main`) | 로그 후 종료 |

- **예외가 아니라 "확인"인 경우**는 그 자리에서 받는다: 레지스트리 키 없음(`FileNotFoundError`), 포트 사용 중(`OSError`), 큐 비었음(`queue.Empty`)
- 던질 때는 의미 있는 타입을 쓴다 (`ValueError`, `KeyError`, `TypeError`). `Exception`을 그대로 던지지 않는다.
- 빈 `except` 금지, 받으면 최소한 로그를 남긴다.

## 9. 문자열 비교 (원본 §0.7)
- 식별자(코드값·파라미터명·컬럼명) 비교는 `StringUtil.equalsIgnoreCase(a, b)`
- 사용자 데이터 비교는 `==`

## 10. Util 클래스 (원본 §0.10)
- 전부 `@staticmethod`로 만들고, `__init__`에서 `TypeError`를 던져 인스턴스 생성을 막는다.
- Python은 상속을 문법으로 막을 수 없으므로 상속하지 않는 것을 규칙으로 지킨다.

## 11. 메서드 체이닝 금지 (원본 §13)
- `a.strip().lower()`처럼 이어 부르지 않고 변수에 나눠 담는다.
- `super().__init__()`도 체이닝이므로 `부모클래스.__init__(self, ...)`로 쓴다.
- 모듈 경로(`os.path.join`, `urllib.parse.urlsplit`)는 체이닝이 아니다.

## 12. 람다 금지 (원본 §14)
- `lambda`를 쓰지 않는다. 콜백에는 **이름 있는 메서드**를 넘긴다 (`command=self.openTaskList`).
- Python에는 익명 클래스가 없으므로, Java의 "익명 클래스로 대체"는 "이름 있는 메서드로 대체"로 옮긴다.

## 13. 로거 (원본 §0.6)
- 클래스 맨 위에 상수로 한 번 선언: `LOGGER = logging.getLogger(__name__)`
- `__name__`은 `폴더.클래스명`(예: `task.ManageTestTaskList`)이 되어 로그에 위치가 그대로 남는다 (문자열 범주를 따로 쓰지 않는다).

## 14. null 처리 (원본 §10)
- 목록을 돌려주는 메서드는 `None` 대신 빈 리스트를 돌려준다.
- 문자열 표시용 값은 `StringUtil.nvl(값, "")`로 받는다.
