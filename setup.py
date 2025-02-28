import os
import shutil
import subprocess
from pathlib import Path
from runpy import run_path
from typing import List

from setuptools import Command, find_packages, setup

# read the program version from version.py (without loading the module)
__version__ = run_path("src/cache_warmer/version.py")["__version__"]


def read(fname):
    """Utility function to read the README file."""
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


def read_requirements(file_path: Path) -> List[str]:
    """
    This function reads the requirements and passes it to the setup.

    :param file_path: The filepath where
    :return: A list of requirements.
    """
    # read the requirements and add them to install_requires
    with open(file_path, "r") as f:
        requirements = f.read().split("\n")
        requirements.remove("")
    return requirements


class DistCommand(Command):
    description = "build the distribution packages (in the 'dist' folder)"
    user_options = [("buildid=", "b", "buildid to add to the artifacts")]

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        if os.path.exists("build"):
            shutil.rmtree("build")
        subprocess.run(["python", "setup.py", "sdist", "bdist_wheel"])


setup(
    name="cache_warmer",
    version=__version__,
    author="Samuel Demir",
    author_email="demir.samuel@outlook.de",
    description="A cache warmer for magento2.",
    license="proprietary",
    url="",
    packages=find_packages("src"),
    package_dir={"": "src"},
    package_data={"cache_warmer": ["config/*", "logger/*"]},
    long_description=read("README.md"),
    install_requires=read_requirements(Path("requirements.txt")),
    cmdclass={
        "dist": DistCommand,
    },
    platforms="any",
    python_requires="~=3.11",
)
