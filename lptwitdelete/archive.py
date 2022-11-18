# -*- coding: utf-8 -*-
"""Provides code to handle downloaded Twitter archive."""

import json
import logging

from argparse import Namespace
from typing import List

from lptwitdelete.filters import filter_tweets, filter_dms


def load_filter_archive(args: Namespace) -> List[dict]:
    """Load a Twitter archive and filter tweets on the passed options."""
    logger = logging.getLogger(__name__)

    # Load tweet archive
    logger.info("Parsing Twitter archive in %s...", args.archpath)
    with args.archpath.open("r") as ifh:
        # The tweet.js file starts with non-standard text (window.YTD.tweet.part0 = )
        # that the JSON parser cannot handle, so we need to strip this before parsing
        firstline = ifh.readline()
        if firstline.startswith("window.YTD.tweets.part0"):
            ifh.seek(26, 0)
        elif firstline.startswith("window.YTD.direct_messages.part0"):
            ifh.seek(35, 0)
        else:
            ifh.seek(0, 0)
        tweets = json.load(ifh)
        logger.debug("Loaded %s tweets", len(tweets))

    if "dmConversation" in tweets[0]:
        logger.info("Archive is a direct message archive, not a tweet archive")
        return filter_dms(list(tweets), args)
    else:
        return filter_tweets(list(tweets), args)
