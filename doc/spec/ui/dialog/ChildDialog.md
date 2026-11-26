# ChildDialog

**자식 Dialog 공통**

부모 위 가운데에 뜨는 크기 고정 모달 창(`ttkbootstrap.Toplevel`, 메인 창의 테마·아이콘을 그대로 씀). 열려 있는 동안 부모는 사용자가 조작할 수 없다(`grab_set`). 시스템에 의한 부모 화면 갱신은 계속된다.

## 메서드

| 메서드 | 설명 |
|---|---|
| `showModal()` | 보이고 입력을 가져온다 |
| `closeDialog()` | 입력 반납, 부모가 ChildDialog면 부모에 입력 돌려줌, 닫힘 콜백 호출 |
| `openChild(oDialog)` | 이 창의 자식 열기 (중첩 모달) |
| `bringToFront()` | 가장 안쪽 자식을 앞으로 |
| `refresh()` | 하위 클래스가 재정의 — 작업 이벤트 때 불린다 |

소스: [src/main/ui/dialog/ChildDialog.py](../../../../src/main/ui/dialog/ChildDialog.py)
