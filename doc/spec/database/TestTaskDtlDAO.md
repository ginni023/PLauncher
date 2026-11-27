# TestTaskDtlDAO

**TEST_TASK_DTL 접근**

작업의 동작(TestTaskDtlDTO)을 등록·수정·조회한다. SQL은 [mainSql.xml](../../../resource/db/mainSql.xml), 바인드 값은 `TestTaskDtlDTO.toParams()`.

## 메서드

| 메서드 | SQL | 설명 |
|---|---|---|
| `selectTestTaskDtlList(strTaskId)` | `selectTestTaskDtlList` (S) | 작업의 동작 목록, DATA_SEQ·ACT_NO 순 → TestTaskDtlDTO 리스트 |
| `selectTestTaskDtl(oDtl)` | `selectTestTaskDtl` (S) | 동작 1건 (TASK_ID + DATA_SEQ + ACT_NO) → TestTaskDtlDTO, 없으면 None |
| `insertTestTaskDtl(oDtl)` | `insertTestTaskDtl` (I) | 동작 등록 (전체 컬럼). 없는 TASK_ID면 외래키 오류 |
| `updateTestTaskDtlResult(oDtl)` | `updateTestTaskDtlResult` (U) | 동작 결과·상태·결과 상세·에러 CLASS·에러 메시지 변경 (TASK_ID + DATA_SEQ + ACT_NO) |

소스: [src/main/database/TestTaskDtlDAO.py](../../../src/main/database/TestTaskDtlDAO.py)
