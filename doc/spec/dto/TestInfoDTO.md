# TestInfoDTO

**TEST_TASK_DTL 대응 객체**

작업 안의 동작 1건을 담는다. 구조는 TestTaskDTO와 같다.

- INTEGER 컬럼(DATA_SEQ, DELAY_TIME, ACT_NO)은 `m_n…` / `getN…()` / `setN…(nValue)`
- 기본값: DATA_SEQ=0, DELAY_TIME=2, ACT_NO=0
- int set 함수는 None을 0으로 바꾼다

## 메서드

| 메서드 | 설명 |
|---|---|
| `fromRow(oRow) [static]` | sqlite3.Row → 객체 |
| `toParams()` | {바인드 변수명: 값} |

소스: [src/main/dto/TestInfoDTO.py](../../../src/main/dto/TestInfoDTO.py)
