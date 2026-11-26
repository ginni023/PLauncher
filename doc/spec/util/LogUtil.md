# LogUtil

**로그 설정**

`<기준>/log/ktopia.log`, UTF-8, 5MB × 5개 순환, INFO 이상. 각 클래스는 `LOGGER = logging.getLogger(__name__)`.

## 메서드

| 메서드 | 설명 |
|---|---|
| `setup()` | 한 번만 설정 |

소스: [src/main/util/LogUtil.py](../../../src/main/util/LogUtil.py)
