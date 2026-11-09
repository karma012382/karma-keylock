# KΛRMA Key Lock

A key lock. One dependency-free Python file.

> Not yet independently audited.

## How it works

1. A 512-bit key is stretched with SHA3-512 into two 256-bit halves.
2. Each half defines a sparse 256 x 256 matrix.
3. The public value is computed from the characteristic polynomials of both matrices.
4. To open, the public value is recomputed from the key and compared.

## Use

```
python keylock.py public KEY            # print the public value
python keylock.py check KEY public.txt  # OPEN / LOCKED
python tests/test_vectors.py            # self-test
```

`KEY`: a 512-bit integer, decimal or `0x` hex.

## License

Apache-2.0
