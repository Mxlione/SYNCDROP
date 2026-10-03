"""Lets SyncDrop run with ``python3 -m syncdrop``, with nothing installed."""

from __future__ import annotations

import sys

from syncdrop.cli import main

if __name__ == "__main__":
    sys.exit(main())
