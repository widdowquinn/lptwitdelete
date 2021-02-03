# -*- coding: utf-8 -*-
"""lptwitdelete script entry point."""

import json
import logging
import sys
import time

from typing import List, Optional

from lptwitdelete.archive import load_filter_archive
from lptwitdelete.config import Config
from lptwitdelete.logger import config_logger
from lptwitdelete.parser import parse_cmdline
from lptwitdelete.twitter import delete_tweets, filter_twitter, oauth_login


def main(argv: Optional[List[str]] = None):
    """Main entry point for lptwitdelete.

    :param argv:  arguments from command line
    """
    # Process command-line arguments
    args = parse_cmdline(argv)

    # Set up logging
    time0 = time.time()
    logger = logging.getLogger(__name__)
    config_logger(args)

    # Authenticate with Twitter
    if args.skip_auth:
        logger.warning("Skipping OAuth with Twitter!")
        api = None
    else:
        keys = Config(args.username, args.confpath)
        api = oauth_login(keys.CONSUMER_KEY, keys.CONSUMER_SECRET)
        logger.info("Authenticated with Twitter as %s", api.me().screen_name)

    # If archive file is supplied, load tweets into memory; any filtering on command-line
    # terms is performed in the load_filter_archive() call
    # If an archive file is not supplied, we attempt to use the Twitter API
    if args.archpath:
        try:
            tweets = load_filter_archive(args)
        except FileNotFoundError:
            logger.error(f"Archive file {args.archpath} cannot be found (exiting)")
            sys.exit(1)
    else:
        tweets = filter_twitter(api, args)
    logger.info("Filtered archive contains %s tweets for deletion", len(tweets))

    # Write filtered tweets (that will be deleted) to file as JSON, if requested
    if args.outfile:
        try:
            with args.outfile.open("w") as ofh:
                json.dump(tweets, ofh)
            logger.info("Wrote %d tweets to %s", len(tweets), args.outfile)
        except IOError:
            logger.error(
                "Could not write filtered tweets to %s (exiting)", args.outfile
            )
            raise SystemError(1)

    # Delete tweets in filtered set
    if args.delete:
        delete_tweets(api, tweets)

    logger.info("Time taken: %.2fs", time.time() - time0)
