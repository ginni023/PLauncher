# TestCommDAO

**TEST_COMM_LIST 접근**

공통 정보(TestCommDTO)를 등록·수정·조회한다. SQL은 [mainSql.xml](../../../resource/db/mainSql.xml), 바인드 값은 `TestCommDTO.toParams()`.

## 메서드

| 메서드 | SQL | 설명 |
|---|---|---|
| `selectTestCommList(strUprDivKey)` | `selectTestCommList` (S) | 구분키의 목록, META_KEY 순 → TestCommDTO 리스트 |
| `selectTestComm(oComm)` | `selectTestComm` (S) | 1건 (UPR_DIV_KEY + META_KEY) → TestCommDTO, 없으면 None |
| `insertTestComm(oComm)` | `insertTestComm` (I) | 등록 (SYS_RECD_CHG_DT 제외) |
| `updateTestComm(oComm)` | `updateTestComm` (U) | 수정일·제목·추가 제목·값·상세 설명 변경 |

## 참고

사용처: [CrawlingRunner](../runner/CrawlingRunner.md)의 시스템 정보 저장 (UPR_DIV_KEY `PL_UI_SYSTEM_INFO`).

소스: [src/main/database/TestCommDAO.py](../../../src/main/database/TestCommDAO.py)
