"""
knowledge_updater.py — Skill #232: Micro Urban Agriculture Design & Management
==============================================================================
crawl4ai-powered knowledge pipeline that fetches the latest research and news
from authoritative urban agriculture / hydroponics sources and appends new,
deduplicated entries to SECOND-KNOWLEDGE-BRAIN.md.

Schedule: Weekly cron — recommended: 0 6 * * 1  (Monday 06:00 UTC)

Dependencies:
    pip install crawl4ai feedparser requests beautifulsoup4 python-dateutil

Usage:
    python knowledge_updater.py [--dry-run] [--verbose]

    --dry-run   Print entries that would be added without writing to files
    --verbose   Print detailed crawl progress

Output:
    - Appends new rows to SECOND-KNOWLEDGE-BRAIN.md (papers table + methods + log)
    - Updates .knowledge_index.json with hashes of processed entries
"""

import argparse
import asyncio
import hashlib
import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional
from urllib.parse import urljoin, urlparse

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------

BASE_DIR = Path(__file__).resolve().parent.parent  # D:\Dungchan\skill_adv\232\
KNOWLEDGE_BRAIN_PATH = BASE_DIR / "SECOND-KNOWLEDGE-BRAIN.md"
INDEX_PATH = BASE_DIR / ".knowledge_index.json"

DOMAIN_KEYWORDS = [
    "hydroponics", "aeroponics", "DLI", "daily light integral",
    "nutrient film technique", "NFT", "deep water culture", "DWC", "Kratky",
    "urban agriculture", "urban farming", "soilless", "controlled environment agriculture",
    "CEA", "vertical farming", "rooftop farming", "balcony garden",
    "nutrient solution", "EC", "electrical conductivity", "pH",
    "VPD", "vapor pressure deficit", "plant growth lighting",
    "lettuce", "basil", "microgreens", "hydroponic tomato",
    "food security", "water use efficiency", "food miles",
]

MIN_RELEVANCE_SCORE = 0.3  # minimum keyword match fraction to include entry

SOURCES = [
    {
        "name": "MDPI Horticulturae RSS",
        "url": "https://www.mdpi.com/journal/horticulturae/rss",
        "type": "rss",
        "description": "Open-access peer-reviewed journal on horticultural science",
    },
    {
        "name": "ArXiv q-bio.QM Recent",
        "url": "https://arxiv.org/list/q-bio.QM/recent",
        "type": "arxiv_html",
        "description": "Quantitative methods in biology — includes plant physiology",
    },
    {
        "name": "FAO Urban Agriculture",
        "url": "https://www.fao.org/urban-agriculture/en/",
        "type": "html_scrape",
        "description": "FAO's urban and peri-urban agriculture resources",
    },
    {
        "name": "RUAF Foundation News",
        "url": "https://ruaf.org/news/",
        "type": "html_scrape",
        "description": "Resource Centres on Urban Agriculture and Food Systems",
    },
    {
        "name": "MDPI Horticulturae Search — Hydroponics",
        "url": "https://www.mdpi.com/search?q=hydroponics&journal=horticulturae&article_type=research-article&order=pubdate",
        "type": "html_scrape",
        "description": "MDPI Horticulturae search for hydroponics research articles",
    },
]

# ---------------------------------------------------------------------------
# Data classes
# ---------------------------------------------------------------------------

class Entry:
    """Represents a single knowledge entry (paper, news item, report)."""

    def __init__(
        self,
        title: str,
        url: str,
        authors: str = "Unknown",
        year: Optional[int] = None,
        venue: str = "Unknown",
        abstract: str = "",
        source_name: str = "",
    ):
        self.title = title.strip()
        self.url = url.strip()
        self.authors = authors.strip()
        self.year = year or datetime.now(timezone.utc).year
        self.venue = venue.strip()
        self.abstract = abstract.strip()
        self.source_name = source_name
        self.relevance_score: float = 0.0
        self.url_hash: str = self._compute_hash()

    def _compute_hash(self) -> str:
        canonical = self.url.lower().split("?")[0].rstrip("/")
        return hashlib.sha256(canonical.encode("utf-8")).hexdigest()[:16]

    def to_table_row(self) -> str:
        short_title = self.title[:80] + "..." if len(self.title) > 80 else self.title
        short_authors = self.authors[:40] + "..." if len(self.authors) > 40 else self.authors
        relevance_note = self._relevance_note()
        return (
            f"| {short_title} | {short_authors} | {self.year} "
            f"| {self.venue} | {self.url} | {relevance_note} |"
        )

    def _relevance_note(self) -> str:
        matched = [kw for kw in DOMAIN_KEYWORDS if kw.lower() in self.title.lower() + " " + self.abstract.lower()]
        if not matched:
            return "Urban agriculture relevance"
        return f"Keywords: {', '.join(matched[:3])}"


# ---------------------------------------------------------------------------
# Relevance scoring
# ---------------------------------------------------------------------------

def score_relevance(entry: Entry) -> float:
    """Score entry relevance against domain keywords (0.0–1.0)."""
    text = (entry.title + " " + entry.abstract).lower()
    matched = sum(1 for kw in DOMAIN_KEYWORDS if kw.lower() in text)
    score = matched / len(DOMAIN_KEYWORDS)
    return min(score, 1.0)


# ---------------------------------------------------------------------------
# Index management
# ---------------------------------------------------------------------------

def load_index() -> set:
    """Load the set of already-processed URL hashes."""
    if INDEX_PATH.exists():
        try:
            data = json.loads(INDEX_PATH.read_text(encoding="utf-8"))
            return set(data.get("processed_hashes", []))
        except (json.JSONDecodeError, KeyError):
            return set()
    return set()


def save_index(hashes: set) -> None:
    """Persist the updated set of processed URL hashes."""
    data = {
        "last_updated": datetime.now(timezone.utc).isoformat(),
        "processed_hashes": sorted(hashes),
        "total_entries": len(hashes),
    }
    INDEX_PATH.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")


# ---------------------------------------------------------------------------
# Crawl4AI async crawlers
# ---------------------------------------------------------------------------

async def crawl_rss(source: dict, verbose: bool = False) -> list[Entry]:
    """Crawl an RSS feed and extract entries."""
    entries = []
    try:
        import feedparser
        import requests

        if verbose:
            print(f"  [RSS] Fetching {source['url']}")

        headers = {"User-Agent": "Mozilla/5.0 (knowledge_updater/1.0; urban-ag-skill)"}
        resp = requests.get(source["url"], headers=headers, timeout=30)
        resp.raise_for_status()
        feed = feedparser.parse(resp.content)

        for item in feed.entries[:20]:  # cap at 20 items per source
            title = getattr(item, "title", "")
            link = getattr(item, "link", "")
            summary = getattr(item, "summary", "")
            # Clean HTML from summary
            summary_clean = re.sub(r"<[^>]+>", " ", summary).strip()
            # Extract year from published date
            pub_year = None
            if hasattr(item, "published_parsed") and item.published_parsed:
                pub_year = item.published_parsed.tm_year
            # Extract authors
            authors = "Unknown"
            if hasattr(item, "authors"):
                authors = ", ".join(a.get("name", "") for a in item.authors[:3])
            elif hasattr(item, "author"):
                authors = item.author

            if title and link:
                entry = Entry(
                    title=title,
                    url=link,
                    authors=authors,
                    year=pub_year,
                    venue=source["name"],
                    abstract=summary_clean[:500],
                    source_name=source["name"],
                )
                entries.append(entry)

        if verbose:
            print(f"  [RSS] Found {len(entries)} entries from {source['name']}")

    except Exception as e:
        print(f"  [RSS] Error crawling {source['name']}: {e}", file=sys.stderr)

    return entries


async def crawl_arxiv_html(source: dict, verbose: bool = False) -> list[Entry]:
    """Crawl ArXiv recent listings page and extract paper entries."""
    entries = []
    try:
        from crawl4ai import AsyncWebCrawler

        if verbose:
            print(f"  [ArXiv] Fetching {source['url']}")

        async with AsyncWebCrawler(verbose=False) as crawler:
            result = await crawler.arun(url=source["url"])
            if not result.success:
                print(f"  [ArXiv] Crawl failed: {result.error_message}", file=sys.stderr)
                return entries

            content = result.markdown or ""

            # Extract paper blocks: look for title + abstract + arXiv ID patterns
            # ArXiv HTML structure: dt/dd pairs with title, authors, abstract
            title_pattern = re.compile(
                r"\[(\d{4}\.\d{4,5})\].*?Title:\s*(.+?)(?:\n|Authors:)", re.DOTALL
            )
            for match in title_pattern.finditer(content):
                arxiv_id = match.group(1)
                title = match.group(2).strip().replace("\n", " ")
                url = f"https://arxiv.org/abs/{arxiv_id}"
                entry = Entry(
                    title=title,
                    url=url,
                    year=int("20" + arxiv_id[:2]),
                    venue="ArXiv q-bio.QM",
                    source_name=source["name"],
                )
                entries.append(entry)

            if verbose:
                print(f"  [ArXiv] Extracted {len(entries)} candidate entries")

    except ImportError:
        print("  [ArXiv] crawl4ai not installed. Skipping ArXiv crawl.", file=sys.stderr)
    except Exception as e:
        print(f"  [ArXiv] Error: {e}", file=sys.stderr)

    return entries


async def crawl_html_scrape(source: dict, verbose: bool = False) -> list[Entry]:
    """Generic HTML scrape using crawl4ai — extracts links and titles."""
    entries = []
    try:
        from crawl4ai import AsyncWebCrawler
        from crawl4ai.extraction_strategy import JsonCssExtractionStrategy

        if verbose:
            print(f"  [HTML] Fetching {source['url']}")

        schema = {
            "name": "ArticleLinks",
            "baseSelector": "article, .post, .news-item, .card, .entry",
            "fields": [
                {"name": "title", "selector": "h2, h3, .title, .entry-title", "type": "text"},
                {"name": "url", "selector": "a", "type": "attribute", "attribute": "href"},
                {"name": "summary", "selector": "p, .excerpt, .summary", "type": "text"},
            ],
        }

        extraction_strategy = JsonCssExtractionStrategy(schema)

        async with AsyncWebCrawler(verbose=False) as crawler:
            result = await crawler.arun(
                url=source["url"],
                extraction_strategy=extraction_strategy,
            )

            if not result.success:
                # Fall back to plain markdown extraction
                content = result.markdown or ""
                # Extract markdown links: [title](url)
                link_pattern = re.compile(r"\[([^\]]+)\]\((https?://[^\)]+)\)")
                for match in link_pattern.finditer(content):
                    title = match.group(1).strip()
                    url = match.group(2).strip()
                    if len(title) > 20 and any(kw.lower() in title.lower() for kw in DOMAIN_KEYWORDS):
                        entry = Entry(
                            title=title,
                            url=url,
                            venue=source["name"],
                            source_name=source["name"],
                        )
                        entries.append(entry)
            else:
                try:
                    extracted = json.loads(result.extracted_content or "[]")
                    for item in extracted[:15]:
                        title = item.get("title", "").strip()
                        url = item.get("url", "").strip()
                        summary = item.get("summary", "").strip()
                        if not title or not url:
                            continue
                        # Resolve relative URLs
                        if url.startswith("/"):
                            parsed = urlparse(source["url"])
                            url = f"{parsed.scheme}://{parsed.netloc}{url}"
                        entry = Entry(
                            title=title,
                            url=url,
                            abstract=summary[:500],
                            venue=source["name"],
                            source_name=source["name"],
                        )
                        entries.append(entry)
                except json.JSONDecodeError:
                    pass

        if verbose:
            print(f"  [HTML] Extracted {len(entries)} candidate entries from {source['name']}")

    except ImportError:
        print("  [HTML] crawl4ai not installed. Skipping HTML scrape.", file=sys.stderr)
    except Exception as e:
        print(f"  [HTML] Error crawling {source['name']}: {e}", file=sys.stderr)

    return entries


# ---------------------------------------------------------------------------
# SECOND-KNOWLEDGE-BRAIN.md update logic
# ---------------------------------------------------------------------------

def append_to_knowledge_brain(new_entries: list[Entry], dry_run: bool = False) -> int:
    """
    Append new entries to the appropriate sections of SECOND-KNOWLEDGE-BRAIN.md.
    Returns the count of entries actually written.
    """
    if not KNOWLEDGE_BRAIN_PATH.exists():
        print(f"ERROR: SECOND-KNOWLEDGE-BRAIN.md not found at {KNOWLEDGE_BRAIN_PATH}", file=sys.stderr)
        return 0

    content = KNOWLEDGE_BRAIN_PATH.read_text(encoding="utf-8")
    count_added = 0
    today = datetime.now(timezone.utc).strftime("%Y-%m-%d")

    # --- Append paper table rows ---
    papers_marker = "## 2. Key Research Papers"
    papers_table_end_pattern = re.compile(r"(\| [^\n]+ \|)\n\n---", re.DOTALL)

    paper_rows = []
    for entry in new_entries:
        row = entry.to_table_row()
        paper_rows.append(row)

    if paper_rows:
        rows_block = "\n".join(paper_rows)
        # Find the end of the papers table (last row before blank line + ---)
        # Insert new rows before the blank line after the last existing row
        papers_section_match = re.search(
            r"(## 2\. Key Research Papers.*?\n)((?:\| .+\|\n)+)",
            content,
            re.DOTALL,
        )
        if papers_section_match:
            insert_pos = papers_section_match.end()
            if not dry_run:
                content = content[:insert_pos] + rows_block + "\n" + content[insert_pos:]
            count_added += len(paper_rows)
        else:
            print("  [WARN] Could not locate papers table in SECOND-KNOWLEDGE-BRAIN.md", file=sys.stderr)

    # --- Append Knowledge Update Log entry ---
    log_marker = "## 7. Knowledge Update Log"
    log_table_pattern = re.compile(
        r"(## 7\. Knowledge Update Log\n\n\| Date \|.*?\n(?:\| --- \|.*?\n))((?:\| .+\|\n)*)",
        re.DOTALL,
    )
    log_match = log_table_pattern.search(content)
    if log_match:
        sources_crawled = list(set(e.source_name for e in new_entries))
        log_entry = (
            f"| {today} | {', '.join(sources_crawled[:3])} "
            f"| {count_added} | Automated weekly crawl |"
        )
        insert_pos = log_match.end()
        if not dry_run:
            content = content[:insert_pos] + log_entry + "\n" + content[insert_pos:]
    else:
        print("  [WARN] Could not locate Knowledge Update Log in SECOND-KNOWLEDGE-BRAIN.md", file=sys.stderr)

    if not dry_run and count_added > 0:
        KNOWLEDGE_BRAIN_PATH.write_text(content, encoding="utf-8")
        print(f"  [KB] Wrote {count_added} new entries to SECOND-KNOWLEDGE-BRAIN.md")

    return count_added


# ---------------------------------------------------------------------------
# Main pipeline
# ---------------------------------------------------------------------------

async def run_pipeline(dry_run: bool = False, verbose: bool = False) -> None:
    """Main knowledge update pipeline."""
    print(f"{'[DRY RUN] ' if dry_run else ''}Knowledge Updater — Skill #232 Micro Urban Agriculture")
    print(f"Timestamp: {datetime.now(timezone.utc).isoformat()}")
    print(f"Knowledge Brain: {KNOWLEDGE_BRAIN_PATH}")
    print("-" * 60)

    # Load existing index
    processed_hashes = load_index()
    print(f"Index: {len(processed_hashes)} entries already processed")

    # Crawl all sources
    all_entries: list[Entry] = []
    for source in SOURCES:
        if source["type"] == "rss":
            entries = await crawl_rss(source, verbose=verbose)
        elif source["type"] == "arxiv_html":
            entries = await crawl_arxiv_html(source, verbose=verbose)
        elif source["type"] == "html_scrape":
            entries = await crawl_html_scrape(source, verbose=verbose)
        else:
            print(f"  [WARN] Unknown source type: {source['type']}", file=sys.stderr)
            entries = []
        all_entries.extend(entries)

    print(f"\nTotal raw entries fetched: {len(all_entries)}")

    # Score relevance
    for entry in all_entries:
        entry.relevance_score = score_relevance(entry)

    # Filter by relevance threshold
    relevant = [e for e in all_entries if e.relevance_score >= MIN_RELEVANCE_SCORE]
    print(f"Relevant (score >= {MIN_RELEVANCE_SCORE}): {len(relevant)}")

    # Deduplicate against index
    new_entries = [e for e in relevant if e.url_hash not in processed_hashes]
    print(f"New (not previously seen): {len(new_entries)}")

    if not new_entries:
        print("\nNo new entries to add. Knowledge base is current.")
        return

    # Sort by relevance score descending
    new_entries.sort(key=lambda e: e.relevance_score, reverse=True)

    if verbose:
        print("\nTop new entries by relevance:")
        for e in new_entries[:5]:
            print(f"  [{e.relevance_score:.2f}] {e.title[:70]}...")

    # Append to SECOND-KNOWLEDGE-BRAIN.md
    count_written = append_to_knowledge_brain(new_entries, dry_run=dry_run)

    # Update index
    if not dry_run:
        for entry in new_entries:
            processed_hashes.add(entry.url_hash)
        save_index(processed_hashes)
        print(f"Index updated: {len(processed_hashes)} total entries")

    print(f"\n{'[DRY RUN] Would have added' if dry_run else 'Added'} {count_written} entries.")
    print("Done.")


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(
        description="Weekly knowledge updater for Skill #232 — Micro Urban Agriculture Design"
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Print entries that would be added without writing to files",
    )
    parser.add_argument(
        "--verbose",
        action="store_true",
        help="Print detailed crawl progress",
    )
    args = parser.parse_args()

    asyncio.run(run_pipeline(dry_run=args.dry_run, verbose=args.verbose))


if __name__ == "__main__":
    main()


# ---------------------------------------------------------------------------
# Cron setup instructions (comment block)
# ---------------------------------------------------------------------------
# To schedule weekly execution:
#
# Linux/macOS (crontab -e):
#   0 6 * * 1 /path/to/venv/bin/python /path/to/skill_adv/232/tools/knowledge_updater.py >> /var/log/ku_232.log 2>&1
#
# Windows Task Scheduler:
#   Action: "Start a program"
#   Program: C:\path\to\venv\Scripts\python.exe
#   Arguments: D:\Dungchan\skill_adv\232\tools\knowledge_updater.py
#   Trigger: Weekly, Monday, 06:00
#
# Docker (optional — mount the skill_adv directory):
#   docker run --rm -v D:/Dungchan/skill_adv:/app urban-ag-skill python /app/232/tools/knowledge_updater.py
