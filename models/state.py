"""Holds the `State` `Model`, which contains general data which can be used by the application."""

import datetime
from typing import Dict, Union

from models.model import Model


class State(Model):
    """The `State` model."""

    key: str
    value: Union[Dict, str, datetime.datetime]
