import json
from datetime import datetime, timezone
from pathlib import Path

import feedparser

FEEDS = [
    {"name": "404 Media", "url": "https://www.404media.co/rss"},
    {"name": "Ahead of AI", "url": "https://magazine.sebastianraschka.com/feed"},
    {"name": "AI Accelerator Institute | Future of Artificial Intelligence", "url": "https://aiacceleratorinstitute.com/rss/"},
    {"name": "AI – AI-TechPark", "url": "https://ai-techpark.com/category/ai/feed/"},
    {"name": "AI Archives | KnowTechie", "url": "https://knowtechie.com/category/ai/feed/"},
    {"name": "AI Business", "url": "https://aibusiness.com/rss.xml"},
    {"name": "AIModels.fyi", "url": "https://aimodels.substack.com/feed"},
    {"name": "AI News", "url": "https://www.artificialintelligence-news.com/feed/rss/"},
    {"name": "AI News | VentureBeat", "url": "https://venturebeat.com/category/ai/feed/"},
    {"name": "AI Now Institute", "url": "https://ainowinstitute.org/category/news/feed"},
    {"name": "Ai Prompt Programming", "url": "https://www.reddit.com/r/aipromptprogramming/.rss"},
    {"name": "AI – SiliconANGLE", "url": "https://siliconangle.com/category/ai/feed"},
    {"name": "AI Snake Oil", "url": "https://aisnakeoil.substack.com/feed"},
    {"name": "AI – Uber Engineering Blog", "url": "https://eng.uber.com/category/articles/ai/feed"},
    {"name": "Anaconda Blog", "url": "https://www.anaconda.com/blog/feed"},
    {"name": "Analytics India Magazine", "url": "https://analyticsindiamag.com/feed/"},
    {"name": "Announcements - Stability AI", "url": "https://stability.ai/blog?format=rss"},
    {"name": "Ars Technica - All content", "url": "https://feeds.arstechnica.com/arstechnica/index"},
    {"name": "Artificial Intelligence", "url": "https://www.reddit.com/r/artificial/.rss"},
    {"name": "Artificial intelligence (AI) – The Conversation", "url": "https://theconversation.com/europe/topics/artificial-intelligence-ai-90/articles.atom"},
    {"name": "Artificial intelligence (AI) | The Guardian", "url": "https://www.theguardian.com/technology/artificialintelligenceai/rss"},
    {"name": "artificial intelligence Archives - SpaceNews", "url": "https://spacenews.com/tag/artificial-intelligence/feed/"},
    {"name": "Artificial Intelligence – Futurism", "url": "https://futurism.com/categories/ai-artificial-intelligence/feed"},
    {"name": "Artificial Intelligence Latest - Wired", "url": "https://www.wired.com/feed/tag/ai/latest/rss"},
    {"name": "Artificial Intelligence News -- ScienceDaily", "url": "https://www.sciencedaily.com/rss/computers_math/artificial_intelligence.xml"}
]

MAX_ITEMS = 5
USER_AGENT = "Mozilla/5.0 (compatible; ProPointsRSSFetcher/1.0; +https://bpmstc.github.io/ProPoints/)"

OUTPUT_PATH = Path("docs/assets/intro-to-ai/data/feeds.json")


def parse_entry(entry):
    title = entry.get("title", "Untitled").strip() if entry.get("title") else "Untitled"
    link = entry.get("link", "#").strip() if entry.get("link") else "#"
    date = entry.get("published") or entry.get("updated") or ""
    date = date.strip() if isinstance(date, str) else ""
    return {"title": title, "link": link, "date": date}


def build_feed_snapshot():
    results = []
    for feed in FEEDS:
        try:
            parsed = feedparser.parse(feed["url"], request_headers={"User-Agent": USER_AGENT})
            if parsed.bozo:
                raise RuntimeError(str(parsed.bozo_exception))
            entries = [parse_entry(entry) for entry in parsed.entries[:MAX_ITEMS]]
            results.append({
                "name": feed["name"],
                "url": feed["url"],
                "items": entries,
                "error": None
            })
        except Exception as exc:  # noqa: BLE001
            results.append({
                "name": feed["name"],
                "url": feed["url"],
                "items": [],
                "error": str(exc)
            })

    payload = {
        "generatedAt": datetime.now(timezone.utc).isoformat(),
        "feeds": results
    }

    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT_PATH.write_text(json.dumps(payload, indent=2), encoding="utf-8")


if __name__ == "__main__":
    build_feed_snapshot()
