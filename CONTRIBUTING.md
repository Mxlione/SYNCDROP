# Contributing

## The rule that shapes everything else

**SyncDrop has no runtime dependencies.** Not "few". None.

It has to work on a machine somebody has just sat down at, which may have no network to install
from, because working without the internet is the entire point. That is why the QR encoder is
written out in full in `src/syncdrop/qr/` rather than imported.

A pull request that adds an import of something from PyPI will be turned down, however good the
library is. CI has a job that checks this and it is not advisory.

Development tools are a different matter: ruff, mypy and pytest are all welcome, and so is any
library a test needs.

## Getting set up

```bash
python3 -m venv .venv
.venv/bin/pip install -e ".[dev]"
```

## The checks

The same four CI runs, which you can run in a few seconds:

```bash
.venv/bin/ruff check .          # lint
.venv/bin/ruff format .         # formatting
.venv/bin/mypy                  # types, strict
.venv/bin/pytest -q             # tests
```

And the one that matters most, with a bare interpreter:

```bash
PYTHONPATH=src python3 -m syncdrop
```

## The rules that matter

**Say why, not what.** The code says what it does. A comment that repeats it is noise. A comment
saying why a 480 kHz sample rate rather than 270, or why the second copy of the format
information splits seven and eight rather than eight and seven, is worth ten that narrate.

**A test that cannot fail is not a test.** `test_qr_against_another_encoder.py` compares every
module against a separate implementation because "it looked like a QR code" would have passed
while three real bugs were present.

**Be honest about what has not been verified.** SyncDrop has been run between two devices far
fewer times than it will be. Anything that has not been tried on real hardware, on a real
network, says so.

## Where to start

`TASKS.md` is the plan, in build order. Anything marked 🟢 is a good first contribution, and
anything marked 📱 needs a second device — which the maintainer often does not have two of.

The most useful thing you can do right now is **run it between two real devices and say what
happened**, especially on a network that is not a simple home router: a phone hotspot, a
university network with client isolation, a mesh, or Windows with its firewall on.
