#!/usr/bin/env python3
"""Validate that timeline.yaml entries are in reverse chronological order."""

import sys
import yaml

def main():
    with open("data/timeline.yaml", "r") as f:
        entries = yaml.safe_load(f)

    if not entries:
        print("WARNING: timeline.yaml is empty")
        sys.exit(0)

    errors = []
    for i in range(len(entries) - 1):
        current_year = entries[i]["year"]
        next_year = entries[i + 1]["year"]
        if current_year < next_year:
            errors.append(
                f"Entry {i} (year {current_year}) is before entry {i+1} "
                f"(year {next_year}) — must be reverse chronological"
            )

    if errors:
        print("Timeline validation FAILED:")
        for error in errors:
            print(f"  - {error}")
        sys.exit(1)
    else:
        print(f"Timeline validation passed: {len(entries)} entries in correct order")
        sys.exit(0)

if __name__ == "__main__":
    main()
