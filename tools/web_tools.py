import httpx
from typing import Any, Optional
from urllib.parse import quote_plus


class WebTool:
    name = "web"
    description = "Search the web or fetch a URL's content."

    def __call__(self, action: str, query: str = "", url: str = "") -> str:
        if action == "search":
            return self._search(query)
        elif action == "fetch":
            return self._fetch(url)
        return "Unknown action. Use 'search' or 'fetch'."

    def _search(self, query: str) -> str:
        encoded = quote_plus(query)
        search_url = f"https://html.duckduckgo.com/html/?q={encoded}"
        try:
            r = httpx.get(search_url, timeout=15, follow_redirects=True, headers={
                "User-Agent": "Mozilla/5.0 (Pallas Agent)"
            })
            from html.parser import HTMLParser

            class TextExtractor(HTMLParser):
                def __init__(self):
                    super().__init__()
                    self.texts = []
                    self._in_result = False

                def handle_data(self, data):
                    t = data.strip()
                    if t:
                        self.texts.append(t)

            parser = TextExtractor()
            parser.feed(r.text)
            snippets = [t for t in parser.texts if len(t) > 30][:20]
            return "\n".join(snippets) if snippets else "No results found."
        except Exception as e:
            return f"Search error: {e}"

    def _fetch(self, url: str) -> str:
        try:
            r = httpx.get(url, timeout=20, follow_redirects=True, headers={
                "User-Agent": "Mozilla/5.0 (Pallas Agent)"
            })
            from html.parser import HTMLParser

            class TextExtractor(HTMLParser):
                def __init__(self):
                    super().__init__()
                    self.result = []
                    self._skip = False

                def handle_starttag(self, tag, attrs):
                    if tag in ("script", "style", "nav", "footer"):
                        self._skip = True

                def handle_endtag(self, tag):
                    if tag in ("script", "style", "nav", "footer"):
                        self._skip = False

                def handle_data(self, data):
                    if not self._skip:
                        t = data.strip()
                        if t:
                            self.result.append(t)

            p = TextExtractor()
            p.feed(r.text)
            return "\n".join(p.result)[:6000]
        except Exception as e:
            return f"Fetch error: {e}"
