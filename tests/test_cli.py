"""The command line.

What somebody sees in the first ten seconds, which is the only part of a tool most people ever
judge.
"""

from __future__ import annotations

import pytest

from syncdrop import __version__
from syncdrop.cli import main


class TestOutput:
    def test_the_address_is_printed(self, capsys: pytest.CaptureFixture[str]) -> None:
        assert main(["--no-qr"]) == 0
        printed = capsys.readouterr().out
        assert "http://" in printed
        assert ":8080" in printed or ":80" in printed

    def test_the_reason_for_the_address_is_shown(self, capsys: pytest.CaptureFixture[str]) -> None:
        """Somebody on a machine where the guess is wrong needs to see what it was based on."""
        main(["--no-qr"])
        assert "Using " in capsys.readouterr().out

    def test_a_qr_code_is_drawn_by_default(self, capsys: pytest.CaptureFixture[str]) -> None:
        main([])
        printed = capsys.readouterr().out
        # The half-block characters the symbol is drawn with.
        assert "█" in printed or "▀" in printed

    def test_the_qr_code_can_be_turned_off(self, capsys: pytest.CaptureFixture[str]) -> None:
        main(["--no-qr"])
        printed = capsys.readouterr().out
        assert "█" not in printed and "▀" not in printed

    def test_it_says_the_transfer_server_does_not_exist_yet(
        self, capsys: pytest.CaptureFixture[str]
    ) -> None:
        """Better than a program that looks like it is running and answers nothing."""
        main(["--no-qr"])
        assert "not written yet" in capsys.readouterr().out


class TestAddressListing:
    def test_every_address_is_listed_with_its_reasoning(
        self, capsys: pytest.CaptureFixture[str]
    ) -> None:
        assert main(["--addresses"]) == 0
        printed = capsys.readouterr().out
        assert "score" in printed
        assert "interface" in printed

    def test_loopback_appears_with_its_reason(self, capsys: pytest.CaptureFixture[str]) -> None:
        """It is never chosen, but hiding it makes the listing look wrong to anybody checking."""
        main(["--addresses"])
        assert "127.0.0.1" in capsys.readouterr().out


class TestFailures:
    def test_an_address_this_machine_does_not_have(
        self, capsys: pytest.CaptureFixture[str]
    ) -> None:
        assert main(["--address", "10.99.99.99", "--no-qr"]) == 1
        assert "cannot start" in capsys.readouterr().err

    def test_the_failure_says_what_addresses_there_are(
        self, capsys: pytest.CaptureFixture[str]
    ) -> None:
        main(["--address", "10.99.99.99", "--no-qr"])
        assert "It has:" in capsys.readouterr().err


class TestVersion:
    def test_the_version_is_the_package_version(self, capsys: pytest.CaptureFixture[str]) -> None:
        with pytest.raises(SystemExit) as exited:
            main(["--version"])
        assert exited.value.code == 0
        assert __version__ in capsys.readouterr().out
