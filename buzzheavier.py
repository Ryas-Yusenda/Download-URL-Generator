import re
import asyncio
from urllib.parse import urlparse
import requests

import aiohttp
from selectolax.parser import HTMLParser

from process import Process

class Buzzheavier(Process):
    def __init__(self):
        super().__init__() 
        self.allowed_domains = ["buzzheavier.com"]

    async def get_direct_link(self, session, download_url: str) -> str | None:
        download_url = download_url.strip() + '/download'
        headers = {
            "user-agent": (
                "Mozilla/5.0 (iPhone; CPU iPhone OS 17_7 like Mac OS X) "
                "AppleWebKit/605.1.15 (KHTML, like Gecko) "
                "CriOS/134.0.6998.99 Mobile/15E148 Safari/604.1"
            ),
            "accept-language": "en-US,en;q=0.9,id;q=0.8",
            "accept-encoding": "gzip, deflate, br",
            'hx-current-url': download_url,
            'hx-request': 'true',
            'referer': download_url
        }

        async with session.head(download_url, headers=headers) as response:
            response.raise_for_status()
            hx_redirect = response.headers.get('hx-redirect')
            if hx_redirect:
                return hx_redirect
            else:
                print("[!] No hx-redirect found in response headers.")
                return None
            
        return None
    
if __name__ == "__main__":
    buzzheavier =   Buzzheavier()
    buzzheavier.run()
