import os
import re
import asyncio
from urllib.parse import urlparse

import aiohttp
from selectolax.parser import HTMLParser


class FuckingFastDownloader:
    allowed_domains = ["fuckingfast.co"]

    def __init__(self, input_file="links.txt", output_file="links_output.txt"):
        self.input_file = input_file
        self.output_file = output_file

        if not os.path.exists(self.input_file):
            open(self.input_file, "w").close()

        open(self.output_file, "w").close()

    async def get_fuckingfast_link(self, session, download_url):
        headers = {
            "user-agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 17_7 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) CriOS/134.0.6998.99 Mobile/15E148 Safari/604.1",
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
            tasks = [
                self.get_fuckingfast_link(session, url) if "fuckingfast.co" in urlparse(url).netloc else None
                for url in map(str.strip, urls)
                if url
            ]
            return await asyncio.gather(*tasks)

    def extract_valid_links(self, content):
        tree = HTMLParser(content)
        return [
            a.attributes["href"]
            for a in tree.css("a")
            if (href := a.attributes.get("href")) and any(domain in href for domain in self.allowed_domains)
        ]

    def run(self):
        with open(self.input_file, "r", encoding="utf-8") as file:
            content = file.read()
            urls = self.extract_valid_links(content) or content.strip().splitlines()

        if not urls:
            print("[!] No valid links found in links.txt.")
            return

        download_links = asyncio.run(self.process_links(urls))

        with open(self.output_file, "w", encoding="utf-8") as output_file:
            total = sum(1 for link in download_links if link and output_file.write(link + "\n"))

        print(f"[*] Done generating download links! {total} links found.")


if __name__ == "__main__":
    FuckingFastDownloader().run()
    os.system("pause")
