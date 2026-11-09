#!/usr/bin/env python3
# Copyright 2026 KARMA (KΛRMA)
# SPDX-License-Identifier: Apache-2.0
"""KΛRMA Key Lock (pure Python, no dependencies)."""
import hashlib
import sys

N = 256
H = N // 2
MASK = (1 << 64) - 1
KEY_BITS = 512


def parse_key(text):
    text = text.strip().lower()
    k = int(text, 16) if text.startswith("0x") else int(text)
    if not 0 <= k < (1 << KEY_BITS):
        raise ValueError("key must be an integer in [0, 2^512)")
    return k


def _rows(f):
    out = []
    for s in range(N):
        c0 = 2 * (s % H)
        flip = ((s >> 7) & 1) ^ ((f >> s) & 1)
        out.append(((c0, 1), (c0 + 1, -1 if flip else 1)))
    return out


def _charpoly(f):
    rows = _rows(f)
    p = [1]
    for r in range(N):
        a = 0
        R = []
        for c, v in rows[r]:
            if c == r:
                a = v
            elif c < r:
                R.append((c, v))
        S = [0] * r
        for i in (r >> 1, (r >> 1) + H):
            if i < r:
                for c, v in rows[i]:
                    if c == r:
                        S[i] = v
        C = [1, (-a) & MASK]
        vec = S
        for _ in range(r):
            C.append((-sum(v * vec[c] for c, v in R)) & MASK)
            nxt = [0] * r
            for i in range(r):
                acc = 0
                for c, v in rows[i]:
                    if c < r:
                        acc += v * vec[c]
                nxt[i] = acc & MASK
            vec = nxt
        q = [0] * (r + 2)
        for i in range(r + 2):
            acc = 0
            for j in range(max(0, i - (len(C) - 1)), min(i, r) + 1):
                acc += C[i - j] * p[j]
            q[i] = acc & MASK
        p = q
    return p


def _lock(f):
    e = _charpoly(f)
    return [(e[j] >> 16) & 0xFFFF for j in range(1, N + 1)]


def public_value(key):
    d = hashlib.sha3_512(key.to_bytes(KEY_BITS // 8, "big")).digest()
    return _lock(int.from_bytes(d[:32], "big")) + _lock(int.from_bytes(d[32:], "big"))


def main(argv):
    if len(argv) >= 2 and argv[0] == "public":
        print(",".join(map(str, public_value(parse_key(argv[1])))))
        return 0
    if len(argv) >= 3 and argv[0] == "check":
        want = [int(x) for x in open(argv[2]).read().replace("\n", ",").split(",") if x.strip()]
        ok = public_value(parse_key(argv[1])) == want
        print("OPEN" if ok else "LOCKED")
        return 0 if ok else 1
    print("usage: keylock.py public KEY | check KEY PUBLIC_FILE   (KEY: 512-bit integer, decimal or 0x-hex)")
    return 2


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
