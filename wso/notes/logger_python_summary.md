**Two things that are actually wrong:**

**1. No formatter.** Your output is just the raw string you pass to `logger.info()`. No timestamp. No level name. No line number. You need a `Formatter` attached to the handler:

```python
_handler = logging.StreamHandler()
_handler.setFormatter(logging.Formatter(
    "%(asctime)s %(levelname)s %(name)s: %(message)s"
))
logger.addHandler(_handler)
```

That's the difference between `"[msg_body] hello"` and `"2026-11-18 14:32:01,234 INFO notify: [msg_body] hello"`.

**2. All your wrappers log at `INFO`.** `FAIL`, `STOP`, `PASS`, `TEST` all call `logger.info()`. That means if you set the level to `ERROR`, everything disappears. You need:

```python
def FAIL(msg: str = None) -> None: msg_body(msg, level=logging.ERROR)
def STOP(msg: str = None) -> None: msg_body(msg, level=logging.CRITICAL)
def PASS(msg: str = None) -> None: msg_body(msg, level=logging.INFO)
def TEST(msg: str = None) -> None: msg_body(msg, level=logging.DEBUG)
def INFO(msg: str = None) -> None: msg_body(msg, level=logging.INFO)
```

And `msg_body` needs to accept and use the level:

```python
def msg_body(msg, whoami=False, level=logging.INFO) -> None:
    if whoami:
        logger.log(level, "[%s] [%s] [%s] [%s]",
            funcname(depth=2), modulename(depth=3),
            msg or "no message", funcname(depth=3))
    else:
        logger.log(level, "[%s] %s", funcname(depth=2), msg or "")
```

`logger.log(level, ...)` is the generic method. `logger.info(...)`, `logger.error(...)`, etc. are just shortcuts that hardcode the level.

---

**What the module can do that you're not using, grouped by what problem it solves:**

**Output to multiple destinations at once:**

```python
# stderr (for dev)
_sh = logging.StreamHandler()
_sh.setFormatter(fmt)
logger.addHandler(_sh)

# file (for the pipe to read)
_fh = logging.FileHandler("/var/log/notify/app.log")
_fh.setFormatter(fmt)
logger.addHandler(_fh)
```

Both get every message. The logger fans out to all attached handlers. You can have as many as you want.

**Rotating file output** (so the log file doesn't grow forever):

```python
from logging.handlers import RotatingFileHandler

_fh = RotatingFileHandler(
    "/var/log/notify/app.log",
    maxBytes=5_000_000,   # 5 MB
    backupCount=3,        # keep 3 old files
)
```

Or time-based:

```python
from logging.handlers import TimedRotatingFileHandler

_fh = TimedRotatingFileHandler(
    "/var/log/notify/app.log",
    when="midnight",      # rotate every day
    backupCount=7,        # keep 7 days
)
```

**Per-module loggers** (set different levels for different parts of your app):

```python
log_db = logging.getLogger("notify.db")       # child of "notify"
log_db.setLevel(logging.DEBUG)                 # db gets debug output

log_net = logging.getLogger("notify.net")      # another child
log_net.setLevel(logging.WARNING)              # net only gets warnings
```

The hierarchy is by dot notation. `notify.db` inherits from `notify` unless you override. If `notify` is `INFO` and `notify.db` is `DEBUG`, the db logger emits DEBUG and above, everything else emits INFO and above.

**Traceback on errors:**

```python
try:
    do_thing()
except Exception:
    logger.exception("do_thing failed")
    # automatically appends the full traceback to the message
```

`logger.exception()` is `logger.error()` + traceback. No need to call `traceback.format_exc()` yourself.

**Check before doing expensive work:**

```python
if logger.isEnabledFor(logging.DEBUG):
    # only build this expensive string if it will actually be emitted
    detailed = compute_expensive_debug_string()
    logger.debug("%s", detailed)
```

Without this check, Python still evaluates the arguments to `logger.debug()` even if the level is too low. For cheap strings it doesn't matter. For expensive ones it does.

**Flush on exit** (so the file handler actually writes the last few lines):

```python
import atexit
atexit.register(logging.shutdown)
```

Without this, if your script crashes or exits abruptly, the last few buffered log lines might be lost.

**Capture `warnings` into the logging system:**

```python
logging.captureWarnings(True)
```

Now `warnings.warn("...")` calls go through your logger instead of printing to stderr directly. Useful if a third-party library spams warnings and you want them in your log file with timestamps.

---

**The full picture of what a `LogRecord` carries** (the object that flows from logger through handlers):

| Attribute | What it is |
|-----------|-----------|
| `name` | Logger name (`"notify"`) |
| `levelno` / `levelname` | 20 / `"INFO"` |
| `msg` | Your message string |
| `args` | The format args (if any) |
| `message` | `msg % args` (filled in) |
| `asctime` | Timestamp (set by the formatter) |
| `pathname` | Full path to the source file |
| `filename` | Just the filename |
| `module` | Module name (filename without `.py`) |
| `funcName` | The function name |
| `lineno` | Line number |
| `process` / `processName` | PID / process name |
| `thread` / `threadName` | Thread ID / name |
| `exc_info` / `exc_text` | Traceback (if using `logger.exception()`) |
| `stack_info` | Stack trace (if using `stack_info=True`) |

You can reference any of these in your format string:

```python
logging.Formatter("%(asctime)s %(levelname)s %(module)s:%(lineno)d %(funcName)s: %(message)s")
# 2026-11-18 14:32:01,234 INFO mymodule:42 msg_body: [msg_body] hello
```

That's everything. The module is small. The surface area is: `Logger` (decides whether to emit), `Handler` (decides where to send), `Formatter` (decides what it looks like), `Filter` (extra per-handler rules beyond level). That's the whole system. Everything else is convenience wrappers around those four.

