import re
import asyncio
from urllib.parse import urlparse
import requests

import aiohttp
from selectolax.parser import HTMLParser

from process import Process

class Gofile(Process):
    def __init__(self):
        super().__init__() 
        self.allowed_domains = ["gofile.io"]
        self.token = '7sOpBGKyhOZJTEoeya1JMXyUXreN2naw' or self._get_token()
        self.wt = '4fd6sg89d7s6' or self._get_wt()

    def _get_token(self):
        resp = requests.post("https://api.gofile.io/accounts", timeout=30)
        token = resp.json()["data"]["token"]
        if token:
            print(f"[*] Account token obtained: {token}")
            self.token = token
        else:
            print("[!] Failed to obtain account token. Please check your network connection or API status.")
            exit(1)

    def _get_wt(self):
        js_file = requests.get("https://gofile.io/dist/js/global.js").text
        if 'appdata.wt = "' in js_file:
            wt = js_file.split('appdata.wt = "')[1].split('"')[0]
            self.wt = wt
        else:
            print("[!] Failed to extract wt from global.js. Please check the file structure.")
            exit(1)
        
    async def get_direct_link(self, session, download_url: str) -> str | None:        
        content_id = download_url.strip("/").split("/")[-1]
        password = None
        hash_password = sha256(password.encode()).hexdigest() if password != None else ""
        
        headers = {
            "Authorization": f"Bearer {self.token}",
        }
        
        download_url = f"https://api.gofile.io/contents/{content_id}?wt={self.wt}&cache=true&password={hash_password}"

        async with session.get(download_url, headers=headers) as response:
            json = await response.json()
            if json["status"] != "ok":
                print("[!] Error fetching data for link:", download_url, "Status:", json["status"])
                return None
            
            data = json["data"]
            if data["type"] == "file":
                return data["link"]
            else:
                children = data["children"]
                if children:
                    first_file = next((v for v in children.values() if v["type"] == "file"), None)
                    return first_file["link"] if first_file else None
        return None
    
if __name__ == "__main__":
    gofile =  Gofile()
    gofile.run()
