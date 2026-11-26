# TestTaskDTO

**TEST_TASK_LIST 대응 객체**

작업 1건의 데이터를 담는다. 컬럼마다 멤버변수와 get/set 함수가 있다. 멤버변수 목록은 [DEVELOPMENT.md DB 스키마](../../DEVELOPMENT.md#test_task_list--작업-테이블-객체-testtaskdto) 참고.

- 기본값: DEVICE=`"PC"`, 나머지 문자열은 `None`
- `COLUMNS`: (컬럼명, 바인드 변수명, get 함수명, set 함수명) 목록

## 메서드

| 메서드 | 설명 |
|---|---|
| `fromRow(oRow) [static]` | sqlite3.Row → 객체. 결과에 있는 컬럼만 set 함수로 넣는다 |
| `getStrXxx() / setStrXxx(strValue)` | VARCHAR 컬럼. set은 None을 그대로 두고 그 외는 str로 바꾼다 |
| `toParams()` | {바인드 변수명: 값} — mainSql.xml의 `:task_Id` 등에 그대로 쓴다 |

## 참고

이 파일은 컬럼 정의에서 생성했다. 컬럼이 바뀌면 같은 규칙으로 함께 고친다.

소스: [src/main/dto/TestTaskDTO.py](../../../src/main/dto/TestTaskDTO.py)
