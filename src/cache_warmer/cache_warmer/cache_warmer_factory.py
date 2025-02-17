import logging
from typing import List

from pyhocon import ConfigTree

from cache_warmer.cache_warmer.cache_warmer import CacheWarmer, SitemapRetriever


class CacheWarmerFactory:
    """
    A factory class to create a list of CacheWarmer.
    """

    def __init__(self, logger: logging.Logger, cache_warmers_configs: ConfigTree):
        self.logger = logger
        self.cache_warmers_configs = cache_warmers_configs

    def create(self) -> List[CacheWarmer]:
        """
        This function creates a list of cache_warmers.
        :return: A list of CacheWarmer objects.
        """
        cache_warmers = []
        for cache_warmer_name, sitemap_config in self.cache_warmers_configs.items():
            sitemap_address = sitemap_config["sitemap_address"]
            rate = int(sitemap_config["rate"])
            semaphore = int(sitemap_config["semaphore"])
            sitemap_retriever = SitemapRetriever(sitemap_address=sitemap_address)
            cache_warmers.append(
                CacheWarmer(
                    self.logger,
                    name=cache_warmer_name,
                    sitemap_retriever=sitemap_retriever,
                    rate=rate,
                    semaphore=semaphore,
                )
            )

        return cache_warmers
