# -*- coding: utf-8 -*-
"""Apply filters to collections of tweets."""

import logging

from argparse import Namespace
from datetime import datetime
from typing import Iterable, List


def filter_tweets(tweets: Iterable, args: Namespace) -> List[dict]:
    """Apply filters to tweets and return filtered collection.

    :param tweets:  iterable of JSON format tweets
    :param args:  command-line argument namespace
    """
    logger = logging.getLogger(__name__)

    # Filter start date for deletion
    if args.start_date:
        logger.info("Filtering archive for tweets posted after %s...", args.start_date)
        try:
            sdate = datetime.strptime(args.start_date, "%Y-%m-%d").astimezone()
        except ValueError:
            logger.error(
                "Could not parse start date %s (exiting)",
                args.start_date,
                exc_info=True,
            )
            raise SystemError(1)
        tweets = filter(lambda tweet: date_after(tweet, sdate), tweets)

    # Filter end date for deletion
    if args.end_date:
        logger.info("Filtering archive for tweets posted before %s...", args.end_date)
        try:
            edate = datetime.strptime(args.end_date, "%Y-%m-%d").astimezone()
        except ValueError:
            logger.error(
                "Could not parse end date %s (exiting)", args.end_date, exc_info=True
            )
            raise SystemError(1)
        tweets = filter(lambda tweet: date_before(tweet, edate), tweets)

    # Filter if retweet
    if args.is_retweet:
        logger.info("Filtering archive for tweets that are retweets...")
        tweets = filter(is_retweet, tweets)

    # Filter if retweet
    if args.is_reply:
        logger.info("Filtering archive for tweets that are replies...")
        tweets = filter(is_reply, tweets)

    return list(tweets)


def date_after(tweet: dict, date: datetime):
    """Return True if passed tweet was posted after the passed date.

    :param tweet:  JSON dict for tweet
    :param date:  if the tweet was posted after this date it should be considered for deletion
    """
    logger = logging.getLogger(__name__)

    try:
        tweet_date = datetime.strptime(
            tweet["tweet"]["created_at"], "%a %b %d %X %z %Y"
        )
    except KeyError:
        print(tweet)
        logger.warning("Tweet %s has no 'created_at' field", tweet["tweet"]["id"])
        return False
    if tweet_date >= date:
        return True
    return False


def date_before(tweet: dict, date: datetime):
    """Return True if passed tweet was posted before the passed date.

    :param tweet:  JSON dict for tweet
    :param date:  if the tweet was posted before this date it should be considered for deletion

    Expected date format: "%a %b %d %X %z %Y"

    e.g. Mon Jul 02 00:00:00 +0000 2019
    """
    logger = logging.getLogger(__name__)

    try:
        tweet_date = datetime.strptime(
            tweet["tweet"]["created_at"], "%a %b %d %X %z %Y"
        )
    except KeyError:
        logger.warning("Tweet %s has no 'created_at' field", tweet["tweet"]["id"])
        return False
    if tweet_date <= date:
        return True
    return False


def is_retweet(tweet: dict):
    """Return True if the passed tweet is a retweet.

    :param tweet:  JSON dict for tweet
    """
    try:
        text = tweet["tweet"]["full_text"]
    except KeyError:
        text = tweet["tweet"]["text"]
    if text.startswith("RT @"):
        return True
    return False


def is_reply(tweet: dict):
    """Return True if the passed tweet is a reply.

    :param tweet:  JSON dict for tweet
    """
    if tweet["tweet"]["in_reply_to_screen_name"]:
        return True
    return False
