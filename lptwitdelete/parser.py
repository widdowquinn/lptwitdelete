# -*- coding: utf-8 -*-
"""Parser for command-line API."""

import sys

from argparse import ArgumentParser, Namespace
from typing import List, Optional

from pathlib import Path


def build_parser() -> ArgumentParser:
    """Return parser for lptwitdelete command-line API."""
    parser = ArgumentParser()

    # Required positional arguments
    parser.add_argument(action="store", type=str, dest="username", default=None, help="Twitter username")

    # Optional arguments
    parser.add_argument(
        "-a", "--archpath", type=Path, dest="archpath", default=None, help="Path to Twitter archive file"
    )
    parser.add_argument(
        "--start_date", type=str, dest="start_date", default=None, help="Start date for deletion (YYYY-MM-DD)"
    )
    parser.add_argument(
        "--end_date", type=str, dest="end_date", default=None, help="End date for deletion (YYYY-MM-DD)"
    )
    parser.add_argument(
        "--is_retweet",
        dest="is_retweet",
        default=False,
        action="store_true",
        help="Only delete tweets that are retweets",
    )
    parser.add_argument(
        "-o", "--outfile", dest="outfile", type=Path, default=None, help="Write filtered tweets to this file",
    )
    parser.add_argument(
        "--is_reply", dest="is_reply", default=False, action="store_true", help="Only delete tweets that are replies",
    )

    parser.add_argument(
        "-c",
        "--confpath",
        type=Path,
        dest="confpath",
        default=Path.home() / ".twitter/lptwitdelete/conf.yml",
        help="Path to config file with API keys",
    )
    parser.add_argument(
        "-v", "--verbose", action="store_true", dest="verbose", default=False, help="report verbose progress to log",
    )
    parser.add_argument(
        "--debug", action="store_true", dest="debug", default=False, help="report debug messages to log",
    )
    parser.add_argument(
        "--delete", action="store_true", dest="delete", default=False, help="actually delete tweets from Twitter",
    )
    parser.add_argument(
        "--skip_auth",
        action="store_true",
        dest="skip_auth",
        default=False,
        help="skip Twitter OAuth (e.g. for searching archive)",
    )
    parser.add_argument(
        "-l", "--logfile", dest="logfile", action="store", default=None, type=Path, help="logfile location",
    )
    return parser


def parse_cmdline(argv: Optional[List] = None) -> Namespace:
    """Parse command-line arguments for lptwitdelete.

    :param argv:  list of comand-line arguments
    """
    parser = build_parser()

    if argv is None:
        argv = sys.argv[1:]
    return parser.parse_args([str(_) for _ in argv])
