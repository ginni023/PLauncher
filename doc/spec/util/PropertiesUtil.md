# PropertiesUtil

**properties 파일 읽기/쓰기**

Java properties 형식과 호환: `키=값`, `#`·`!` 주석, 값의 `\\`, `\n`, `\r`, `\t` 이스케이프. UTF-8.

## 메서드

| 메서드 | 설명 |
|---|---|
| `load(strPath)` | dict (파일이 없으면 빈 dict) |
| `store(strPath, mapValues, arrKeyOrder, strHeader)` | 헤더·시각 주석 + 키 순서대로 저장 |

소스: [src/main/util/PropertiesUtil.py](../../../src/main/util/PropertiesUtil.py)
