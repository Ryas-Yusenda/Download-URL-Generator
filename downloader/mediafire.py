import cloudscraper
from selectolax.parser import HTMLParser


class Mediafire:
    def __init__(self):
        self.allowed_domains = ["mediafire.com"]
        self.cloudscraper = cloudscraper.create_scraper()

    def get_direct_link(self, download_url: str) -> str | None:
        headers = {
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/140.0.0.0 Safari/537.36',
        }

        response = self.cloudscraper.get(download_url, headers=headers)
        tree = HTMLParser(response.text)


        # kalau kena proteksi cloudflare
        if "Just a moment..." in tree.html:
            print("[!] Detected by Cloudflare")
            return None

        match = tree.css_first("a#downloadButton[href^='https://download']")
        if match:
            return match.attributes.get("href", None)

        print(response.text)

        return None