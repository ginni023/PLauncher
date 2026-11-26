# ProtocolRegistry

**ktopia:// 레지스트리 등록**

`HKEY_CURRENT_USER\Software\Classes\ktopia`에 등록한다 (관리자 권한 불필요).
- 기본값 `URL:ktopia Protocol`, `URL Protocol` 값, `DefaultIcon`
- `shell\open\command` = `"KTOPIA.exe 경로" "%1"` (소스 실행 시 `"pythonw.exe" "main.py" "%1"`)

## 메서드

| 메서드 | 설명 |
|---|---|
| `applyConfig(oConfig)` | LINK_REGST_IND=Y면 (명령이 다를 때만) 등록, N이면 해제 |
| `register() / unregister()` | 등록 / 하위 키까지 삭제 |
| `isRegistered()` | 등록된 명령이 현재 실행 파일과 같은지 |
| `getCommand()` | 등록할 명령 문자열 |

## 참고

exe 위치를 옮기면 다음 실행 때 새 경로로 다시 등록된다.

소스: [src/main/engine/ProtocolRegistry.py](../../../src/main/engine/ProtocolRegistry.py)
