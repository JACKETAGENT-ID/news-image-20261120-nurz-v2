#!/usr/bin/env python3
"""news-image-20261120 entry: copy the pre-rendered front page to /output."""
import os
import shutil

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")

os.makedirs(OUT, exist_ok=True)
src = os.path.join(HERE, "entry.png")
dst = os.path.join(OUT, "entry.png")
shutil.copyfile(src, dst)
# Deterministic output: the copy must be byte-identical to the source.
assert os.path.getsize(src) == os.path.getsize(dst), "copy size mismatch"
print("wrote", dst, os.path.getsize(dst), "bytes")
