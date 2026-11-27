# LoginGuideDialog

**로그인 안내 창**

크롤링 작업에서 로그인이 필요할 때(`loginYn=Y`) 띄우는 창. 사용자가 브라우저에서 로그인을 마치고 [확인]을 누르면 `ManageTestTaskList.confirmLogin()` → 크롤링 엔진이 세션을 저장한다.

- 제목 "로그인 안내", 내용 "브라우저에서 로그인을 마친 뒤 이 창의 [확인] 버튼을 눌러주세요. (브라우저는 닫지 마세요)", 버튼 [확인]
- 브라우저 창에 가리지 않도록 **항상 위**(topmost)
- 창의 X(닫기)도 [확인]과 같게 처리 — 창을 닫아 로그인 대기가 멈추지 않게
- 로그인이 다른 이유로 끝나면(브라우저를 닫음, 작업 중지) 런처가 창을 자동으로 닫는다 (`WorkDialog.closeLoginGuide`)
- 다른 자식 Dialog가 열려 있으면 그 위에 자식으로 연다

## 메서드

| 메서드 | 설명 |
|---|---|
| `__init__(oParent, fnOnConfirm, fnOnClose)` | fnOnConfirm: [확인] 때 부를 함수 |
| `confirmLogin()` | fnOnConfirm 호출 후 닫기 |

소스: [src/main/ui/dialog/LoginGuideDialog.py](../../../../src/main/ui/dialog/LoginGuideDialog.py)
