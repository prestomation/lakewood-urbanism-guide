# AGENTS.md — Lakewood Urbanism Guide

This is a city repo for the urbanism-guide platform.

## First: Read the Platform Guide

Before making any changes, read the platform AGENTS.md for architecture, CI rules, required scripts, and workflow conventions:

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

## CI Rules (summary — full details in core AGENTS.md)

1. **Never push directly to `main`** — always open a PR
2. **Use `poll_pr.sh`** after every push to a PR branch — waits for CI + Amazon Q
3. **Use `check_deploy.sh`** after every merge — verifies deploy + HTTP 200
4. Scripts at: `~/.openclaw/workspace/skills/post-pull-request/scripts/`
