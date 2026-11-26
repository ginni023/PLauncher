# LauncherEnvironment

**실행 환경 확인 (Node.js, Playwright)**

런처 시작 init 3·4단계에서 쓴다. 런처 폴더에 넣어 배포하는 Node.js·Playwright만 본다 (PC에 설치된 Node.js는 보지 않는다).

## 메서드

| 메서드 | 설명 |
|---|---|
| `isNodeInstalled(oConfig)` | `NODEJS_PATH\node.exe`가 있는지 |
| `isPlaywrightInstalled(oConfig)` | `PLAYWRIGHT_PATH\node_modules\@playwright\test\package.json`이 있는지 (UI TEST용 `@playwright/test` 설치 여부) |
| `getNodeExePath(oConfig)` / `getPlaywrightPackagePath(oConfig)` | 확인하는 파일 경로 (로그용) |

## 참고

크롤링에 쓰는 Python판 Playwright(crawling 패키지)는 별개다. 여기서는 UI TEST용 Node.js 쪽만 확인한다.

소스: [src/main/engine/LauncherEnvironment.py](../../../src/main/engine/LauncherEnvironment.py)
