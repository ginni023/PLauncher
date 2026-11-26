# ConfigDialog

**설정 UI**

config.properties의 키를 한 화면에 보여준다.

- 경로(INSTALL/NODEJS/PLAYWRIGHT/SAVE_PATH): 읽기 전용
- Y/N 키: 켜고 끄는 스위치(`primary-round-toggle`), RESERVATION_CHECK_TIME: 1~1440 숫자
- 버튼: [인증](남색 테두리), [적용](남색), [닫기](회색)
- 인증 아이디: [인증] 버튼으로 시스템 도메인 API 확인. 아이디를 바꾸면 인증해야 적용 가능 (빈 값은 허용)
- [적용] 버튼(우측 하단): 변경이 있고, 인증이 됐고, 예약 체크 타임이 올바를 때만 활성화. 눌러야 저장된다

## 메서드

| 메서드 | 설명 |
|---|---|
| `_onApply()` | 저장 → 레지스트리 반영(LINK_REGST_IND) → 런처에 알림 |
| `_onAuthenticate()` | SystemApiClient.authenticate 호출 |

소스: [src/main/ui/dialog/ConfigDialog.py](../../../../src/main/ui/dialog/ConfigDialog.py)
