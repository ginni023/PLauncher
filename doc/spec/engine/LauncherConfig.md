# LauncherConfig

**설정 (config.properties)**

실행 파일과 같은 폴더의 `config.properties`. 키와 기본값은 [설계서 §6](../../KTOPIA_설계서.md#6-설정) 참고.

- 파일이 없으면 기본값으로 만들고 `isCreated()`가 True (첫 실행 → 설정 창)
- 없는 키는 기본값으로 채운다
- 런처 버전은 실행 파일 기준 폴더의 **`.launcher` 파일**에서 읽는다 (`readLauncherVersion()`, init 1단계 버전 체크에 사용). 파일 내용은 버전 문자열만 (예: `1.0`). 앞뒤 공백·줄바꿈·UTF-8 BOM은 무시, 파일이 없으면 `""`
- INSTALL_PATH, NODEJS_PATH, PLAYWRIGHT_PATH, SAVE_PATH는 **시작할 때마다 현재 폴더 기준으로 다시 계산**한다

## 메서드

| 메서드 | 설명 |
|---|---|
| `load() / save()` | 읽기 / 쓰기 |
| `readLauncherVersion() [static]` | `.launcher` 파일의 런처 버전 (없으면 `""`) |
| `getVersionFilePath() [static]` | `.launcher` 경로 |
| `getValue(strKey) / setValue(strKey, strValue)` | 값 (없으면 "") |
| `isYes(strKey)` | Y/N 값이 Y인지 |
| `getReservationCheckMinutes()` | RESERVATION_CHECK_TIME (잘못된 값이면 5) |
| `copyValues()` | 전체 값 복사본 |
| `getDefaultValues() [static]` | 기본값 |

## 참고

키 상수(`LauncherConfig.RESERVATION_SYSTEM`, `API_TOKEN` 등)와 `KEY_ORDER`(파일·화면 순서), `AUTO_PATH_KEYS`, `FLAG_KEYS`, `SECRET_KEYS`(화면에서 가릴 키: API_TOKEN)를 제공한다.

API_TOKEN은 config.properties에 **평문**으로 저장된다 (암호화는 `secure` 폴더에서 추후).

소스: [src/main/engine/LauncherConfig.py](../../../src/main/engine/LauncherConfig.py)
