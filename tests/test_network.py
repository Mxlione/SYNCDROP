"""Choosing which address to print.

Most of these drive the scoring directly with invented interface lists, because the interesting
cases are machines this one is not: a laptop behind a VPN, a server with no Wi-Fi, a phone
hotspot. Only the few marked ``network`` touch this machine's real interfaces.
"""

from __future__ import annotations

import socket

import pytest

from syncdrop.network import (
    DEFAULT_PORT,
    Candidate,
    _score,
    candidates,
    choose,
    default_route_address,
    find_port,
)


class TestScoring:
    """What each signal is worth, and in which direction."""

    def test_the_default_route_wins(self) -> None:
        """The system's own routing decision outweighs a suspicious-looking name."""
        wifi, _ = _score("192.168.1.42", "wlp0s20f3", "192.168.1.42")
        docker, _ = _score("172.17.0.1", "docker0", "192.168.1.42")
        assert wifi > docker

    def test_loopback_is_never_usable(self) -> None:
        """127.0.0.1 reaches this machine and nothing else, whatever else is true of it."""
        score, why = _score("127.0.0.1", "lo", "127.0.0.1")
        assert score == 0
        assert "loopback" in why

    def test_a_virtual_interface_is_demoted_even_on_a_home_range(self) -> None:
        """libvirt sits on 192.168.122.0/24, which looks exactly like somebody's home network.

        The address alone cannot tell them apart. The interface name can.
        """
        home, _ = _score("192.168.1.50", "wlan0", None)
        libvirt, _ = _score("192.168.122.1", "virbr0", None)
        assert home > libvirt

    def test_an_unknown_interface_name_is_neither_rewarded_nor_punished(self) -> None:
        """A name this code has never seen should not be guessed at."""
        score, _ = _score("192.168.1.50", "qqq0", None)
        assert score == 0

    @pytest.mark.parametrize(
        "address",
        ["172.17.0.1", "172.22.0.1", "10.0.3.1", "192.168.122.1"],
    )
    def test_ranges_virtualisation_uses_are_demoted(self, address: str) -> None:
        score, why = _score(address, "unknown0", None)
        assert score < 0
        assert "virtualisation" in why or "gateway" in why

    def test_every_score_carries_a_reason(self) -> None:
        """A choice nobody can question is a choice nobody can correct."""
        for address, interface in [
            ("192.168.1.42", "wlan0"),
            ("172.17.0.1", "docker0"),
            ("127.0.0.1", "lo"),
            ("8.8.8.8", "eth0"),
        ]:
            _, why = _score(address, interface, None)
            assert why.strip(), f"{interface} got no reason"


class TestChoosing:
    """Picking one, and failing usefully when there is none."""

    def test_an_address_that_is_not_here_is_refused(self) -> None:
        """A typo should fail now, not later when a phone cannot connect."""
        with pytest.raises(LookupError, match="no address"):
            choose("10.99.99.99")

    def test_the_refusal_lists_what_there_is(self) -> None:
        """Being told the answer is wrong is only half of it."""
        with pytest.raises(LookupError) as raised:
            choose("10.99.99.99")
        assert "It has:" in str(raised.value)

    def test_candidates_come_back_in_a_stable_order(self) -> None:
        """A list that reshuffles between runs makes a bug report useless."""
        first = [one.address for one in candidates()]
        second = [one.address for one in candidates()]
        assert first == second

    def test_candidates_are_sorted_best_first(self) -> None:
        scores = [one.score for one in candidates()]
        assert scores == sorted(scores, reverse=True)


class TestCandidate:
    def test_a_negative_score_is_not_usable(self) -> None:
        assert not Candidate("172.17.0.1", "docker0", -135, "virtual").is_usable

    def test_zero_is_not_usable_either(self) -> None:
        """Nothing known in its favour is not the same as being fine."""
        assert not Candidate("127.0.0.1", "lo", 0, "loopback").is_usable


@pytest.mark.network
class TestThisMachine:
    """The few things that need this machine's real interfaces."""

    def test_the_default_route_is_not_loopback(self) -> None:
        """The probe exists to find an address another device could use."""
        address = default_route_address()
        assert address is None or not address.startswith("127.")

    def test_the_probe_sends_nothing(self) -> None:
        """A UDP connect fixes the peer and transmits nothing.

        This matters more than it looks: SyncDrop runs on networks with no internet, and a probe
        that actually tried to reach the address would hang rather than answer.
        """
        # TEST-NET-2 is reserved and never routed, so a reply would mean something is wrong.
        assert default_route_address() != "198.51.100.1"

    def test_a_chosen_address_is_one_this_machine_has(self) -> None:
        try:
            chosen = choose()
        except LookupError:
            pytest.skip("this machine has no usable address")
        assert chosen.address in {one.address for one in candidates()}

    def test_the_port_found_can_be_bound(self) -> None:
        """The whole point of the function."""
        port = find_port()
        with socket.socket() as held:
            held.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            held.bind(("", port))

    def test_a_taken_port_is_stepped_over(self) -> None:
        with socket.socket() as taken:
            taken.bind(("", 0))
            busy = taken.getsockname()[1]
            taken.listen(1)
            assert find_port(busy) != busy

    def test_giving_up_says_which_ports_were_tried(self) -> None:
        held = []
        try:
            for offset in range(3):
                keep = socket.socket()
                try:
                    keep.bind(("", DEFAULT_PORT + 40000 + offset))
                    keep.listen(1)
                    held.append(keep)
                except OSError:
                    keep.close()
                    pytest.skip("could not take a contiguous block of ports")
            with pytest.raises(OSError, match="are all taken"):
                find_port(DEFAULT_PORT + 40000, attempts=3)
        finally:
            for keep in held:
                keep.close()
