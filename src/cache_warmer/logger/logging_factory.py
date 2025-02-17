import logging
import sys
from pathlib import Path

from pyhocon import ConfigFactory


class LoggerFactory:
    def __init__(self):
        self.logger = logging.getLogger("cache_warmer")
        self.config = ConfigFactory.parse_file(f"{Path(__file__).parent}/logging.conf")

    def create(self) -> logging.Logger:
        """
        setup logging based on the configuration
        :param config: the parsed config tree
        """

        fmt = self.config.get("logging.format")
        stream_handler_name = self.config.get("logging.stream_handler_name")
        if self.config.get_bool("logging.enabled"):
            level = logging._nameToLevel[self.config.get("logging.level").upper()]
        else:
            level = logging.NOTSET
        formatter = logging.Formatter(fmt)
        logging.basicConfig(format=fmt, level=logging.INFO)
        self.logger.setLevel(level)
        self.logger.propagate = False
        self._add_stream_handler_if_not_exists(
            stream_handler_name=stream_handler_name, formatter=formatter
        )
        self.logger.info(f"Logger successfully created and configured.")
        return self.logger

    def _add_stream_handler_if_not_exists(
        self,
        stream_handler_name: str,
        formatter: logging.Formatter = None,
    ):
        """
        Check if a stream handler already exists. If not add a stream handler.
        :return:
        """

        log_handlers = self.logger.handlers

        stream_handler_exists = False
        for handler in log_handlers:
            # can only be checked using stream handler name
            if handler.name != stream_handler_name:
                continue
            stream_handler_exists = True

        if not stream_handler_exists:
            stream_handler = logging.StreamHandler(sys.stdout)
            stream_handler.name = stream_handler_name
            if formatter is not None:
                stream_handler.setFormatter(formatter)
            self.logger.addHandler(stream_handler)
