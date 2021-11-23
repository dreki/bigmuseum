"""Holds the `State` `Model`, which contains general data which can be used by the application."""

from typing import Dict
from models.model import Model


class State(Model):
    """The `State` model."""

    key: str
    value: Dict
