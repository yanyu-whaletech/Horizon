"""Accelerator / startup directory scraper.

Fetches company directories that expose a JSON API (no RSS) and emits newly
listed companies as ContentItems. Cross-run de-dup (data/seen.json, keyed on
item id) means each company surfaces only once, so most runs add nothing —
only newly listed companies flow through and get scored.

Providers:
- "yc"       -> Y Combinator batch JSON (yc-oss mirror); each url is a batch file
- "speedrun" -> a16z Speedrun companies API; url[0] is the API base
"""

import logging
from datetime import datetime, timezone
from typing import List

import httpx

from .base import BaseScraper
from ..models import CompanySourceConfig, ContentItem, SourceType

logger = logging.getLogger(__name__)


class CompaniesScraper(BaseScraper):
    """Scraper for accelerator/startup company directories backed by JSON APIs."""

    def __init__(
        self, sources: List[CompanySourceConfig], http_client: httpx.AsyncClient
    ):
        super().__init__({"sources": sources}, http_client)

    async def fetch(self, since: datetime) -> List[ContentItem]:
        items: List[ContentItem] = []
        for src in self.config["sources"]:
            if not src.enabled:
                continue
            try:
                if src.provider == "yc":
                    items.extend(await self._fetch_yc(src))
                elif src.provider == "speedrun":
                    items.extend(await self._fetch_speedrun(src))
                else:
                    logger.warning("Unknown companies provider: %s", src.provider)
            except Exception as e:  # noqa: BLE001 - never let one source break the run
                logger.warning("Error fetching companies source %s: %s", src.name, e)
        return items

    @staticmethod
    def _launched_at(row: dict) -> int:
        try:
            return int(row.get("launched_at") or 0)
        except (TypeError, ValueError):
            return 0

    @staticmethod
    def _safe_url(candidate: str, fallback: str) -> str:
        """Return candidate only if it's an http(s) URL, else the fallback."""
        c = (candidate or "").strip()
        return c if c.startswith("http://") or c.startswith("https://") else fallback

    async def _fetch_yc(self, src: CompanySourceConfig) -> List[ContentItem]:
        rows: List[dict] = []
        for url in src.urls:
            try:
                resp = await self.client.get(url, follow_redirects=True, timeout=20.0)
                resp.raise_for_status()
                data = resp.json()
            except Exception as e:  # noqa: BLE001
                logger.warning("YC batch fetch failed %s: %s", url, e)
                continue
            if isinstance(data, list):
                rows.extend(data)
            elif isinstance(data, dict):
                rows.extend(data.get("companies") or data.get("results") or [])

        # Most-recently-launched first, then cap (de-dup surfaces only new ones).
        rows.sort(key=self._launched_at, reverse=True)
        rows = rows[: src.max_items]

        items: List[ContentItem] = []
        for r in rows:
            name = (r.get("name") or "").strip()
            if not name:
                continue
            one = (r.get("one_liner") or "").strip()
            desc = (r.get("long_description") or "").strip()
            batch = (r.get("batch") or "").strip()
            industry = (r.get("industry") or "").strip()
            tags = r.get("tags") if isinstance(r.get("tags"), list) else []
            slug = str(r.get("slug") or r.get("id") or name)
            website = (r.get("website") or r.get("url") or "").strip()
            url = self._safe_url(website, f"https://www.ycombinator.com/companies/{slug}")

            parts = [f"Y Combinator {batch} startup: {name}"]
            if one:
                parts.append(f"One-liner: {one}")
            if industry:
                parts.append(f"Industry: {industry}")
            if tags:
                parts.append(f"Tags: {', '.join(str(t) for t in tags)}")
            if desc:
                parts.append("")
                parts.append(desc)

            title = f"{name}（YC {batch}）：{one}" if one else f"{name}（YC {batch}）"
            try:
                items.append(
                    ContentItem(
                        id=self._generate_id("companies", "yc", slug),
                        source_type=SourceType.COMPANIES,
                        title=title,
                        url=url,
                        content="\n".join(parts),
                        author=f"Y Combinator {batch}".strip(),
                        published_at=datetime.now(timezone.utc),
                        metadata={
                            "provider": "yc",
                            "batch": batch,
                            "industry": industry,
                            "tags": tags,
                            "category": src.category,
                            "feed_name": f"YC {batch}".strip() or "Y Combinator",
                        },
                    )
                )
            except Exception as e:  # noqa: BLE001 - skip a single bad row
                logger.debug("Skipping YC company %s: %s", name, e)
        return items

    async def _fetch_speedrun(self, src: CompanySourceConfig) -> List[ContentItem]:
        base = (
            src.urls[0]
            if src.urls
            else "https://speedrun.a16z.com/api/companies/companyparams"
        )
        page = 100
        offset = 0
        rows: List[dict] = []
        # Fetch the full directory (fast HTTP) so we can pick the newest cohort.
        while True:
            url = f"{base}?offset={offset}&limit={page}&team_size_min=1&ordering=name"
            try:
                resp = await self.client.get(url, follow_redirects=True, timeout=20.0)
                resp.raise_for_status()
                data = resp.json()
            except Exception as e:  # noqa: BLE001
                logger.warning("Speedrun fetch failed %s: %s", url, e)
                break
            results = data.get("results") if isinstance(data, dict) else data
            if not results:
                break
            rows.extend(results)
            if not (isinstance(data, dict) and data.get("next")) or len(rows) >= 1000:
                break
            offset += page

        # Keep only the newest cohort(s) — that is what "new companies" means and
        # it bounds how many we score. Cohorts look like "SR003" (zero-padded),
        # so a reverse string sort gives newest first.
        cohorts = sorted(
            {(r.get("cohort") or "").strip() for r in rows if r.get("cohort")},
            reverse=True,
        )
        if cohorts:
            keep = set(cohorts[: max(1, src.cohorts)])
            rows = [r for r in rows if (r.get("cohort") or "").strip() in keep]
        collected = rows[: src.max_items]

        items: List[ContentItem] = []
        for r in collected:
            name = (r.get("name") or "").strip()
            if not name:
                continue
            desc = (r.get("description") or r.get("preamble") or "").strip()
            cohort = (r.get("cohort") or "").strip()
            industries = r.get("industries")
            if isinstance(industries, list):
                ind_str = ", ".join(str(x) for x in industries)
            else:
                ind_str = str(industries or "").strip()
            slug = str(r.get("slug") or r.get("id") or name)
            website = (r.get("website_url") or "").strip()
            url = self._safe_url(website, f"https://speedrun.a16z.com/company/{slug}")

            parts = [f"a16z Speedrun {cohort} startup: {name}"]
            if ind_str:
                parts.append(f"Industries: {ind_str}")
            if desc:
                parts.append("")
                parts.append(desc)

            short = (desc[:80] + "…") if len(desc) > 80 else desc
            title = (
                f"{name}（a16z Speedrun {cohort}）：{short}"
                if short
                else f"{name}（a16z Speedrun {cohort}）"
            )
            try:
                items.append(
                    ContentItem(
                        id=self._generate_id("companies", "speedrun", slug),
                        source_type=SourceType.COMPANIES,
                        title=title,
                        url=url,
                        content="\n".join(parts),
                        author=f"a16z Speedrun {cohort}".strip(),
                        published_at=datetime.now(timezone.utc),
                        metadata={
                            "provider": "speedrun",
                            "cohort": cohort,
                            "category": src.category,
                            "feed_name": f"a16z Speedrun {cohort}".strip()
                            or "a16z Speedrun",
                        },
                    )
                )
            except Exception as e:  # noqa: BLE001 - skip a single bad row
                logger.debug("Skipping Speedrun company %s: %s", name, e)
        return items
