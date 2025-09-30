import re
import cloudscraper
from selectolax.parser import HTMLParser


class Pixeldrain:
    def __init__(self):
        self.allowed_domains = ["pixeldrain.com"]
        self.scraper = cloudscraper.create_scraper()
        self.bypass_url = "https://pd.cybar.xyz/"

    def get_direct_link(self, download_url: str) -> str | list[str] | None:
        """
        Convert Pixeldrain file or gallery link to bypass direct link(s).

        Args:
            download_url (str): Original Pixeldrain link (file or gallery)

        Returns:
            str | list[str] | None:
                - Direct bypass URL (if single file)
                - List of bypass URLs (if gallery)
                - None if parsing failed
        """
        # Case 1: Single file
        if "/u/" in download_url:
            file_id = download_url.split("/u/")[-1]
            return f"{self.bypass_url}{file_id}"

        # Case 2: Gallery list
        if "/l/" in download_url:
            try:
                resp = self.scraper.get(download_url)
                if resp.status_code != 200:
                    return None

                tree = HTMLParser(resp.text)
                links = []

                # Gallery links have "a.file" selector
                for a in tree.css("a.file"):
                    bg_div = a.css_first("div")
                    if not bg_div:
                        continue

                    # Extract ID from background-image url
                    style = bg_div.attributes.get("style", "")
                    match = re.search(r"/api/file/(\w+)/", style)
                    if match:
                        file_id = match.group(1)
                        links.append(f"{self.bypass_url}{file_id}")

                return links if links else None
            except Exception as e:
                print(f"[Pixeldrain] Gallery parsing error: {e}")
                return None

        # Case 3: Zip file info
        if "/api/file/" in download_url and "/zip/" in download_url:
            zip_suffix = download_url.replace("https://pixeldrain.com/api/file/", "")
            return f"{self.bypass_url}{zip_suffix}"

        return None
