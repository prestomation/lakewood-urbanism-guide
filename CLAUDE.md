# CLAUDE.md - AI Assistant Guide for Lakewood Urbanism Guide

## Project Overview

This is a **Hugo static site** serving as a practical reference guide for Lakewood, Ohio urbanists and advocates. It helps people understand urban planning issues, learn terminology, and prepare for community participation.

- **Site URL**: https://lakewood.urbanism-guide.com/
- **Theme**: hugo-book (git submodule at `themes/hugo-book/`)
- **Hugo Version**: 0.147.0 (extended)
- **License**: MIT

## Directory Structure

```
lakewood-urbanism-guide/
├── archetypes/           # Content templates for new pages
│   ├── blog.md          # Blog post template
│   ├── glossary.md      # Glossary entry template
│   └── default.md       # Generic page template
├── content/              # All Markdown content (main working area)
│   ├── _index.md        # Homepage
│   ├── quick-start/     # Lakewood governance & context
│   ├── glossary/        # Terminology by category (4 files)
│   ├── guides/          # In-depth topic guides (walkability, bike, transit, housing)
│   ├── timeline/        # Historical events section
│   ├── data/            # Public data sources directory
│   └── blog/            # Analysis posts
├── data/                 # Structured data files
│   └── timeline.yaml    # Timeline entries (year, title, description, sources)
├── layouts/              # Custom Hugo templates
│   ├── partials/        # Template includes (head injection for CSS)
│   └── shortcodes/      # timeline.html, blog-list.html
├── static/               # Static assets served as-is
│   └── css/timeline.css # Custom styling for timeline, blog, and site
├── themes/hugo-book/     # External theme (git submodule - DO NOT EDIT)
├── scripts/              # Build and validation scripts
│   ├── validate-timeline.py      # Ensures timeline is in reverse chronological order
│   └── check-external-links.py   # Validates all external URLs in content
├── .github/workflows/    # CI/CD automation
│   ├── deploy.yml       # Production deployment to gh-pages
│   ├── pr-preview.yml   # PR preview builds
│   └── pr-preview-cleanup.yml
├── hugo.toml             # Main Hugo configuration
├── .htmltest.yml         # Link validation config
├── ideas.md              # Content ideas and suggestions for new guides, glossary, timeline, blog
├── CLAUDE.md             # This file — AI assistant guide
└── README.md             # User-facing documentation
```

## Quick Commands

```bash
# Local development server (includes drafts)
hugo server -D

# Production build
hugo --gc --minify

# Validate timeline order (run before committing timeline changes)
python3 scripts/validate-timeline.py

# Check all external links in content
python3 scripts/check-external-links.py

# Create new blog post
hugo new blog/my-post-title.md

# Create new glossary entry
hugo new glossary/category/term-name.md
```

## Content Editing Guidelines

### Glossary Entries (`content/glossary/`)

Four category files exist:
- `housing-zoning.md` — ADU, variance, CRA, conditional use, historic preservation, mixed-use, zoning code
- `transportation.md` — Complete streets, mode share, active transportation, Walk Score, RTA, last mile, Safe Routes to School
- `land-use.md` — Community Vision, comprehensive plan, inner-ring suburb, streetcar suburb, upzoning, resiliency
- `funding-policy.md` — TIF, CDBG, CRA, impact fees, tax abatement, Main Street program, Startup Lakewood

**Format for new terms**:
```markdown
### Term Name

Brief definition in plain language.

**Why it matters:** Explain relevance to Lakewood urbanists.

**See also:** [Related Term](#related-term)

**Learn more:** [Primary Source](url) | [Secondary Source](url)
```

**Source requirements for glossary terms:**
- **Primary source (required):** Must be a governmental or official institutional source (e.g., lakewoodoh.gov, riderta.com, development.ohio.gov, hud.gov, cuyahogacounty.gov)
- **Secondary source (preferred):** The Land (thelandcle.org), Ideastream, Crain's Cleveland Business, Cleveland.com, Lakewood Observer, or other reputable local journalism/policy sources

### Timeline Entries (`data/timeline.yaml`)

Entries are in **reverse chronological order** (newest first). Each entry:

```yaml
- year: 2024
  title: "Event Title"
  description: "What happened and why it matters."
  legacy: "Long-term impact or current relevance."
  sources:
    primary:
      text: "Source Name"
      url: "https://..."
    secondary:
      text: "Additional Source"
      url: "https://..."
```

### Topic Guides (`content/guides/`)

Guides are in-depth pages covering a specific urbanism topic in Lakewood. Each guide lives as a single Markdown file in `content/guides/`.

**Existing guides:**
- `walkability.md` — Walk Score, pedestrian infrastructure, sidewalks, safety
- `bike-network.md` — Bicycle Master Plan, Active Transportation plan, Bike Lakewood
- `public-transit.md` — RTA bus routes, rapid rail, last mile study, circulator history
- `housing.md` — Housing stock, Lakewood Common, zoning code update, Housing Forward

**Front matter:**
```yaml
---
title: "Guide Title"
weight: 3          # Controls sidebar order (1 = first)
bookToc: true      # Enables right-side table of contents
---
```

**Standard section structure** (follow this order; omit sections that don't apply):

```markdown
# Topic Name in Lakewood

Introductory paragraph: what this is and why it matters. 1-3 sentences.

## Current state / types / operators
Overview of how things work today. Use ### subheadings for categories.

## History
Chronological ### subheadings (e.g., "### 2024: Active Transportation Plan Adopted").
Cover key milestones from origin to present. Include inline source links.

## How the city manages / plans / funds it
Permitting, planning frameworks, funding sources, relevant city departments.

## Advocacy organizations (if applicable)
Bullet list of key orgs with links and one-line descriptions.

## Data sources
Where to find official data: city dashboards, county portals, state datasets.

## Key statistics
Markdown table with current metrics. Cite sources below the table.

## Related resources
Cross-links to other guides (use relref) and relevant external pages.

---

*Last updated: Month Year*
```

**Writing style:**
- Practical and factual; write for someone preparing for a public hearing or community meeting
- Use **bold** for program names, organization names, and key terms on first mention
- Inline source citations as Markdown links, not footnotes
- Prefer lakewoodoh.gov, riderta.com, cuyahogacounty.gov, development.ohio.gov as primary sources
- Use The Land (thelandcle.org), Ideastream, Crain's Cleveland Business, Lakewood Observer, or Cleveland.com as secondary sources
- Every claim with a number or date should have a source link

**Source requirements for guides:**
- **Primary sources (required):** Government or official institutional sources (lakewoodoh.gov, riderta.com, cuyahogacounty.gov, development.ohio.gov, hud.gov, census.gov)
- **Secondary sources (preferred):** The Land, Ideastream, Crain's Cleveland Business, Cleveland.com, Lakewood Observer, Freshwater Cleveland, NEOtrans
- **Advocacy/org sources (acceptable for org-specific claims):** lakewoodalive.org, bikecleveland.org, lakewoodhistory.org
- **Verify every URL** with WebFetch or the link checker before committing

**After creating a new guide**, update `content/guides/_index.md` to add an entry under "Available Guides":
```markdown
- [Guide Title]({{< relref "file-name" >}}) -- Short description
```

### Blog Posts (`content/blog/`)

Use the archetype: `hugo new blog/post-title.md`

Front matter includes:
- `title`, `date`, `tags`, `categories`, `summary`
- `draft: true` by default (remove or set false to publish)

## Key Configuration (hugo.toml)

- **Base URL**: `https://lakewood.urbanism-guide.com/`
- **Theme settings**: Auto dark/light mode, TOC enabled, search enabled
- **Markup**: Goldmark with unsafe HTML allowed (for shortcodes)
- **Menu weights**: Quick Start (1), Glossary (2), Guides (3), Timeline (4), Data (5), Blog (6)

## Custom Components

### Timeline Shortcode
`{{</* timeline */>}}` renders `data/timeline.yaml` as an interactive timeline with source citations.

### Blog List Shortcode
`{{</* blog-list */>}}` auto-generates a list of blog posts with dates, tags, and summaries.

## Build and Deployment

### Automated (GitHub Actions)
- **Push to main**: Validates timeline order, builds, checks external links, deploys to gh-pages
- **Pull requests**: Validates timeline order, creates preview at `/pr-preview/{PR_NUMBER}/`
- **PR close**: Cleans up preview directory

### Timeline Validation
`scripts/validate-timeline.py` runs before every build to ensure timeline entries are in reverse chronological order. The build will fail if entries are out of order.

### Link Validation
`scripts/check-external-links.py` checks all external URLs in content Markdown files. External link failures are logged but don't block deployment.

## Important Conventions

1. **Every factual claim needs a source**: All claims, facts, statistics, dates, and assertions in content must have an inline linked source. No unsourced statements — if you can't find a source for a claim, don't include it. Use inline Markdown links (not footnotes) to cite sources directly where the claim appears. **Avoid subjective or editorial language** (e.g., "one of the best," "remarkably") — stick to verifiable facts and let readers draw their own conclusions.

2. **Theme is read-only**: Never edit files in `themes/hugo-book/`. Override via `layouts/` or `static/`.

3. **Content format**: All content is Markdown with YAML front matter. Keep it portable.

4. **Timeline sources required**: New timeline entries should include at least a primary source with URL.

5. **Chronology**: Timeline entries in `data/timeline.yaml` are ordered newest-first.

6. **Draft content**: Set `draft: true` in front matter for work-in-progress. Use `hugo server -D` to preview.

7. **No node_modules by default**: The project is pure Hugo unless package.json is added for asset processing.

8. **Verify links before adding**: Always use WebFetch to verify that external URLs are valid before adding them to content. The CI runs `python3 scripts/check-external-links.py` which will log broken links. To check all links locally, run:
   ```bash
   python3 scripts/check-external-links.py
   ```

## Git Workflow

- Main branch: `main`
- Feature branches for changes
- PRs get automatic preview builds
- Merge triggers production deployment

## Common Tasks for AI Assistants

**Content ideas:** See `ideas.md` in the project root for prioritized suggestions for new guides, glossary terms, timeline entries, and blog posts. Consult this file when planning new content. After implementing an idea, remove it from the list entirely.

### Adding a glossary term
1. Identify the correct category file in `content/glossary/`
2. Add the term in alphabetical order within the file
3. Follow the "Term Name / Definition / Why it matters / See also / Learn more" format
4. **Verify all URLs using WebFetch before adding them** to ensure they return valid content (not 404s)
5. Include a primary governmental source and secondary source (preferably The Land or Ideastream) in the "Learn more" section

### Adding a timeline event
1. Edit `data/timeline.yaml`
2. Insert at the correct position (reverse chronological — newer entries first)
3. Include year, title, description, legacy, and at least one source
4. **Verify all source URLs using WebFetch before adding them** to ensure they return valid content (not 404s)
5. Run `python3 scripts/validate-timeline.py` to verify order before committing

### Creating a new topic guide
1. Read an existing guide (e.g., `content/guides/walkability.md` or `content/guides/housing.md`) to match the tone and structure
2. Create a new file at `content/guides/topic-name.md` with the standard front matter (`title`, `weight`, `bookToc: true`)
3. Follow the standard section structure: current state, history, city management/planning, advocacy orgs, data sources, key statistics table, related resources
4. Research content using WebSearch; aim for a mix of government sources and local journalism
5. **Verify every external URL** using WebFetch or `python3 scripts/check-external-links.py` before committing
6. Add cross-links: link to related glossary pages using `{{< relref "/glossary/category" >}}` and to other guides using `{{< relref "guide-name" >}}`
7. **Add glossary entries** for key urbanist terms introduced or heavily used in the guide (see "Glossary integration" below)
8. **Add data sources** to `content/data/_index.md` for any primary/public data dashboards, portals, or datasets referenced in the guide (see "Data page integration" below)
9. Update `content/guides/_index.md` to list new guide
10. End the page with `*Last updated: Month Year*`

### Glossary integration
When creating or editing guides, any urbanist term that has a glossary entry should be linked to it using `relref` on first mention in the guide. If a key urbanist term used in a guide does **not** yet have a glossary entry, create one:
1. Identify the correct category file (`housing-zoning.md`, `transportation.md`, `land-use.md`, or `funding-policy.md`)
2. Add the entry in alphabetical order following the standard format (Term Name / Definition / Why it matters / See also / Learn more)
3. Link back to the term from the guide using `{{< relref "/glossary/category#term-anchor" >}}`

This ensures the glossary stays comprehensive and readers can always jump from a guide to a plain-language definition.

### Data page integration
When a guide references a primary, public data source — a government dashboard, open data portal, interactive map, or public API — add it to `content/data/_index.md` under the appropriate geographic section (City of Lakewood, Cuyahoga County, or Regional & State). Follow the existing format:
```markdown
### Dashboard Name

One-sentence description of what data it provides and how urbanists can use it.

**Access:** [Link Text](url)
```
This keeps the Data page as the single reference for all public data sources across the site.

### Creating a blog post
1. Run `hugo new blog/post-title.md` or manually create file
2. Fill in front matter (title, date, tags, summary)
3. Set `draft: false` when ready to publish

### Modifying styles
1. Edit `static/css/timeline.css` — this is the single custom stylesheet for the entire site
2. Dark mode: Use `@media (prefers-color-scheme: dark)` queries
3. Mobile: Breakpoint at 600px width

**Color palette:** The site uses Lake Erie and Lakewood-inspired colors defined as CSS variables in `:root`. Always use these variables — never hardcode colors.

| Variable | Light | Dark | Inspiration |
|---|---|---|---|
| `--color-link` | `#1B6B93` Lake Erie Blue | `#5DB8D9` Light Blue | Lake Erie |
| `--accent-green` | `#2E8B57` Emerald | `#5CB88A` | Parks and tree canopy |
| `--accent-gold` | `#D4A843` Gold | `#E8C36A` | Historic character |
| `--accent-brick` | `#C75B39` Brick Red | `#D98067` | Streetcar-era homes |
| `--accent-gradient` | Blue → Green | Lightened | Both |

Additional variables: `--card-shadow`, `--card-shadow-hover`, `--border-radius` (0.5rem).

**Visual conventions:**
- Homepage sections use card-style `.book-columns` with shadows and hover lift
- Timeline and blog entries are styled as cards with `--card-shadow`
- Table headers use `--color-link` as background color
- The homepage h1 uses a gradient text effect (`--accent-gradient`)
- Bold labels like "Why it matters:" are colored with `--color-link` via `p > strong:first-child`

### Testing locally
```bash
hugo server -D  # Starts at http://localhost:1313/
```

## Lakewood-Specific Context

Key facts for content accuracy:

- **Population:** ~52,000 in 5.53 square miles
- **Density:** ~9,400 people/sq mi (highest in Ohio, comparable to Washington, D.C.)
- **Government:** Council-manager with 7 council members (3 at-large, 4 ward)
- **Planning framework:** Community Vision (2012, updated 2017/2019) — not a traditional master plan
- **Zoning:** Last comprehensive update in 1996; major update process launched 2024
- **Commercial corridors:** Detroit Avenue (primary) and Madison Avenue (secondary)
- **Transit:** 6 RTA bus routes, 2 nearby Red Line stations (W. 117th, Triskett)
- **Walk Score:** 70 (highest in Ohio; state average is 34)
- **School buses:** Lakewood has never operated school buses
- **Key development:** Lakewood Common — $119M mixed-use, 305 units, 25K sq ft retail (groundbreaking Sep 2025)
- **Key organizations:** LakewoodAlive (CDC), Bike Lakewood (advocacy), Lakewood Historical Society

**Primary source domains:**
- lakewoodoh.gov (city government)
- riderta.com (transit authority)
- cuyahogacounty.gov (county government)
- codelibrary.amlegal.com (codified ordinances)
- development.ohio.gov (state development agency)
- lakewoodalive.org (community development)
- lakewoodhistory.org (historical society)

**Secondary source domains:**
- thelandcle.org (The Land — Cleveland journalism)
- ideastream.org (Ideastream Public Media)
- crainscleveland.com (Crain's Cleveland Business)
- cleveland.com (Cleveland.com / Plain Dealer)
- lakewoodobserver.com (Lakewood Observer)
- neo-trans.blog (NEOtrans — development news)
- freshwatercleveland.com (Freshwater Cleveland)
- case.edu/ech (Encyclopedia of Cleveland History)

## File Size Reference

- Content: ~15 markdown files across glossary, guides, quick-start, data, blog
- Glossary: 4 category files
- Timeline: 15 entries in YAML
- Guides: 4 topic guides
- Custom CSS: ~180 lines
- Total: Lightweight Hugo site

## External Resources

- Hugo documentation: https://gohugo.io/documentation/
- hugo-book theme: https://github.com/alex-shpak/hugo-book
- htmltest: https://github.com/wjdp/htmltest
- City of Lakewood: https://www.lakewoodoh.gov/
- LakewoodAlive: https://www.lakewoodalive.org/
- Bike Lakewood: https://www.bikecleveland.org/bikelakewood/
