import asyncio
from urllib.parse import urlparse
from selectolax.parser import HTMLParser
import aiohttp
import os

class Process:
    def __init__(self):
        self.input_file = "links.txt"
        self.output_file = "links_output.txt"
        
    async def _process_links(self, urls):
        async with aiohttp.ClientSession() as session:
            coroutines = [
                self.get_direct_link(session, url)
                for url in map(str.strip, urls)
                if url
            ]
            return await asyncio.gather(*coroutines)

    def _extract_valid_links(self, content):
        tree = HTMLParser(content)
        links = [a.attributes["href"] for a in tree.css("a") if a.attributes.get("href")]

        if not links:
            content = content.strip().splitlines()
            links = [line for line in content if line.strip() and "http" in line]

        def normalize_domain(url):
            netloc = urlparse(url).netloc
            return netloc[4:] if netloc.startswith("www.") else netloc

        return [url for url in links if normalize_domain(url) in self.allowed_domains]

    def _start_processing(self, urls):
        if not urls:
            print("[!] No valid links found in links.txt.")
            return []

        download_links = asyncio.run(self._process_links(urls))
        return self._save_download_links(download_links)
        
    def _save_download_links(self, download_links):
        download_links = [link for link in download_links if link]
        total = len(download_links)
        
        if total > 0:
            with open(self.output_file, "w", encoding="utf-8") as output_file:
                for link in download_links:
                    output_file.write(link + "\n")
            print(f"[*] Done generating download links! {total} links found.")
            return download_links
        else:
            print("[!] No valid download links found.")

    def run(self):
        with open(self.input_file, "r", encoding="utf-8") as file:
            content = file.read()
            urls = self._extract_valid_links(content)
            
        self._start_processing(urls)
        os.system("pause")
        

