import logging

from pyhocon import ConfigFactory, ConfigTree

from cache_warmer import get_src_root_path


class ConfigurationLoader:
    """
    A configuration loader
    """

    def __init__(self, logger: logging.Logger):
        self.logger = logger

    def load_config_relative_from_root(
        self, config_file_path: str = "default.conf"
    ) -> ConfigTree:
        """
        Load data by config file path relative from root folder.

        :param config_file_path: The config filepath.
        :return: A config file tree.
        """
        src_root_path = get_src_root_path()
        config_file_path = src_root_path.joinpath(f"{config_file_path}")

        self.logger.info(f"Loading configuration from {config_file_path}")
        config: ConfigTree = ConfigFactory.parse_file(config_file_path)
        self.logger.info(f"Loaded configuration from {config_file_path}")

        return config

    def load_config_absolute(
        self, config_file_path: str = "default.conf"
    ) -> ConfigTree:
        """
        Load data by config file path with an absolute filepath.

        :param config_file_path: The config filepath.
        :return: A config file tree.
        """
        self.logger.info(f"Loading configuration from {config_file_path}")
        config = ConfigFactory.parse_file(config_file_path)
        self.logger.info(f"Loaded configuration from {config_file_path}")
        return config
