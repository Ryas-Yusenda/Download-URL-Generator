import os
import asyncio
from urllib.parse import urlparse
from hashlib import sha256

import time
import requests


class GofileDirectDownloader:
    allowed_domains = ["gofile.io"]

    def __init__(self, input_file="links.txt", output_file="links_output.txt"):
        self.input_file = input_file
        self.output_file = output_file

        if not os.path.exists(self.input_file):
            open(self.input_file, "w").close()

        open(self.output_file, "w").close()

    def get_direct_gofile_link(self, token: str, shared_url: str, password: str | None = None) -> str | None:
        try:
            content_id = shared_url.strip("/").split("/")[-1]

            # Get the direct download link
            headers = {
                "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.3",
                "Authorization": f"Bearer {token}",
                "Accept-Encoding": "gzip, deflate, br",
                "Accept": "*/*",
                "Connection": "keep-alive",
            }
            api_url = f"https://api.gofile.io/contents/{content_id}?wt=4fd6sg89d7s6&cache=true&sortField=createTime&sortDirection=1"
            if password:
                hashed_pw = sha256(password.encode()).hexdigest()
                api_url += f"&password={hashed_pw}"

            resp = requests.get(api_url, headers=headers, timeout=30)
            resp.raise_for_status()
            data = resp.json()

            if data["status"] != "ok":
                print("[!] Error fetching data for link:", shared_url, "Status:", data["status"])
                return None

            # Process the response to find the direct download link
            item = data["data"]
            if item["type"] == "file":
                return item["link"]
            else:
                children = item["children"]
                if children:
                    first_file = next((v for v in children.values() if v["type"] == "file"), None)
                    return first_file["link"] if first_file else None
        except Exception as e:
            print("[!] Error processing link:", shared_url, "Error:", e)
            return None

    def get_account_token(self):
        headers = {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.3",
            "Accept-Encoding": "gzip, deflate, br",
            "Accept": "*/*",
            "Connection": "keep-alive",
        }
        api_url = "https://api.gofile.io/accounts"

        resp = requests.post(api_url, headers=headers, timeout=30)
        resp.raise_for_status()
        token = resp.json()["data"]["token"]
        if token:
            print(f"[*] Account token obtained: {token}")
        return token

    async def process_links(self, urls):
        results = []

        # Get an account token
        token = self.get_account_token()

        if not token:
            print("[!] Failed to get account token.")
            return results

        for url in map(str.strip, urls):
            if not url:
                continue

            domain = urlparse(url).netloc
            if any(domain.endswith(d) for d in self.allowed_domains):
                result = self.get_direct_gofile_link(token, url)
                results.append(result)
                time.sleep(1)
            else:
                results.append(None)
        return results

    def run(self):
        with open(self.input_file, "r", encoding="utf-8") as file:
            urls = file.read().strip().splitlines()

        if not urls:
            print("[!] No valid links found in links.txt.")
            return

        download_links = asyncio.run(self.process_links(urls))

        with open(self.output_file, "w", encoding="utf-8") as output_file:
            total = sum(1 for link in download_links if link and output_file.write(link + "\n"))

        print(f"[*] Done generating direct download links! {total} links found.")


if __name__ == "__main__":
    GofileDirectDownloader().run()
    os.system("pause")
