# SingleInstanceServer

**중복 실행 방지와 주소 전달**

`127.0.0.1:47321`에 TCP 서버를 연다(`SO_EXCLUSIVEADDRUSE`). 이미 열려 있으면 다른 런처가 실행 중인 것이다. 두 번째 실행은 받은 주소(없으면 빈 문자열)를 보내고 종료한다.

## 메서드

| 메서드 | 설명 |
|---|---|
| `start()` | 포트를 열면 True. 이미 사용 중이면 False |
| `stop()` | 서버 닫기 |
| `sendToRunning(strMessage) [static]` | 실행 중인 런처에 UTF-8로 보내기 |
| `_acceptLoop()` | 스레드 경계. 받은 문자열을 생성자의 `fnOnMessage`로 넘긴다 |

## 참고

PC 안(127.0.0.1)에서만 접속된다. 다른 프로그램이 47321 포트를 쓰고 있으면 런처가 실행되지 않는다 (로그에 남음).

소스: [src/main/engine/SingleInstanceServer.py](../../../src/main/engine/SingleInstanceServer.py)
