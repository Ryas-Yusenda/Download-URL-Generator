import re

import cloudscraper
from selectolax.parser import HTMLParser

from process import Process

class Mediafire(Process):
    def __init__(self):
        super().__init__() 
        self.allowed_domains = ["mediafire.com"]
        self.cloudscraper = cloudscraper.create_scraper()
        
    def _start_processing(self, urls):
        if not urls:
            print("[!] No valid links found in links.txt.")
            return []

        download_links = [self.get_direct_link(url) for url in map(str.strip, urls) if url]
        return self._save_download_links(download_links)

    def get_direct_link(self, download_url: str) -> str | None:
        response = self.cloudscraper.get(download_url)
        tree = HTMLParser(response.text)
            
        # if contain (Just a moment by Cloudflare) return None
        if "Just a moment..." in tree.html:
            print("[!] Detected by Cloudflare")
            return None
        
        match = tree.css_first("a#downloadButton[href^='https://download']")
        if match:
            return match.attributes.get("href", None)

        return None
    
if __name__ == "__main__":
    mediafire = Mediafire()
    mediafire.run()
