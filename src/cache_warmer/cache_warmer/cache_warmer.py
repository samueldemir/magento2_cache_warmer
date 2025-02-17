import asyncio
import logging
import xml.etree.ElementTree as ElementTree
from datetime import datetime
from typing import Any, Dict, List

import aiohttp
import requests


class SitemapRetriever:
    """
    A class to retrieve sitemaps from a URL.
    """

    def __init__(self, sitemap_address):
        self.sitemap_address = sitemap_address

    def get_urls(self):
        """
        This function retrieves the relevant magento urls from an xml file.
        :return:
        """
        response = requests.get(self.sitemap_address)
        response.raise_for_status()
        xml_content = response.text

        # Parse the XML content
        urls = []
        root = ElementTree.fromstring(xml_content)
        namespace = {"ns": "http://www.sitemaps.org/schemas/sitemap/0.9"}
        for url in root.findall("ns:url", namespace):
            loc = url.find("ns:loc", namespace).text
            urls.append(loc)

        return urls


class CacheWarmer:
    """
    A class to warm the cache of a website.
    """

    def __init__(
        self,
        logger: logging.Logger,
        name: str,
        sitemap_retriever: SitemapRetriever,
        rate: int = 10,
        semaphore: int = 10,
        fetch_first: int = None,
    ):
        self.logger = logger
        self.name = name
        self.sitemap_retriever = sitemap_retriever
        self.rate = rate
        self.semaphore = asyncio.Semaphore(semaphore)
        self.fetch_first = fetch_first

    async def fetch_url(self, url: str) -> Dict[str, Any]:
        """
        An async function to fetch an url.
        :param url: A specific url to call.
        :return: A Dict with the called url, the status, and the time where it got fired.
        """
        async with self.semaphore:
            async with aiohttp.ClientSession() as session:
                start_timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                async with session.get(url) as response:
                    await response.text()
                    status_code = response.status
                    self.logger.info(f"Made request: {url}. Status: {status_code}")
                    await asyncio.sleep(self.rate)
                    return {
                        "url": url,
                        "status_code": status_code,
                        "start_time": start_timestamp,
                    }

    async def fetch_all(self, urls) -> List[Dict[str, Any]]:
        """
        This function fecthes all urls.
        :param urls: A list of urls to fetch.
        :return: A list of results.
        """
        tasks = []
        for url in urls:
            task = self.fetch_url(url)
            tasks.append(task)
        results = await asyncio.gather(*tasks)
        return results

    def warm_cache(self) -> List[Dict[str, Any]]:
        """
        This function starts to run the cache warming.
        :return:
        """
        urls = self.sitemap_retriever.get_urls()
        if self.fetch_first:
            urls = urls[: self.fetch_first]
        results = asyncio.run(self.fetch_all(urls))
        return results
