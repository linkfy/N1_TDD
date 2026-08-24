#!/usr/bin/env sh

# Run NES with PyPy through uv.
# Usage:
# 	sh launcher.sh
# or:
# 	chmod +x launcher.sh
#	./launcher.sh

uv run --python pypy python main.py
