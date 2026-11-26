# DatabaseUtil

**SQLite 연결과 SQL XML 처리**

DB 파일: `resource/db/ktopia.db` (PathUtil 기준). SQL은 같은 폴더의 `initSql.xml`, `mainSql.xml`에서 읽는다.

## 메서드

| 메서드 | 설명 |
|---|---|
| `connect()` | 폴더가 없으면 만들고 연결. `row_factory=sqlite3.Row`, `PRAGMA foreign_keys = ON` |
| `initDb()` | initSql.xml에서 `version > PRAGMA user_version`인 항목만 순서대로 실행하고 user_version을 최댓값으로 올린다 |
| `initMappingQuery()` | 쿼리를 세 맵에 로딩 (런처 시작 init 2단계). 아래 표 참고 |
| `getSelectQuery(id)` / `getExecuteQuery(id)` / `getSystemQuery(id)` | 각 맵에서 SQL 반환. 없으면 KeyError |
| `executeUpdate(strSqlId, mapParams)` | **executeQueryMap**의 SQL 실행 후 commit |
| `selectRows(strSqlId, mapParams)` | **selectQueryMap**의 SQL 조회 결과 행 리스트 |

**쿼리 맵** (`initMappingQuery`)

| 맵 | 들어가는 SQL |
|---|---|
| `selectQueryMap` (`s_mapSelectQuery`) | mainSql.xml 중 `type="S"` |
| `executeQueryMap` (`s_mapExecuteQuery`) | mainSql.xml 중 `type="I"`, `"U"`, `"D"` |
| `systemQueryMap` (`s_mapSystemQuery`) | initSql.xml 전체 (테이블·인덱스 구조 SQL) |

- mainSql.xml에 `type`이 없거나 S/I/U/D가 아니면 ValueError로 시작이 멈춘다.
- select용 id를 `executeUpdate`에 넘기거나 그 반대면 KeyError — 조회와 변경이 섞이지 않게 한다.

## 참고

- 연결은 호출마다 열고 닫는다 (여러 스레드에서 안전하게 쓰기 위해).
- `initMappingQuery()` 전에는 어떤 SQL도 쓸 수 없다. mainSql.xml을 고치면 런처를 다시 시작해야 반영된다.
- `initDb()`는 init보다 먼저(런처 시작 직후) initSql.xml을 직접 읽어 실행한다. `systemQueryMap`은 같은 내용을 id로 찾아 쓸 수 있게 둔 것이다.

소스: [src/main/database/DatabaseUtil.py](../../../src/main/database/DatabaseUtil.py)
