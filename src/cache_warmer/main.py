from typing import Dict, List

import requests

from cache_warmer.argparser import parse_args
from cache_warmer.cache_warmer.cache_warmer import CacheWarmer
from cache_warmer.cache_warmer.cache_warmer_factory import CacheWarmerFactory
from cache_warmer.config.config_loader import ConfigurationLoader
from cache_warmer.logger.logging_factory import LoggerFactory


def main(argv=None):
    """
    Main function.
    :return:
    """
    args = parse_args(argv)
    logger = _build_logger()
    logger.info(f"Running with Args {args}")

    config_file_path = args.config_file_path
    if config_file_path is None:
        config_file_path = "config/config.conf"
    config_loader = ConfigurationLoader(logger)
    config = config_loader.load_config_relative_from_root(
        config_file_path=config_file_path
    )

    cache_warmers_configs = config.get("cache_warmers")
    cache_warmer_factory = CacheWarmerFactory(
        logger=logger, cache_warmers_configs=cache_warmers_configs
    )
    cache_warmers = cache_warmer_factory.create()
    run_cache_warmers(cache_warmers)


def health_check(argv=None):
    """
    Main function of the health checker.
    :return:
    """
    args = parse_args(argv)
    logger = _build_logger()
    logger.info(f"Running with Args {args}")

    config_file_path = args.config_file_path
    if config_file_path is None:
        config_file_path = "config/health_check_config.conf"
    config_loader = ConfigurationLoader(logger)
    config = config_loader.load_config_relative_from_root(
        config_file_path=config_file_path
    )

    teams_webhook = config.get("teams_webhook")
    if teams_webhook["active"]:
        webhook_url = teams_webhook["teams_webhook_url"]
        cache_warmers_configs = config.get("cache_warmers")
        cache_warmer_factory = CacheWarmerFactory(
            logger=logger, cache_warmers_configs=cache_warmers_configs
        )
        cache_warmers = cache_warmer_factory.create()
        for cache_warmer in cache_warmers:
            cache_warmer.fetch_first = 5

        prev_status = "healthy"
        msg_healthy = "cache_warmer_status: healthy"
        send_teams_alert(webhook_url, msg_healthy)
        while True:
            results = run_cache_warmers(cache_warmers)
            health_checks_failed, new_status = get_health_information(results)
            if new_status != prev_status:
                if new_status == "healthy":
                    send_teams_alert(webhook_url, msg_healthy)
                else:
                    msg = ""
                    for failed_health_check in health_checks_failed.values():
                        msg += failed_health_check + "\n"
                    send_teams_alert(webhook_url, msg)
            prev_status = new_status
            time.sleep(300)


def get_health_information(results: Dict) -> Tuple[Dict, str]:
    health_checks_failed = {}
    health_status_overall = "healthy"
    for cache_warmer_name, cache_warmer_result in results.items():
        items = []
        for result in cache_warmer_result:
            status_code = result["status_code"]
            url = result["url"]
            if status_code != 200:
                items.append(f"{url} ({status_code})")
        if len(items) > 0:
            health_status_overall = "unhealthy"
            health_checks_failed[cache_warmer_name] = (
                cache_warmer_name + f" ({health_status_overall}):" + "<br>" + "<br>".join(items) + "<br><br>"
            )

    return health_checks_failed, health_status_overall


def send_teams_alert(webhook_url, msg):
    """
    Sending a teams alert.
    :param webhook_url:
    :param msg:
    :return:
    """
    payload = {"text": msg}
    requests.post(webhook_url, json=payload)


def run_cache_warmers(cache_warmers: List[CacheWarmer]) -> Dict[str, List]:
    """
    Run the cache warmers in a loop.
    :param cache_warmers: A list of cache_warmers.
    :return: The result contains information about cache_warmer_name, url, status_code and time.
    """
    results = {}
    for cache_warmer in cache_warmers:
        result = cache_warmer.warm_cache()
        results[cache_warmer.name] = result

    return results


def _build_logger():
    logger_factory = LoggerFactory()
    logger = logger_factory.create()
    return logger
