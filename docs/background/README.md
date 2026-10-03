# Background

These documents came before SyncDrop took its current shape. They are kept because the thinking
in them is still useful, and removed from the front of the repository because parts of them are
now wrong.

| | |
|---|---|
| [`cahier-des-charges.md`](cahier-des-charges.md) | The original requirements, in French |
| [`ancien-mode-demploi.md`](ancien-mode-demploi.md) | Instructions for a version that no longer exists |
| [`design-des-ecrans.md`](design-des-ecrans.md) | The screen designs, which are still the plan |

## What changed, and why

The requirements call for a desktop application and a mobile application, built with Electron
and React Native, talking to each other over the local network. A first attempt went that way:
there is an Electron `.deb` and an Android `.apk` in the history, and `ancien-mode-demploi.md`
explains how to install them.

SyncDrop no longer ships either. One program runs on one device and serves a page; every other
device opens that page in a browser.

The reason is the install. Two applications means two things to download, two review processes,
two update paths, and a 118 MB APK to move a photo across a room. The browser on the far device
can already render a file picker, a progress bar and a drag target, and it is already
installed. Removing the applications removes most of the product's weight and nearly all of the
reason somebody would not try it.

What survives from the requirements, unchanged:

- Everything stays on the local network. No cloud, no account, no third party.
- Both directions, large files, progress, history.
- Pairing by QR code or PIN, with a session that expires.

What is dropped:

- Wi-Fi Direct and Bluetooth. A browser cannot reach either.
- The receive folder on the far device is wherever that browser downloads to, which is the
  browser's decision and not SyncDrop's.

The screen designs in `design-des-ecrans.md`, and the nine screens under `template/`, are still
the plan. They were drawn for a mobile application and translate to a web page almost directly,
because that is what they always were underneath.
