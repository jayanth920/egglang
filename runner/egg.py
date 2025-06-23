#!/usr/bin/env python3
import sys
from egg_interpreter import run_egglang  # Local import from same folder

def main():
    if len(sys.argv) != 2:
        print("Usage: egg.py <filename.egg>")
        sys.exit(1)

    filename = sys.argv[1]
    try:
        with open(filename, 'r') as f:
            code = f.read()
        run_egglang(code)
    except FileNotFoundError:
        print(f"fragile: cannot find file '{filename}'")
        sys.exit(1)

if __name__ == "__main__":
    main()
