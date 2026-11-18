Got it. Your problem is: **AI adds 20 unnecessary things, you need to find and delete them in 1 minute without breaking the script.**

**AI Bloat Removal in 60s:**

1. **Auto-detect (30s):** Run `vulture` (unused functions/vars) + `ruff` (unused imports). Delete everything flagged ≥80% confidence.

2. **Eyeball 10 patterns (30s):** Empty `except: pass`, single-use helpers/constants, restating comments, single-method classes, orphan logging, redundant checks, duplicate logic, over-broad `except`, wrong type hints.

3. **Delete in one pass, run the script.** If it breaks, undo just that one deletion.

**Core rule:** *If deleting it doesn't change output, it wasn't needed.*



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

