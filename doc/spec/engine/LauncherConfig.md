# LauncherConfig

**설정 (config.properties)**

실행 파일과 같은 폴더의 `config.properties`. 키와 기본값은 [설계서 §6](../../KTOPIA_설계서.md#6-설정) 참고.

- 파일이 없으면 기본값으로 만들고 `isCreated()`가 True (첫 실행 → 설정 창)
- 없는 키는 기본값으로 채운다
- 런처 버전은 상수 `LAUNCHER_VERSION` (현재 `0.1.0`, init 1단계 버전 체크에 사용)
- INSTALL_PATH, NODEJS_PATH, PLAYWRIGHT_PATH, SAVE_PATH는 **시작할 때마다 현재 폴더 기준으로 다시 계산**한다

## 메서드

| 메서드 | 설명 |
|---|---|
| `load() / save()` | 읽기 / 쓰기 |
| `getValue(strKey) / setValue(strKey, strValue)` | 값 (없으면 "") |
| `isYes(strKey)` | Y/N 값이 Y인지 |
| `getReservationCheckMinutes()` | RESERVATION_CHECK_TIME (잘못된 값이면 5) |
| `copyValues()` | 전체 값 복사본 |
| `getDefaultValues() [static]` | 기본값 |

## 참고

키 상수(`LauncherConfig.RESERVATION_SYSTEM` 등)와 `KEY_ORDER`(파일·화면 순서), `AUTO_PATH_KEYS`, `FLAG_KEYS`를 제공한다.

소스: [src/main/engine/LauncherConfig.py](../../../src/main/engine/LauncherConfig.py)
