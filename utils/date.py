"""Provides date utilities."""

import datetime
from typing import Optional

import dateparser


def parse_nl_date(date_str: str) -> Optional[datetime.datetime]:
    """Parse a natural language date string.

    :param date_str: The date string to parse.
    :return: The parsed date.
    """
    return dateparser.parse(date_str)
