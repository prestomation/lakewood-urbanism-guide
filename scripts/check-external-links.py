#!/usr/bin/env python3
"""Check external links in all Markdown content files."""

import os
import re
import sys
import urllib.request
import urllib.error

CONTENT_DIR = "content"
TIMEOUT = 30
LINK_PATTERN = re.compile(r'\[([^\]]*)\]\((https?://[^\)]+)\)')

def find_markdown_files(directory):
    """Find all .md files in directory tree."""
    md_files = []
    for root, _, files in os.walk(directory):
        for f in files:
            if f.endswith(".md"):
                md_files.append(os.path.join(root, f))
    return md_files

def extract_links(filepath):
    """Extract external URLs from a Markdown file."""
    links = []
    with open(filepath, "r") as f:
        for line_num, line in enumerate(f, 1):
            for match in LINK_PATTERN.finditer(line):
                links.append((match.group(2), line_num))
    return links

def check_url(url):
    """Check if a URL is reachable."""
    try:
        req = urllib.request.Request(url, method="HEAD")
        req.add_header("User-Agent", "LinkChecker/1.0")
        with urllib.request.urlopen(req, timeout=TIMEOUT) as resp:
            return resp.status < 400
    except (urllib.error.URLError, urllib.error.HTTPError, OSError):
        try:
            req = urllib.request.Request(url, method="GET")
            req.add_header("User-Agent", "LinkChecker/1.0")
            with urllib.request.urlopen(req, timeout=TIMEOUT) as resp:
                return resp.status < 400
        except Exception:
            return False

def main():
    md_files = find_markdown_files(CONTENT_DIR)
    broken = []
    checked = 0

    for filepath in md_files:
        links = extract_links(filepath)
        for url, line_num in links:
            checked += 1
            if not check_url(url):
                broken.append((filepath, line_num, url))
                print(f"  BROKEN: {filepath}:{line_num} -> {url}")
            else:
                print(f"  OK: {url}")

    print(f"\nChecked {checked} links in {len(md_files)} files")
    if broken:
        print(f"Found {len(broken)} broken link(s):")
        for filepath, line_num, url in broken:
            print(f"  {filepath}:{line_num} -> {url}")
        sys.exit(1)
    else:
        print("All links valid!")
        sys.exit(0)

if __name__ == "__main__":
    main()
