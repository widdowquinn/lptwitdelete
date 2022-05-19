# -*- coding: utf-8 -*-

import logging
import yaml

from pathlib import Path


class Config:

    """Configuration YAML parsing for lptwitdelete keys."""

    CONSUMER_KEY = ""
    CONSUMER_SECRET = ""
    ACCESS_KEY = ""
    ACCESS_SECRET = ""
    USERNAME = ""

    def __init__(self, username: str, confpath: Path) -> None:
        """Use local configuration information for the Twitter account with passed username."""
        logger = logging.getLogger(__name__)

        with confpath.open("r") as ifh:
            try:
                confdata = yaml.safe_load(ifh)
                self.CONSUMER_KEY = confdata["lptwitdelete"]["api_key"]
                self.CONSUMER_SECRET = confdata["lptwitdelete"]["api_secret_key"]
                self.ACCESS_KEY = confdata["lptwitdelete"]["access_token"]
                self.ACCESS_SECRET = confdata["lptwitdelete"]["access_token_secret"]
                self.USERNAME = username
            except yaml.YAMLError:
                logger.error("Error loading config file %s (exiting)", confpath, exc_info=True)
                raise SystemError(1)
