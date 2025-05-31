import re
import asyncio
from urllib.parse import urlparse

import aiohttp
from selectolax.parser import HTMLParser

from process import Process

class FuckingFast(Process):
    def __init__(self):
        super().__init__() 
        self.allowed_domains = ["fuckingfast.co"]

    async def get_direct_link(self, session, download_url: str) -> str | None:
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
    
if __name__ == "__main__":
    fuckingfast = FuckingFast()
    fuckingfast.run()
