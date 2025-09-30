import asyncio
from urllib.parse import urlparse
import aiohttp
import os
import re

import importlib.util
import subprocess
import sys

# Import all available downloaders (add new ones here when needed)
from downloader.buzzheavier import Buzzheavier
from downloader.fuckingfast import FuckingFast
from downloader.mediafire import Mediafire
from downloader.pixeldrain import Pixeldrain


class DependencyManager:
    """
    Ensures required dependencies are installed with specific versions.
    If a package is missing or wrong version, it will be installed/upgraded.
    """

    def __init__(self):
        # Define required packages and versions here
        self.required_packages = {
            "aiohttp": "3.12.15",
            "selectolax": "0.3.34",
            "cloudscraper": "1.2.71",
        }

    def _get_installed_version(self, package: str) -> str | None:
        """Check installed version of a package."""
        try:
            pkg = importlib.import_module(package)
            return getattr(pkg, "__version__", None)
        except ImportError:
            return None

    def _install_package(self, package: str, version: str):
        """Install or update a package to a specific version."""
        print(f"[*] Installing {package}=={version} ...")
        subprocess.check_call(
            [sys.executable, "-m", "pip", "install", f"{package}=={version}"]
        )

    def ensure(self):
        """Ensure all required packages with specific versions are installed."""
        for package, version in self.required_packages.items():
            installed_version = self._get_installed_version(package)
            if installed_version != version:
                print(
                    f"[!] {package} version mismatch "
                    f"(installed: {installed_version}, required: {version})"
                )
                self._install_package(package, version)
            else:
                # print(f"[✓] {package}=={version} already installed")
                continue

class Process:
    """
    Main processing class responsible for:
    - Reading URLs from `links.txt`
    - Matching each URL with the correct downloader handler (based on domain)
    - Executing the downloader to extract direct links
    - Saving results into `links_output.txt`
    """

    def __init__(self):
        self.input_file = "links.txt"
        self.output_file = "links_output.txt"

        # List of all available downloader classes
        downloaders = [Buzzheavier(), FuckingFast(), Mediafire(), Pixeldrain()]

        # Build handler mapping dynamically based on `allowed_domains`
        self.handlers = {}
        for d in downloaders:
            for domain in d.allowed_domains:
                self.handlers[domain] = d

    def _get_handler(self, url: str):
        """
        Select the appropriate handler based on the domain of the given URL.
        """
        netloc = urlparse(url).netloc
        domain = netloc[4:] if netloc.startswith("www.") else netloc
        return self.handlers.get(domain)

    def _extract_urls_from_file(self):
        """
        Extract all valid URLs from self.input_file using regex.
        Supports raw URLs and URLs embedded in HTML (e.g. <a href="...">).
        """
        if not os.path.exists(self.input_file):
            print(f"[!] Input file not found: {self.input_file}")
            return []

        with open(self.input_file, "r", encoding="utf-8") as file:
            content = file.read()

        # Regex to find all URLs (http/https)
        urls = re.findall(r"https?://[^\s'\"<>]+", content)
        return urls

    async def _process_links(self, urls):
        """
        Process a list of URLs asynchronously.
        - Uses aiohttp for async handlers
        - Falls back to run_in_executor for synchronous handlers
        """
        results = []
        async with aiohttp.ClientSession() as session:
            tasks = []
            for url in urls:
                handler = self._get_handler(url)
                if not handler:
                    print(f"[!] No handler found for: {url}")
                    continue

                # Async handler (e.g. Buzzheavier, FuckingFast)
                if asyncio.iscoroutinefunction(handler.get_direct_link):
                    tasks.append(handler.get_direct_link(session, url))
                else:
                    # Sync handler (e.g. Mediafire)
                    loop = asyncio.get_event_loop()
                    tasks.append(loop.run_in_executor(None, handler.get_direct_link, url))

            results = await asyncio.gather(*tasks)
        return results

    def _save_download_links(self, download_links):
        """
        Save valid download links into `links_output.txt`.
        """
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
        """
        Entry point for the process.
        - Extracts URLs from links.txt
        - Processes each link with the correct handler
        - Saves results into links_output.txt
        """
        urls = self._extract_urls_from_file()

        if not urls:
            print("[!] No valid links found in links.txt.")
            return

        print(f"[*] Processing {len(urls)} links...")
        download_links = asyncio.run(self._process_links(urls))
        self._save_download_links(download_links)
        os.system("pause")


if __name__ == "__main__":
    deps = DependencyManager()
    deps.ensure()

    from process import Process  # safe to import after deps check
    Process().run()
