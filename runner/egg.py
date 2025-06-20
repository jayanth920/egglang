#!/usr/bin/env python3
import sys
import os

# Core Pointer
core_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'core'))
sys.path.insert(0, core_path)

from egg_interpreter import run_egglang # type: ignore # At runtime


def main():
    if len(sys.argv) != 2:
        print("Usage: egg.py <filename.egg>")
        sys.exit(1)
    filename = sys.argv[1]
    with open(filename, 'r') as f:
        code = f.read()
    run_egglang(code)

if __name__ == "__main__":
    main()
