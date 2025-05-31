import re
import asyncio
from urllib.parse import urlparse

import aiohttp
from selectolax.parser import HTMLParser


class FuckingFast:
    def __init__(self):
        self.allowed_domains = ["fuckingfast.co"]
        self.input_file = "links.txt"
        self.output_file = "links_output.txt"

    async def get_direct_link(self, session, download_url):
        headers = {
            "user-agent": (
                "Mozilla/5.0 (iPhone; CPU iPhone OS 17_7 like Mac OS X) "
                "AppleWebKit/605.1.15 (KHTML, like Gecko) "
                "CriOS/134.0.6998.99 Mobile/15E148 Safari/604.1"
            ),
            "accept-language": "en-US,en;q=0.9,id;q=0.8",
            "accept-encoding": "gzip, deflate, br",
            "accept": "text/html",
            "referer": "http://www.google.com/",
        }

        async with session.get(download_url, headers=headers) as response:
            tree = HTMLParser(await response.text())
            for script in tree.css("script"):
                if script.text():
                    match = re.search(r"https://fuckingfast.co/dl/[a-zA-Z0-9_-]+", script.text())
                    if match:
                        return match.group()
        return None

    async def process_links(self, urls):
        async with aiohttp.ClientSession() as session:
            coroutines = [
                self.get_direct_link(session, url)
                for url in map(str.strip, urls)
                if url
            ]
            return await asyncio.gather(*coroutines)

    def extract_valid_links(self, content):
        tree = HTMLParser(content)
        links = [a.attributes["href"] for a in tree.css("a") if a.attributes.get("href")]
        if not links:
            content = content.strip().splitlines()
            links = [line for line in content if line.strip() and "http" in line]
        return links

    def start_processing(self, urls):
        if not urls:
            print("[!] No valid links found in links.txt.")
            return []

        print("[*] Extracting download links from fuckingfast.co...")
        urls = [url for url in urls if urlparse(url).netloc in self.allowed_domains]

        download_links = asyncio.run(self.process_links(urls))
        total = sum(1 for link in download_links)
        
        with open(self.output_file, "w", encoding="utf-8") as output_file:
            for link in download_links:
                output_file.write(link + "\n")
        print(f"[*] Done generating download links! {total} links found.")
        return download_links

    def run(self):
        with open(self.input_file, "r", encoding="utf-8") as file:
            content = file.read()
            urls = self.extract_valid_links(content)
            
        download_links = self.start_processing(urls)
        return download_links


if __name__ == "__main__":
    fuckingfast = FuckingFast()
    fuckingfast.run()
