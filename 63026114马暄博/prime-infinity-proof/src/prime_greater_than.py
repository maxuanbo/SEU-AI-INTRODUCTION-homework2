#!/usr/bin/env python3
"""Find a prime p with p > n, and demonstrate Euclid's construction.

The primality test is exact trial division: it checks divisors up to
floor(sqrt(c)). This is deliberately simple and mirrors the proof's
elementary character. It is intended for the report's small/medium test
values rather than for cryptographic-size inputs.
"""

from __future__ import annotations

import argparse
from math import isqrt, prod


def is_prime(candidate: int) -> bool:
    """Return True exactly when candidate is prime."""
    if candidate < 2:
        return False
    if candidate in (2, 3):
        return True
    if candidate % 2 == 0 or candidate % 3 == 0:
        return False

    divisor = 5
    while divisor <= isqrt(candidate):
        if candidate % divisor == 0 or candidate % (divisor + 2) == 0:
            return False
        divisor += 6
    return True


def primes_up_to(n: int) -> list[int]:
    """Return every prime <= n, in increasing order (sieve of Eratosthenes)."""
    if n < 2:
        return []
    sieve = bytearray(b"\x01") * (n + 1)
    sieve[0:2] = b"\x00\x00"
    for p in range(2, isqrt(n) + 1):
        if sieve[p]:
            start = p * p
            sieve[start : n + 1 : p] = b"\x00" * (((n - start) // p) + 1)
    return [value for value in range(2, n + 1) if sieve[value]]


def next_prime(n: int) -> int:
    """Return the least prime strictly greater than n."""
    candidate = n + 1
    if candidate <= 2:
        return 2
    if candidate % 2 == 0:
        candidate += 1
    while not is_prime(candidate):
        candidate += 2
    return candidate


def smallest_prime_factor(value: int) -> int:
    """Return the smallest prime factor of value > 1."""
    if value < 2:
        raise ValueError("value must be greater than 1")
    if value % 2 == 0:
        return 2
    divisor = 3
    while divisor * divisor <= value:
        if value % divisor == 0:
            return divisor
        divisor += 2
    return value


def euclid_construction(n: int) -> tuple[list[int], int, int]:
    """Build N = product of primes <= n, plus 1, and extract a prime factor.

    Only use this demo for modest n: factoring N can be expensive because N
    grows like the primorial of n.
    """
    primes = primes_up_to(n)
    if not primes:
        return [], 2, 2
    product = prod(primes)
    witness = product + 1
    return primes, witness, smallest_prime_factor(witness)


def verify(n: int) -> dict[str, object]:
    """Run the theorem's computational check for one input."""
    p = next_prime(n)
    return {
        "n": n,
        "p": p,
        "gap": p - n,
        "is_prime": is_prime(p),
        "greater_than_n": p > n,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("n", nargs="?", type=int, default=100, help="natural number n")
    args = parser.parse_args()

    if args.n < 0:
        parser.error("n must be a natural number (n >= 0)")

    result = verify(args.n)
    print("=== Direct search ===")
    print(f"n                = {result['n']}")
    print(f"p                = {result['p']}")
    print(f"p - n            = {result['gap']}")
    print(f"is_prime(p)      = {result['is_prime']}")
    print(f"p > n            = {result['greater_than_n']}")

    print("\n=== Euclid construction for n = 10 ===")
    primes, witness, factor = euclid_construction(10)
    print(f"primes <= 10     = {primes}")
    print(f"N                = {' * '.join(map(str, primes))} + 1 = {witness}")
    print(f"N mod p_i        = {[witness % p for p in primes]}")
    print(f"prime factor q   = {factor}")
    print(f"q > 10           = {factor > 10}")

    print("\n=== Regression checks ===")
    cases = [0, 1, 2, 3, 10, 100, 1000, 10_000, 1_000_000]
    for n in cases:
        p = next_prime(n)
        assert is_prime(p), (n, p)
        assert p > n, (n, p)
        print(f"n={n:>7}  p={p:>8}  gap={p - n:>3}  verified")
    print("ALL CHECKS PASSED")


if __name__ == "__main__":
    main()
