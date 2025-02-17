import argparse

from cache_warmer.version import __version__


def parse_args(argv=None):
    parser = argparse.ArgumentParser(
        prog="cache_warmer",
        usage="A small program to warm the cache of thelittlegoldsmith.",
        description="The cache warmer of thelittlegoldsmith.",
        add_help=True,
        allow_abbrev=False,
    )
    parser.add_argument(
        "-c",
        "--config",
        type=str,
        dest="config_file_path",
        metavar="string",
        default=None,
        help="The config file path to run the cache_warmer."
        "I.e. 'src/cache_warmer/config/main.conf'",
    )
    parser.add_argument("-v", "--version", action="version", version=__version__)
    return parser.parse_args(argv)
