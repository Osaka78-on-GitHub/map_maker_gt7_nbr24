START Ask Brave
can python make a filename from the script name?



Searched Python script filename derivation
Exploring Python script filename derivation

Skipping web search; using known Python knowledge

python get script filename from __file__ pathlib
Yes:

from pathlib import Path

stem = Path(__file__).stem  # "GT7_udp_C_raw_tap"
out = Path(f"{stem}.pcap")  # "GT7_udp_C_raw_tap.pcap"

.name gives you GT7_udp_C_raw_tap.py, .stem gives you GT7_udp_C_raw_tap (no extension). So you can name your output file after the script with zero hardcoding — rename the script and the output follows.
END Ask Brave
START Ask Brave
im not talking about that. im saying two ps one port, youre saying 1 ps 2 ports


Checked PS5 GT7 UDP port configuration
You're right, my bad — I answered the wrong question.

No. GT7 has no setting to change the destination port.  The PS5 always sends telemetry to port 33740 on whatever IP you enter in the game. There's no in-game option, no PS5 system setting, nothing. 

So if you have two PS5s both pointed at the same PC, both will try to send to that PC's port 33740 and they'll conflict.

The only workaround is a network-level redirect on the PC side — e.g. an iptables/nftables rule (Linux) or a third-party tool that intercepts packets from one PS5's source IP and rewrites the destination port before the application receives them:

# Linux example: redirect PS5 #2's traffic from :33740 → :33741
iptables -t nat -A PREROUTING -i eth0 -s 192.168.1.50 -p udp --dport 33740 -j REDIRECT --to-port 33741

Then your receiving app binds 33740 for PS5 #1 and 33741 for PS5 #2. Each PS5 still "thinks" it's sending to 33740 — the PC just silently rewrites one of them.

On Windows this is harder (no native equivalent of iptables); you'd need something like netsh interface portproxy won't work for UDP, so you're looking at a small custom relay or a Linux box as the network gateway.


Copy


ok good. so its solved



Confirmed problem solved
Yeah, the iptables redirect on the PC side is the cleanest fix. Both PS5s keep their default 33740 config, and the PC just splits them apart before the app sees them.
END Ask Brave
START Ask Brave
**Start with one file, then split only when you feel the pain.** The common-sense progression:

1. **Extract functions first.** If a chunk of code needs a comment to explain *what* it's doing, pull it into a function and name it after that "what." One function = one job.

2. **Group related functions into modules (files).** When you have a cluster of functions that all deal with the same concern (e.g. all file I/O, all API calls, all data cleaning), move them into their own `.py` file.

3. **Keep a single entry point.** Your top-level script should just orchestrate:

```python
# main.py
from data_processor import clean, transform
from report_generator import write_report

def main():
    raw = load_data()
    clean(raw)
    transform(raw)
    write_report(raw)

if __name__ == "__main__":
    main()
```

4. **Organize by domain, not by type.** Put "all the auth stuff" together, "all the payments stuff" together — not `all_models.py` / `all_views.py` unless a framework demands it.

**Rules of thumb:**

- **Don't pre-architect.** Write it dirty in one file, then refactor. If you don't need a module yet, you don't need one.
- **Don't over-split.** A file with 30 lines of code doesn't deserve its own module.
- **Pass data as arguments** between modules rather than having them mutate shared globals — this keeps them loosely coupled and testable.

That's the whole "common sense" version: **function → module → package**, each step triggered by a real readability or reuse need, not by a line-count threshold.

END Ask Brave
Start Ask Brave
Got it. Your problem is: **AI adds 20 unnecessary things, you need to find and delete them in 1 minute without breaking the script.**

This is a mechanical process, not a design exercise.

## The 1-Minute Process

### Step 1: Let the tools find the dead stuff (30 seconds)

```bash
pip install vulture ruff
```

```bash
# Finds unused functions, classes, variables, imports
vulture your_script.py --min-confidence 80

# Finds unused imports, undefined names, basic issues
ruff check your_script.py --select F401,F841
```

`vulture` output looks like:

```
your_script.py:12: unused function 'validate_input' (60% confidence)
your_script.py:34: unused import 'json' (90% confidence)
your_script.py:58: unused variable 'result' (100% confidence)
```

**Delete everything it reports at 80%+ confidence.** That's your first 5-10 of the 20 stupid things, found automatically.

### Step 2: Eyeball for the AI bloat patterns (30 seconds)

These are the things tools **can't** catch but you can spot in a scan:

| Pattern | What it looks like | Action |
|---------|-------------------|--------|
| `try/except Exception: pass` | Wraps code that can't actually fail | Delete the try/except, keep the inner code |
| Helper function called **exactly once** | `def _format_x(x): return x.strip()` | Inline it at the call site |
| Constant used **exactly once** | `MAX_RETRIES = 3` used in one place | Replace with the literal `3` |
| Comment/docstring that restates the code | `# Get the user name` above `name = user.name` | Delete the comment |
| Class with a single method | `class DataProcessor: def process(self, d): ...` | Make it a function |
| Logging to nowhere | `logger.info("processing...")` with no handler configured | Delete |
| Redundant validation | `if x is not None and len(x) > 0` when `x` is guaranteed non-empty | Delete the check |
| Duplicate logic | Two functions that do the same thing slightly differently | Keep one, delete the other |
| "Robust" error handling | `except (ValueError, TypeError, KeyError): return default` around a simple operation | Delete the except |
| Type hints that are wrong | `def foo(x: str) -> list` when it actually returns a dict | Delete the hints |

**The rule for each:** if you delete it and the script still runs the same, it was stupid.

### Step 3: Delete in bulk, then run

Don't delete one at a time. Select all the stupid stuff, delete it in one pass, then:

```bash
python your_script.py
```

If it works → done. If it breaks → the error tells you exactly which deletion was wrong. Undo just that one.

## Why This Works in 1 Minute

- `vulture` does the tedious "is this function ever called?" search for you
- The bloat patterns are **visually obvious** once you know what to look for — they're the same 10 patterns every time
- The "delete and run" test is your safety net. You don't need to *understand* the code to delete the parts that don't affect output. You just need to know the script was working before.

## The Mental Shortcut

When you look at AI-generated code, ask one question per block:

> **"If I delete this, does the output change?"**

If no → delete. You don't need to understand *why* it's there. AI put it there because it was trained to look thorough, not because the code needs it.

END Ask Brave
