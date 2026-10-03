# SyncDrop task breakdown

How SyncDrop gets built, in order. The [roadmap](README.md#roadmap) says what each version
delivers; this says how.

**Legend** — ✅ done · 🚧 in progress · ⬜ not started · 🟢 good first issue · 📱 needs a second
device to verify

---

## The shape of the thing

One program runs on one device. It serves a page on the local network. Every other device opens
that address in a browser.

```
   PC (or phone, or a Raspberry Pi)              Any other device
   ┌──────────────────────────┐                  ┌──────────────┐
   │  python3 -m syncdrop     │                  │   browser    │
   │                          │                  │              │
   │  http://192.168.1.42:8080│ ←── Wi-Fi LAN ──→│  opens that  │
   │  [QR code in terminal]   │                  │  address     │
   └──────────────────────────┘                  └──────────────┘

   Nothing is hosted anywhere. No cloud, no account, no deployment.
   Nothing leaves the local network.
```

The second device installs nothing. That is the whole idea, and it is why there is no desktop
application and no mobile application.

---

## Phase 0 — Publishable repository

| # | Status | Task | Detail |
|---|---|---|---|
| 1 | ✅ | README | English, with `README.fr.md` kept in sync |
| 2 | ✅ | LICENSE | MIT, Mxlione |
| 3 | ✅ | `pyproject.toml` | ruff, mypy strict, pytest. **No runtime dependencies** |
| 4 | ✅ | CI | Lint, types, tests on 3.11 and 3.12 |
| 5 | 🚧 | Contribution guide | CONTRIBUTING.md done; issue and PR templates still to write |

## Phase 1 — v0.1 · Finding the right address

The first real problem, and the one that decides whether anything works at all. This machine has
six IPv4 addresses: the Wi-Fi, a libvirt bridge, an LXC bridge and three Docker networks.
Printing the wrong one gives a URL that nothing can reach.

| # | Status | Task | Detail |
|---|---|---|---|
| 6 | ✅ | Interface enumeration | Without `ifconfig`, `ip` or any dependency |
| 7 | ✅ | Scoring | Rank candidates: real Wi-Fi/Ethernet above virtual bridges |
| 8 | ✅ | Reachability check | The address a client would actually route to |
| 9 | ✅ | Port selection | A default, a fallback when taken, and `--port` |

## Phase 2 — v0.2 · The QR code

| # | Status | Task | Detail |
|---|---|---|---|
| 10 | ✅ | QR encoding | Model 2, byte mode, pure Python, no dependency |
| 11 | ✅ | Terminal rendering | Half-block characters, readable by a phone camera |
| 12 | ✅ | SVG rendering | The same matrix, for the web page |
| 13 | ✅ | Verification | Compared against an independent encoder across many inputs |

## Phase 3 — v0.3 · Sending and receiving

| # | Status | Task | Detail |
|---|---|---|---|
| 14 | ⬜ | HTTP core | Threaded, streaming, no framework |
| 15 | ⬜ | Upload | Streamed to disk, never held in memory. 500 MB must not use 500 MB |
| 16 | ⬜ | Download | With range requests, so a phone can resume |
| 17 | ⬜ | Safe filenames | A name from the network is hostile until proven otherwise |
| 18 | ⬜ | Integrity | Checksum each transfer, and say when one does not match |

## Phase 4 — v0.4 · Pairing

| # | Status | Task | Detail |
|---|---|---|---|
| 19 | ⬜ | Session token | In the URL the QR code carries |
| 20 | ⬜ | PIN | Six digits, for typing when a camera will not scan |
| 21 | ⬜ | Expiry | Sessions end, by time and by inactivity |
| 22 | ⬜ | Approval | A new device asks before it can do anything |

## Phase 5 — v0.5 · The interface

Built from the designs in `template/`, which already cover nine screens.

| # | Status | Task | Detail |
|---|---|---|---|
| 23 | ⬜ | Design tokens | From `template/proximity_mesh/DESIGN.md` |
| 24 | ⬜ | Send | Drag and drop on a desktop, the file picker on a phone |
| 25 | ⬜ | Receive | The list of what is waiting, and getting it |
| 26 | ⬜ | Progress | Speed, time remaining, per file |
| 27 | ⬜ | History | What has been transferred |
| 28 | ⬜ | Settings | Name, receive folder, trusted devices |
| 29 | ⬜ | No framework | Plain HTML, CSS and JavaScript, so a phone loads it instantly |

## Phase 6 — v0.6 · Live

| # | Status | Task | Detail |
|---|---|---|---|
| 30 | ⬜ | Server-sent events | Progress and device list, pushed |
| 31 | ⬜ | Multi-device | Several phones at once, each with its own session |
| 32 | ⬜ | Notifications | When a transfer finishes |

## Phase 7 — v0.7 · The things that make it usable

| # | Status | Task | Detail |
|---|---|---|---|
| 33 | ⬜ | Folders | A whole directory, preserving its shape |
| 34 | ⬜ | Queue | Several files, one after another |
| 35 | ⬜ | Resume | An interrupted transfer carries on |
| 36 | ⬜ | Shared clipboard | Copy here, paste there |
| 37 | ⬜ | Encryption | HTTPS on the LAN, and what that costs |

## Phase 8 — v1.0 · Documentation and packaging

| # | Status | Task | Detail |
|---|---|---|---|
| 38 | ⬜ | Documentation site | Install, use, protocol, architecture, contributing |
| 39 | ⬜ | Single file | One `.py` anybody can download and run |
| 40 | ⬜ | Packaging | PyPI wheel, `.deb`, a systemd unit for a Raspberry Pi |
| 41 | ⬜ | Release | Changelog, workflow, tags |

## Phase 9 — Community

| # | Status | Task | Detail |
|---|---|---|---|
| 42 | ⬜ | Starter issues | With the files and the acceptance criteria |
| 43 | ⬜ | Labels and milestones | |
| 44 | ⬜ | Showcase | Generated screenshots, as OpenWave does |
| 45 | ⬜ | Announcement | Drafted here, posted by the maintainer |

---

## What this deliberately is not

- **Not a cloud service.** Nothing is hosted. There is no account and no server to pay for.
- **Not a desktop application.** Electron is 900 MB of node_modules to draw a window that a
  browser already draws.
- **Not a mobile application.** An app store review to move a photo across a room is absurd.
- **Not a sync tool.** It does not watch folders or run in the background. You ask, it moves.
