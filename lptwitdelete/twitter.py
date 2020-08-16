# -*- coding: utf-8 -*-
"""Provides access to Twitter API."""

import logging
import webbrowser

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

    delete_tqdm = tqdm(tweets)
    skipped = []
    for tweet in delete_tqdm:
        try:
            delete_tqdm.set_description(tweet["id_str"])
            api.destroy_status(tweet["id_str"])
        except tweepy.TweepError:
            skipped.append(tweet)

    if len(skipped):
        logger.warning("Skipped tweets:\n\t%s", "\n\t".join([_["id_str"] for _ in skipped]))


def filter_twitter(api: tweepy.API, args: Namespace):
    """Filter tweets from a Twitter account based on passed options.

    :param api:  authenticated tweepy API stream
    :param args:  Namespace of command-line arguments
    """
    logger = logging.getLogger(__name__)

    # Iterate through tweets via API
    logger.info("Processing Twitter statuses for %s via web API...", api.me().screen_name)
    tweets = [_._json for _ in tqdm(tweepy.Cursor(api.user_timeline).items())]

    return filter_tweets(tweets, args)


def oauth_login(consumer_key: str, consumer_secret: str):
    """Authenticate with Twitter via OAuth.

    :param consumer_key:  the consumer API key
    :param consumer_secret:  the consumer API secret key
    """
    logger = logging.getLogger(__name__)
    logger.info("Authenticating to Twitter via OAuth")

    # Authenticate
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    try:
        auth_url = auth.get_authorization_url()
    except tweepy.TweepError:
        logger.error("Failed to get request token (exiting)")
        raise SystemError(1)

    # Open webbrowser to authentication URL and get user code
    logger.info("Opening authentication URL %s in new browser tab", auth_url)
    webbrowser.open_new_tab(auth_url)
    verification_code = input("Please enter the verification code from your browser > ")

    # Verify access token
    auth.get_access_token(verification_code)

    return tweepy.API(auth)
