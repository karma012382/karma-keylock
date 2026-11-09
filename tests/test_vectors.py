# SPDX-License-Identifier: Apache-2.0
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE))
import keylock  # noqa: E402


def main():
    bad = 0
    with open(os.path.join(HERE, "vectors.csv")) as fh:
        for line in fh:
            vals = [int(x) for x in line.strip().split(",")]
            if keylock.public_value(vals[0]) != vals[1:]:
                bad += 1
    print("ok" if bad == 0 else "%d failed" % bad)
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
