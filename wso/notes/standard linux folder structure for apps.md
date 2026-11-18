## Osaka78 says
can you explain to me the standard linux folder structure for apps

## Ask Brave says
The FHS (Filesystem Hierarchy Standard) — [spec](https://specifications.freedesktop.org/fhs/latest/) — organises everything around one principle: **separate the code from the config from the data from the state.**

| Directory | What goes there | Changes at runtime? |
|-----------|----------------|:-------------------:|
| `/usr/bin` | The app's executable (code) | No |
| `/usr/lib` | Libraries the app needs | No |
| `/usr/share` | Arch-independent data (icons, man pages, templates) | No |
| `/etc/yourapp/` | Config files (the farmer's rules) | On admin edit |
| `/var/lib/yourapp/` | Persistent state (databases, spools) | Yes |
| `/var/log/yourapp/` | Log files | Yes |
| `/var/cache/yourapp/` | Cache (safe to delete) | Yes |
| `/var/run/yourapp/` | PID files, sockets (cleared on boot) | Yes |
| `/opt/yourapp/` | Self-contained third-party app (alternative to `/usr`) | No |
| `/usr/local/` | Manually compiled software (not from apt) | No |

**The mental model:**

```
/usr       = the sheep (code, read-only, shared)
/etc       = the fence rules (config, you edit it)
/var       = the pasture (things that grow, change, get eaten)
/opt       = a whole other farm (self-contained, doesn't mix with /usr)
```

**Why it matters for your project:**

If your app follows FHS, you get the wall for free:

| Layer | FHS equivalent |
|-------|---------------|
| The wall (can't write back) | `/usr` is read-only. The app's code can't be modified at runtime. |
| The config | `/etc/yourapp/` — only root writes here. |
| The pipe's output | `/var/log/yourapp/` — the app writes, the farmer reads. |
| The state | `/var/lib/yourapp/` — the app owns it, nothing else touches it. |

That's your "file is the wall" pattern, already baked into the OS layout. The app writes to `/var/log/yourapp/`. The farmer reads it. The farmer can't write to `/usr/bin/yourapp`. The app can't write to `/etc/yourapp/`. The OS enforces it. No code needed.

**The one rule that trips people up:**

`/var` is the *only* place where an app writes data at runtime. If your app needs to write a file, it goes in `/var/something/yourapp/`. If it's code or static data, it goes in `/usr/`. If it's config, it goes in `/etc/`. That's the whole standard. Everything else is subdirectory naming.


## Osaka78 says
so how does a good repo mirror that philosophy?

## Ask Brave says

The repo is `/usr`. Everything else is generated or local.

| FHS | Repo equivalent | In git? |
|-----|----------------|:-------:|
| `/usr/bin` (code) | `.py` files, the actual app | ✅ |
| `/usr/share` (static data) | Templates, schema files, constants | ✅ |
| `/etc/yourapp/` (config) | `config.example.toml` (a template) | ✅ |
| `/etc/yourapp/` (actual config) | `config.toml` (user's real settings) | ❌ |
| `/var/log/yourapp/` (logs) | `logs/` directory | ❌ |
| `/var/lib/yourapp/` (state) | `data/`, `db/`, `spool/` | ❌ |
| `/var/run/yourapp/` (sockets, PIDs) | `*.pid`, `*.sock` | ❌ |
| `/opt` (self-contained) | `vendor/` or `third_party/` | ✅ (pinned) |

**The one file that enforces the boundary:**

```gitignore
# .gitignore
config.toml
logs/
data/
*.pid
*.sock
```

That's your wall. The repo says "here's the code, here's a *template* for config, here's the schema." The runtime generates the `/var` stuff. The user edits the `/etc` stuff locally. Neither gets committed.

**The pattern in practice:**

```
yourapp/
├── yourapp.py              # /usr/bin — the code
├── schema.json             # /usr/share — the sheep shape (static)
├── config.example.toml     # /etc template — "copy this, edit it"
├── .gitignore              # the wall
├── README.md
└── (at runtime, generated:)
    ├── config.toml         # /etc — user's actual config
    ├── logs/               # /var/log
    └── data/               # /var/lib
```

**Why this matters for your paddock:**

The `schema.json` in the repo is the farmer's rule. It's public, it's in the code, anyone can read it. That's fine — you already established that the shape being public doesn't matter. What's *not* in the repo is the actual log data, the actual config, and the actual state. A wolf who clones your repo gets the shepherd's *blueprint*, not the *flock.*

The FHS philosophy in one sentence for a repo: **commit the code and the rules, never the data or the state.**


## Osaka78 says
im talking about the literal folder structure for the repo
surely no one has bin var etc?? or do they
and if they do are some folders read only??

## Ask Brave says
No. I was drawing an analogy. Repos don't use FHS names. The FHS layout is for the **installed** system, not the source.

**What repos actually look like:**

```
yourapp/
├── src/              # or just top-level .py files
├── tests/
├── docs/
├── config.example.toml
├── schema.json
├── .gitignore
├── README.md
└── pyproject.toml
```

That's it. No `bin/`, no `var/`, no `etc/`. The FHS mapping happens at **install time** (when `pip install` or `make install` puts files into `/usr/bin`, `/etc`, `/var`). The repo is the *source*, not the *destination.*

**The one exception:** `bin/` does appear in some repos (Python packaging, Node.js, Go's `cmd/`) to hold the entry-point scripts. But it means "the thing that gets installed to `/usr/bin`," not "this folder is read-only."

**"Read only" in a repo:**

Git doesn't enforce read-only on folders. There's no permission system. The boundary is purely **discipline + `.gitignore`.** You *could* commit `var/` if you wanted to. Nobody *should*, but nothing stops you. The "read-only" is social, not enforced.

The FHS analogy is about **intent** — "this is code, this is config, this is data" — not about literal folder names. The repo just uses whatever names the community convention gives it. `src/` is the code. `config.example.toml` is the config template. `.gitignore` says "don't commit the data." That's the whole mapping.


## Osaka
ive noticed some things about python, git, github pages and cloudflare> they seem to expect certain things in certain places

js and html and css seem to be self contained documents, but the others not so much

can you please elaborate on whatever is creating some dependancy or break point

## Brave
The breakpoint is: **does the artifact resolve its dependencies by content or by location?**

**Two worlds:**

| | HTML / JS / CSS | Python / Git / Cloudflare |
|---|---|---|
| Addressing model | **URL** (flat) | **Path** (hierarchical) |
| "Where am I?" | Doesn't matter. The document *is* the reference point. | Everything matters. The interpreter's location determines where `os` is. The repo's location IS the repo. The project root IS the project. |
| Dependencies | Other URLs, relative to the document | Other paths, relative to the filesystem hierarchy |
| Install step? | No. The file IS the final artifact. | Yes. Source → install → the *installed state* is the artifact. |
| "Home" | None. A `.html` file in `/tmp/` is identical to one in `/usr/share/`. | Yes. Git needs a working directory. Python needs `sys.path`. Cloudflare needs a project root with `wrangler.toml`. |

**The one sentence that explains it:**

> HTML/JS/CSS were designed for a **flat, URL-addressed world** where the document is the final artifact. Python/Git/Cloudflare were designed for a **hierarchical, filesystem-addressed world** where the installed state is the final artifact and the source is just the blueprint.

**Why that creates the "expects things in certain places" feeling:**

- **Python** says: "I need to find `os`. I'll walk `sys.path` (a list of directories) until I find a file called `os.py` or `os/`. If you moved me, `sys.path` breaks, and I can't find my dependencies."
- **Git** says: "I am the directory I'm in. My identity is `.git/` in *this* folder. If you move me without `.git/`, I'm not a repo anymore."
- **Cloudflare** says: "I need `wrangler.toml` in the project root. I need `dist/` to exist. I need `package.json` to tell me what to build. If any of those aren't in the expected place, I don't know what I am."
- **HTML** says: "I am this file. My dependencies are `<link href="...">` and `<script src="...">`. Those are URLs relative to *me*. I don't care if I'm in `/tmp/` or `/usr/share/` or a data: URI. I am complete."

**The deeper reason it's a breakpoint, not just a difference:**

The web was designed so that **the document is the unit of distribution.** You hand someone a `.html` file and it works. No install. No build. No "put it in the right folder." The document is self-referential — it knows what it needs by looking at its own content (the tags), not by looking at where it sits on a filesystem.

Python/Git/Cloudflare are **systems that manage a tree of files.** They're not a single document — they're a *structure.* And structures need a root, and the root is a location, and everything else is defined relative to that root. That's the dependency. That's the "expects things in certain places" feeling. It's not a bug. It's what it means to be a system rather than a document.

**The one exception that proves the rule:**

Node.js. JavaScript *in the browser* is a document (flat, URL-addressed, self-contained). JavaScript *in Node* is a system (hierarchical, path-addressed, needs `node_modules/` in the right place, needs `package.json`, needs `require()` to walk the filesystem). Same language. Two different worlds. The breakpoint is the runtime, not the language.

So: the "self-contained document" vs. "expects things in certain places" distinction is really **document vs. system**, and the thing that creates the dependency is **the need to resolve references against a filesystem hierarchy rather than against the document's own content.**
















