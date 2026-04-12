import os
from firecrawl import Firecrawl

def scrape_website(url: str):
    api_key = os.getenv("FIRECRAWL_API_KEY")
    if not api_key:
        raise ValueError("FIRECRAWL_API_KEY is not set")

    app = Firecrawl(api_key=api_key)
    doc = app.scrape(url, formats=["markdown"])

    if hasattr(doc, "markdown"):
        return doc.markdown
    if isinstance(doc, dict) and "markdown" in doc:
        return doc["markdown"]

    raise ValueError("Could not extract website content")