#!/usr/bin/env python3
"""Check external links in all Markdown content files."""

import os
import re
import sys
import time
import urllib.request
import urllib.error

CONTENT_DIR = "content"
TIMEOUT = 30
MAX_RETRIES = 3
RETRY_DELAY = 2  # seconds, doubles each retry
LINK_PATTERN = re.compile(r'\[([^\]]*)\]\((https?://[^\)]+)\)')

# User-Agent that mirrors a real browser to avoid bot-blocking by sites like
# census.gov, cleveland.com, and codelibrary.amlegal.com
USER_AGENT = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
    "AppleWebKit/537.36 (KHTML, like Gecko) "
    "Chrome/120.0.0.0 Safari/537.36"
)


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
    """Check if a URL is reachable, with retries and exponential backoff."""
    for attempt in range(MAX_RETRIES):
        try:
            req = urllib.request.Request(url, method="HEAD")
            req.add_header("User-Agent", USER_AGENT)
            req.add_header("Accept", "text/html,application/xhtml+xml,*/*")
            with urllib.request.urlopen(req, timeout=TIMEOUT) as resp:
                if resp.status < 400:
                    return True
        except (urllib.error.URLError, urllib.error.HTTPError, OSError):
            pass

        # Fall back to GET on last HEAD attempt or if HEAD returned error
        try:
            req = urllib.request.Request(url, method="GET")
            req.add_header("User-Agent", USER_AGENT)
            req.add_header("Accept", "text/html,application/xhtml+xml,*/*")
            with urllib.request.urlopen(req, timeout=TIMEOUT) as resp:
                if resp.status < 400:
                    return True
        except urllib.error.HTTPError as e:
            # 403 often means bot-blocking, not a broken link
            if e.code == 403:
                return True
            if attempt < MAX_RETRIES - 1:
                time.sleep(RETRY_DELAY * (2 ** attempt))
                continue
            return False
        except (urllib.error.URLError, OSError):
            if attempt < MAX_RETRIES - 1:
                time.sleep(RETRY_DELAY * (2 ** attempt))
                continue
            return False

    return False


def main():
    md_files = find_markdown_files(CONTENT_DIR)
    broken = []
    checked = 0

    # Deduplicate URLs: check each unique URL only once
    url_locations = {}  # url -> [(filepath, line_num), ...]
    for filepath in md_files:
        links = extract_links(filepath)
        for url, line_num in links:
            url_locations.setdefault(url, []).append((filepath, line_num))

    unique_urls = list(url_locations.keys())
    url_results = {}  # url -> True/False

    for url in unique_urls:
        checked += 1
        result = check_url(url)
        url_results[url] = result
        if result:
            print(f"  OK: {url}")
        else:
            locations = url_locations[url]
            for filepath, line_num in locations:
                broken.append((filepath, line_num, url))
            print(f"  BROKEN: {url}")
            for filepath, line_num in locations:
                print(f"    referenced in {filepath}:{line_num}")

    print(f"\nChecked {checked} unique links across {len(md_files)} files")
    if broken:
        print(f"Found {len(broken)} broken link reference(s):")
        for filepath, line_num, url in broken:
            print(f"  {filepath}:{line_num} -> {url}")
        sys.exit(1)
    else:
        print("All links valid!")
        sys.exit(0)


if __name__ == "__main__":
    main()
