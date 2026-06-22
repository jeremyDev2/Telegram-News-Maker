from app.db.models import Source
from .rss import get_rss
from .html import scrape_html

def parse_site(source: Source) -> list[dict]:
    items = get_rss(source)
    if items:
        return items
    return scrape_html(source)
