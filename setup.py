#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Distribution setup."""

import sys
import re
import setuptools

from pathlib import Path

try:
    import distribute_setup

    distribute_setup.use_setuptools()
except ImportError:
    pass

# Get long description from README.md
with Path("README.md").open("r") as dfh:
    long_description = dfh.read()  # pylint: disable=C0103

# parse version from package/module without importing or
# evaluating the code
with Path("lptwitdelete/__init__.py").open() as ifh:
    for line in ifh:
        # The escaping/use of quotes in the re.search() below can be treacherous
        match = re.search(r'^__version__ = "(?P<version>[^"]+)"$', line)
        if match:
            version = match.group("version")
            break

if sys.version_info <= (3, 6):
    sys.stderr.write("ERROR: lptwitdelete requires Python 3.7 or above...exiting.\n")
    sys.exit(1)

setuptools.setup(
    name="lptwitdelete",
    version=version,
    author="Leighton Pritchard",
    author_email="leighton.pritchard@strath.ac.uk",
    description="".join([("lptwitdelete is a package for managing personal digital hygiene on Twitter")]),
    long_description=long_description,
    long_description_content_type="text/markdown",
    license="MIT",
    keywords="Twitter",
    platforms="Posix; MacOS X",
    url="http://widdowquinn.github.io/lptwitdelete/",  # project home page
    download_url="https://github.com/widdowquinn/lptwitdelete/releases",
    scripts=[],
    entry_points={
        "console_scripts": ["lptwitdelete = lptwitdelete.lptwitdelete:main", "lptd = lptwitdelete.lptwitdelete:main"]
    },
    packages=setuptools.find_packages(),
    package_data={},
    include_package_date=True,
    install_requires=["tweepy", "tqdm",],
    classifiers=[
        "Development Status :: 4 - Beta",
        "Environment :: Console",
        "Intended Audience :: Science/Research",  # CHANGEME
        "License :: OSI Approved :: MIT License",
        "Natural Language :: English",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: POSIX :: Linux",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Topic :: Scientific/Engineering :: Bio-Informatics",  # CHANGEME
    ],
)
