# -*- coding: utf-8 -*-
"""Module providing support for package-level logging."""

import logging
import logging.config
import re
import sys

from argparse import Namespace
from pathlib import Path
from typing import Optional


class NoColorFormatter(logging.Formatter):

    """Log formatter that strips terminal colour escape codes from the log message."""

    ANSI_RE = re.compile(r"\x1b\[[0-9;]*m")

    def format(self, record):
        """Return logger message with terminal escapes removed."""
        return "[%s] [%s]: %s" % (record.levelname, record.name, re.sub(self.ANSI_RE, "", record.msg % record.args),)


def config_logger(args: Optional[Namespace] = None) -> None:
    """Configure package-level logging.

    :param args: CLI namespace; logfile is used to create a logfile,
                 verbose and debug control logging level.

    We configure a logger at package level, from which the module will
    inherit. If CLI args are provided, these are used to define output
    streams, and logging level.
    """
    # Default logger for this module
    logger = logging.getLogger(__package__)
    logger.setLevel(logging.DEBUG)

    # Create and add STDERR handler
    errformatter = logging.Formatter("[%(levelname)s] [%(name)s]: %(message)s")
    errhandler = logging.StreamHandler(sys.stderr)
    if args is not None and args.verbose:
        errhandler.setLevel(logging.INFO)
    elif args is not None and args.debug:
        errhandler.setLevel(logging.DEBUG)
    else:
        errhandler.setLevel(logging.WARNING)
    errhandler.setFormatter(errformatter)
    logger.addHandler(errhandler)

    # If args.logfile is provided, add a FileHandler for logfile
    if args is not None and args.logfile is not None:
        logdir = args.logfile.parents[0]
        # Check that output directory exists and, if not, create it
        try:
            if not logdir == Path.cwd():
                logdir.mkdir(exist_ok=True)
        except OSError:
            logger.error("Could not create log directory %s (exiting)", logdir, exc_info=True)
            raise SystemExit(1)

        # Create logfile handler
        logformatter = NoColorFormatter()
        loghandler = logging.FileHandler(args.logfile, mode="w", encoding="utf8")
        if args.debug:
            loghandler.setLevel(logging.DEBUG)
        else:
            loghandler.setLevel(logging.INFO)
        loghandler.setFormatter(logformatter)
        logger.addHandler(loghandler)
