# AGENTS.md — Lakewood Urbanism Guide

This is a city repo for the urbanism-guide platform.

## First: Read the Platform Guide

Before making any changes, read the platform AGENTS.md for architecture, CI rules, and workflow conventions:

```bash
gh api repos/prestomation/urbanism-guide-core/contents/AGENTS.md --jq '.content' | base64 -d
```

Everything you need to know about how city repos work, what belongs in core vs city, the PR workflow, and deployment verification is documented there.

## This Repo

- **City:** Lakewood
- **Platform core:** `prestomation/urbanism-guide-core`
- **Core version:** See `go.mod`

## City-Specific Files

Files in this repo that override or extend core:
- `static/css/brand.css` — city color palette
- `archetypes/glossary.md` — city-specific glossary template (if present)
- `scripts/check-external-links.py` — city-specific blocked domains (if present)
- `content/` — all city content (Markdown)
- `data/timeline.yaml` — city timeline entries
- `data/site_stats.yaml` — city statistics for `{{< stat >}}` shortcode

## CI Rules

1. **Never push directly to `main`** — all changes go through a PR
2. **PR preview CI must pass before merging** — `pr-preview.yml` runs the full build and validation
3. **After merging, verify the deploy CI on `main` completes successfully** and confirm the live site is working
4. **If deploy fails, fix via a new PR** — do not push directly to `main`
