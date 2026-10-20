#!/usr/bin/env python3
"""envgap: find gaps between env vars used in code and declared in .env.example."""
import argparse
import json
import sys
from pathlib import Path

from scanner import scan_repo, read_declared


def main():
    p = argparse.ArgumentParser(
        description="Find env var gaps between code and .env.example")
    p.add_argument("path", nargs="?", default=".", help="repo path")
    p.add_argument("--declared", default=None,
                   help="declared env file (default auto)")
    p.add_argument("--json", action="store_true", help="JSON output")
    p.add_argument("--exit-code", action="store_true",
                   help="exit 1 if gaps found")
    args = p.parse_args()
    root = Path(args.path).resolve()
    used = scan_repo(root)
    declared = read_declared(root, args.declared)
    missing = sorted(used - declared)
    unused = sorted(declared - used)
    if args.json:
        print(json.dumps({"used": sorted(used), "declared": sorted(declared),
                          "missing": missing, "unused": unused}, indent=2))
    else:
        print(f"Scanned {root}")
        print(f"Env vars used in code: {len(used)}")
        print(f"Env vars declared: {len(declared)}")
        print()
        if missing:
            print("Used in code but NOT declared:")
            for v in missing:
                print(f"  - {v}")
        else:
            print("No missing declarations.")
        print()
        if unused:
            print("Declared but NOT used in code:")
            for v in unused:
                print(f"  - {v}")
        else:
            print("No unused declarations.")
    if args.exit_code and (missing or unused):
        sys.exit(1)


if __name__ == "__main__":
    main()
