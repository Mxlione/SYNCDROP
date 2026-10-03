# 📂 SyncDrop

> Move files between your devices on one Wi-Fi network. Nothing to install on the far end,
> nothing hosted anywhere, nothing that leaves your network.

![Status](https://img.shields.io/badge/status-pre--alpha-orange)
![License](https://img.shields.io/badge/license-MIT-green)
![Python](https://img.shields.io/badge/python-3.11%20%7C%203.12-blue)
![Dependencies](https://img.shields.io/badge/runtime%20dependencies-none-brightgreen)

*Read this in [French](README.fr.md).*

---

## The idea

One device runs SyncDrop. It prints an address. Every other device opens that address in a
browser.

```
$ python3 -m syncdrop

  SyncDrop is ready.

      http://192.168.1.42:8080

  Open that on your phone. There is nothing to install.
  Ctrl-C to stop.
```

That is the whole product. The phone needs no application, no account, no app store, and no
internet connection. It needs a browser, which it already has.

```
   One device runs it                           Every other device
   ┌───────────────────────────┐                ┌──────────────────┐
   │   python3 -m syncdrop     │                │      browser     │
   │                           │                │                  │
   │   http://192.168.1.42:8080│←── Wi-Fi LAN ─→│  opens that      │
   │   [ QR code ]             │                │  address         │
   └───────────────────────────┘                └──────────────────┘

   No cloud. No account. No deployment. Nothing leaves the local network.
```

---

## Why not an application

Xender, AirDroid and the rest work, and they all ask both ends to install something. That is the
part worth removing.

- **No desktop application.** Electron ships 900 MB of `node_modules` to draw a window that the
  browser on the same machine already draws.
- **No mobile application.** An app store review, a 100 MB download and a permissions dialog, to
  move a photo across a room.
- **No cloud.** There is nothing to host, nothing to pay for, and no third party holding your
  files for the duration of the transfer.

What is left is a program small enough to read in an afternoon, and a web page.

---

## Install

There is nothing to install on the receiving device. Ever. On the one that runs it:

```bash
pip install syncdrop
syncdrop
```

Or from a checkout, with nothing but Python:

```bash
PYTHONPATH=src python3 -m syncdrop
```

A single downloadable `.py` file, with no checkout and no `pip`, is
[task 39](TASKS.md#phase-8--v10--documentation-and-packaging) and does not exist yet.

SyncDrop has **no runtime dependencies**. Everything it needs is in the Python standard library,
including the QR code encoder. That is deliberate: it has to work on a machine with no network
to install from, because working without the internet is the entire point.

---

## Status

Early development. Nothing is released yet.

| | |
|---|---|
| Choosing the right network address | 🟢 works |
| QR code | 🟢 works |
| Sending and receiving | ⬜ not started |
| Pairing | ⬜ not started |
| The web interface | ⬜ not started |

**On a machine with six addresses, five of them wrong.** The first thing SyncDrop does is decide
which address to print, and it is the first thing that can silently fail: a laptop with Docker,
libvirt and LXC installed has six IPv4 addresses, and exactly one of them a phone can reach.
Print any of the other five and the page simply never loads, with no error to explain why.

SyncDrop scores every address it finds and says what it based the choice on:

```
 score  interface          address          why
   140  wlp0s20f3          192.168.226.126  the route the system itself would take, named like real hardware
     0  lo                 127.0.0.1        loopback, reaches nothing but this machine
  -135  docker0            172.17.0.1       named like a virtual interface, in a range virtualisation hands itself, …
  -135  virbr0             192.168.122.1    named like a virtual interface, in a range virtualisation hands itself, …
```

---

## Roadmap

- [ ] **v0.1** — Choosing the right address, and the QR code
- [ ] **v0.2** — Sending and receiving, with large files
- [ ] **v0.3** — Pairing: QR code, PIN, sessions
- [ ] **v0.4** — The web interface
- [ ] **v0.5** — Live progress, several devices at once
- [ ] **v0.6** — Folders, queue, resume, shared clipboard
- [ ] **v1.0** — Documentation, packaging, a single downloadable file

The task breakdown lives in [TASKS.md](TASKS.md).

---

## Scope of use

SyncDrop moves your own files between your own devices on a network you control. It has no
authentication beyond a session token, so anybody on the same network who has the address can
use it while it runs. Do not leave it running on a network you do not trust.

---

## License

MIT — see [LICENSE](LICENSE).
