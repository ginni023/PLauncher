# ReservationScheduler

**예약 확인 스레드**

10초마다 실행된다.
1. RESERVATION_USE=Y이고 마지막 조회 후 RESERVATION_CHECK_TIME(분)이 지났으면 예약 API를 조회해 받은 작업을 `addTask`
2. `checkReservations()`로 시간이 된 예약 작업을 예약 QUEUE로

## 메서드

| 메서드 | 설명 |
|---|---|
| `start() / stop()` | 스레드 시작 / 정지 신호 |
| `_loop()` | 스레드 경계. 예외는 로그 후 계속 |

## 참고

예약 API(`SystemApiClient.fetchReservations`)는 현재 임시 구현(빈 목록).

소스: [src/main/task/ReservationScheduler.py](../../../src/main/task/ReservationScheduler.py)
