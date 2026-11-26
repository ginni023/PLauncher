# TaskListDialog

**작업목록**

TASK_TYPE이 RESERVATION이 아닌 작업 전체, 최근 등록순. 작업 상태가 바뀌면 열린 채로 갱신된다.

컬럼: No, 테스트명, 작업타입, 상태, 결과, 수행시간(RUN_DATE — 작업이 시작된 시각). No는 화면에 보이는 순서대로 1~N (DB 값이 아님). 등록일시는 보여주지 않는다 (정렬에만 사용).

소스: [src/main/ui/dialog/TaskListDialog.py](../../../../src/main/ui/dialog/TaskListDialog.py)
