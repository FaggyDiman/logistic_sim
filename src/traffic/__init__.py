"""
Simple traffic tracking for roads between towns.
Key is frozenset((town_a, town_b)) where town objects are used (they are hashable by id).
Provides increment/get utilities and a global TRAFFIC dict.
"""
from __future__ import annotations
from typing import Dict, Tuple

TRAFFIC: Dict[frozenset, int] = {}


def _key(a, b):
    return frozenset((a, b))


def increment_traffic(a, b, amount: int = 1) -> None:
    """Increment traffic counter for an undirected edge between towns a and b."""
    if amount <= 0:
        return
    k = _key(a, b)
    TRAFFIC[k] = TRAFFIC.get(k, 0) + int(amount)


def get_traffic(a, b) -> int:
    k = _key(a, b)
    return TRAFFIC.get(k, 0)


def get_all_traffic():
    return TRAFFIC


def clear_traffic():
    TRAFFIC.clear()
