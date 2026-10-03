"""Finding the address to put on the screen.

This is the first thing SyncDrop does and the first thing that can go wrong. A machine has more
addresses than people expect: this one has six, of which exactly one is reachable from a phone
on the same Wi-Fi.

    192.168.226.126   the Wi-Fi                 ← the only useful one
    192.168.122.1     libvirt's virtual bridge
    10.0.3.1          an LXC bridge
    172.17.0.1        Docker
    172.27.0.1        Docker
    172.22.0.1        Docker

Printing any of the other five gives a URL that a phone cannot reach, with no error to explain
why: the page simply never loads. So the choice is made by scoring every candidate and showing
the reasoning, rather than by taking the first one and hoping.

Nothing here shells out to ``ip`` or ``ifconfig``. Those are absent on Windows, differ between
Linux distributions, and change their output between versions.
"""

from __future__ import annotations

import ipaddress
import socket
from dataclasses import dataclass
from typing import Final

#: Interface name prefixes that belong to virtualisation rather than to a network a phone is on.
#: A Docker bridge is a real interface with a real address that routes nowhere useful.
VIRTUAL_PREFIXES: Final = (
    "docker",
    "br-",
    "virbr",
    "vmnet",
    "vboxnet",
    "lxcbr",
    "lxdbr",
    "veth",
    "tun",
    "tap",
    "wg",
    "zt",
    "utun",
    "ham",
)

#: Address ranges that virtualisation hands itself, in rough order of how suspicious they are.
#: These are ordinary private ranges, so this cannot be a rule on its own — a real home network
#: uses 192.168.0.0/16, and plenty use 10.0.0.0/8. It is one signal among several.
SUSPICIOUS_RANGES: Final = (
    ipaddress.ip_network("172.16.0.0/12"),  # Docker's default pool
    ipaddress.ip_network("192.168.122.0/24"),  # libvirt
    ipaddress.ip_network("10.0.3.0/24"),  # LXC
)

#: A host part of 1 usually means this machine is the gateway, which is what a virtual bridge is
#: and what a laptop on somebody's Wi-Fi is not.
GATEWAY_HOST_PART: Final = 1


@dataclass(frozen=True, slots=True)
class Candidate:
    """One address this machine could advertise, and what is known about it."""

    address: str
    interface: str
    score: int
    why: str

    @property
    def is_usable(self) -> bool:
        """Whether this is worth showing to somebody at all."""
        return self.score > 0


def default_route_address() -> str | None:
    """The address this machine would use to reach the rest of the network.

    Opens a UDP socket towards a public address and asks the kernel which of this machine's
    addresses it picked. Nothing is sent: a UDP connect only fixes the socket's peer, so this
    works with no network access at all, which matters because SyncDrop's whole point is working
    without the internet.

    This is the single most reliable signal available, because it is the operating system's own
    routing decision rather than a guess. It is not the whole answer: on a machine behind a VPN
    it returns the VPN's address, which is correct for the internet and wrong for the phone in
    the room.
    """
    probe = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        probe.connect(("198.51.100.1", 9))  # TEST-NET-2: reserved, never routed, never reached.
        address = str(probe.getsockname()[0])
    except OSError:
        return None
    finally:
        probe.close()
    return None if address.startswith("127.") else address


def _linux_interfaces() -> dict[str, str]:
    """Every interface's IPv4 address, by interface name, on Linux.

    Uses SIOCGIFADDR, the same ioctl ``ifconfig`` uses, so it needs no external command and no
    dependency. Returns nothing at all on a platform without it rather than raising, because the
    caller has a portable fallback and a missing interface list is not a reason to fail.
    """
    try:
        import fcntl
        import struct
    except ImportError:  # pragma: no cover - Windows has no fcntl
        return {}

    SIOCGIFADDR = 0x8915
    found: dict[str, str] = {}
    probe = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        for _, name in socket.if_nameindex():
            request = struct.pack("256s", name[:15].encode())
            try:
                answer = fcntl.ioctl(probe.fileno(), SIOCGIFADDR, request)
            except OSError:
                # An interface that is down, or has no IPv4 address. Both are ordinary.
                continue
            # The reply is an ifreq: the name, then a sockaddr_in whose address is at offset 20.
            found[name] = socket.inet_ntoa(answer[20:24])
    except OSError:
        return {}
    finally:
        probe.close()
    return found


#: Interface name prefixes that are ordinarily real hardware somebody's phone can reach.
PHYSICAL_PREFIXES: Final = ("wl", "en", "eth", "wlan", "wifi", "em", "eno", "ens", "enp", "ww")

# What each signal is worth. Being the operating system's own routing choice outweighs
# everything else, because it is a decision rather than a guess; the rest only break ties and
# demote the obviously wrong.
SCORE_DEFAULT_ROUTE: Final = 100
SCORE_PHYSICAL_NAME: Final = 40
PENALTY_VIRTUAL_NAME: Final = -80
PENALTY_SUSPICIOUS_RANGE: Final = -30
PENALTY_GATEWAY_HOST: Final = -25


def _score(address: str, interface: str, default_route: str | None) -> tuple[int, str]:
    """Rate one address, and say in words why."""
    parsed = ipaddress.ip_address(address)
    points = 0
    reasons: list[str] = []

    if parsed.is_loopback:
        return 0, "loopback, reaches nothing but this machine"

    if address == default_route:
        points += SCORE_DEFAULT_ROUTE
        reasons.append("the route the system itself would take")

    lowered = interface.lower()
    if lowered.startswith(VIRTUAL_PREFIXES):
        points += PENALTY_VIRTUAL_NAME
        reasons.append("named like a virtual interface")
    elif lowered.startswith(PHYSICAL_PREFIXES):
        points += SCORE_PHYSICAL_NAME
        reasons.append("named like real hardware")

    if any(parsed in network for network in SUSPICIOUS_RANGES):
        points += PENALTY_SUSPICIOUS_RANGE
        reasons.append("in a range virtualisation hands itself")

    if int(parsed) & 0xFF == GATEWAY_HOST_PART:
        points += PENALTY_GATEWAY_HOST
        reasons.append("host part is 1, so this machine is probably the gateway")

    if not parsed.is_private:
        reasons.append("public address")

    return points, ", ".join(reasons) or "nothing for or against it"


def candidates() -> list[Candidate]:
    """Every address this machine could advertise, best first.

    Falls back to the default route alone when interfaces cannot be enumerated, which is what
    happens on a platform without SIOCGIFADDR. One correct answer with no explanation beats a
    crash.
    """
    default_route = default_route_address()
    interfaces = _linux_interfaces()

    if not interfaces and default_route is not None:
        interfaces = {"?": default_route}

    found = [
        Candidate(address, name, *_score(address, name, default_route))
        for name, address in interfaces.items()
    ]
    # Sorted by score, then by address so that two equally good candidates always come back in
    # the same order. A list that reshuffles between runs makes a bug report useless.
    return sorted(found, key=lambda one: (-one.score, one.address))


def choose(preferred: str | None = None) -> Candidate:
    """Pick the address to show, or explain why there is none.

    ``preferred`` overrides the choice, for the machine where the scoring gets it wrong. It is
    checked against what was found: a typo in an address somebody typed should fail here, not
    later when a phone cannot connect and nobody knows why.
    """
    found = candidates()

    if preferred is not None:
        for one in found:
            if one.address == preferred:
                return Candidate(one.address, one.interface, one.score, "chosen by hand")
        known = ", ".join(one.address for one in found) or "none"
        raise LookupError(f"this machine has no address {preferred}. It has: {known}")

    usable = [one for one in found if one.is_usable]
    if not usable:
        raise LookupError(
            "no address on this machine looks reachable from another device. "
            "Connect to a Wi-Fi network, or pass one with --address."
        )
    return usable[0]


#: The port SyncDrop asks for first. Short enough to type on a phone keyboard, and high enough
#: to need no privileges.
DEFAULT_PORT: Final = 8080

#: How many ports above the default to try before giving up.
PORT_ATTEMPTS: Final = 20


def find_port(preferred: int = DEFAULT_PORT, attempts: int = PORT_ATTEMPTS) -> int:
    """Find a port that can actually be bound, starting from the one asked for.

    Binding is the only way to know. Asking whether a port is free and then binding it is a race
    somebody loses eventually, so this binds, closes, and hands back the number — still a race,
    but a far shorter one, and the alternative is failing on a port that was free a moment ago.

    An explicit choice is not second-guessed: if somebody passes ``--port 9000`` and 9000 is
    taken, they want to hear about 9000 rather than be moved quietly to 9001.
    """
    for offset in range(attempts):
        port = preferred + offset
        probe = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        probe.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        try:
            probe.bind(("", port))
        except OSError:
            continue
        finally:
            probe.close()
        return port
    raise OSError(
        f"ports {preferred} to {preferred + attempts - 1} are all taken. "
        f"Free one, or choose another with --port."
    )
