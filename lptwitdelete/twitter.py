# -*- coding: utf-8 -*-
"""Provides access to Twitter API."""

import logging

from argparse import Namespace
from typing import List

import tweepy

from tqdm import tqdm

from lptwitdelete.filters import filter_tweets


def delete_tweets(api: tweepy.API, tweets: List):
    """Delete passed tweets using Twitter API.

    :param api:  authenticated tweepy API stream
    :param tweets:  iterable of tweets for deletion
    """
    logger = logging.getLogger(__name__)
    logger.info("Deleting (filtered) tweets from timeline...")

    delete_tqdm = tqdm(tweets)
    skipped = []
    for tweet in delete_tqdm:
        try:
            if "tweet" in tweet:
                delete_tqdm.set_description(tweet["tweet"]["id_str"])
                api.destroy_status(tweet["tweet"]["id_str"])
            elif "messageCreate" in tweet:
                delete_tqdm.set_description(tweet["messageCreate"]["id"])
                api.delete_direct_message(tweet["messageCreate"]["id"])
            elif "welcomeMessageCreate" in tweet:
                delete_tqdm.set_description(tweet["welcomeMessageCreate"]["id"])
                api.delete_direct_message(tweet["welcomeMessageCreate"]["id"])
        except tweepy.errors.TweepyException:
            skipped.append(tweet)

    if len(skipped):
        logger.warning("Skipped %d tweets", len(skipped))
        # logger.warning(
        #     "Skipped tweets:\n\t%s",
        #     "\n\t".join([_["tweet"]["id_str"] for _ in skipped]),
        # )


def filter_twitter(api: tweepy.API, args: Namespace):
    """Filter tweets from a Twitter account based on passed options.

    :param api:  authenticated tweepy API stream
    :param args:  Namespace of command-line arguments
    """
    logger = logging.getLogger(__name__)

    # Iterate through tweets via API
    logger.info(
        "Processing Twitter statuses for %s via web API...", api.me().screen_name
    )
    tweets = [_._json for _ in tqdm(tweepy.Cursor(api.user_timeline).items())]

    return filter_tweets(tweets, args)


def oauth_login(
    consumer_key: str, consumer_secret: str, access_token: str, access_token_secret: str
):
    """Authenticate with Twitter via OAuth.

    :param consumer_key:  the consumer API key
    :param consumer_secret:  the consumer API secret key
    """
    logger = logging.getLogger(__name__)
    logger.info("Authenticating to Twitter via OAuth")

    # Authenticate
    auth = tweepy.OAuth1UserHandler(
        consumer_key, consumer_secret, access_token, access_token_secret
    )

    return tweepy.API(auth)
