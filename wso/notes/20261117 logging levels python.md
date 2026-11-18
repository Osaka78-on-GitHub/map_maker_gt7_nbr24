Q yeah ive got that sort of thing already. pass fail info stop and test

but im talking like if the user hates notifications or i want to do a debug>
do you have to do conditional logic or does logging have it

Yes, `logging` has it built in. You set a threshold once and everything below it is silently dropped — no conditional logic in your code:

```python
import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)  # only INFO, WARNING, ERROR, CRITICAL get through
```

```python
# in your functions, just call the right level:
logger.debug("checking %s", ip)      # suppressed (below threshold)
logger.info("pass: %s", ip)          # shown
logger.error("fail: %s", ip)         # shown
```

To switch to debug mode, just change the level — no code changes:

```python
# quiet (default)
logger.setLevel(logging.WARNING)   # only WARNING, ERROR, CRITICAL

# normal
logger.setLevel(logging.INFO)      # INFO and up

# verbose / debug
logger.setLevel(logging.DEBUG)     # everything
```

Or control it from the command line without touching the file:

```python
import sys, logging

level = logging.DEBUG if "--debug" in sys.argv else logging.INFO
logger.setLevel(level)
```

```bash
$ python bridge.py            # quiet
$ python bridge.py --debug    # verbose
```

That's the whole mechanism. No `if user_hates_notifications:` checks anywhere. The level *is* the conditional, set once at startup.

Your `PASS`/`FAIL`/`INFO`/`STOP`/`TEST` functions would just map to the right level:

```python
def PASS(msg: str = None) -> None:
    logger.info("[%s] %s", funcname(depth=2), msg or "[no message]")

def FAIL(msg: str = None) -> None:
    logger.error("[%s] %s", funcname(depth=2), msg or "[no message]")

def TEST(msg: str = None) -> None:
    logger.debug("[%s] %s", funcname(depth=2), msg or "[no message]")
```

Set the logger to `INFO` → `TEST` is silent. Set it to `DEBUG` → everything shows. One knob, no conditionals.

