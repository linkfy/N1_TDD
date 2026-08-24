@echo off

REM Run NES with PyPy through uv.
REM Usage:
REM		launcher.cmd

uv run --python pypy python main.py
