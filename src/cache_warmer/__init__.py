from pathlib import Path

__title__ = "price_updater"
__copyright__ = "© 2024 samslensstudio"


def get_src_root_path() -> Path:
    """
    To load files from multiple locations (modules) there is the need
    to have a root folder path to the daprep module location.
    :return:
    """
    return Path(__file__).parent


def get_prj_root_path() -> Path:
    """
    To load files from multiple locations (modules) there is the need
    to have a root folder path to the daprep module location.
    :return:
    """
    return Path(__file__).parent.parent.parent
