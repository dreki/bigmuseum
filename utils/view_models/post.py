"""Holds the `Post` view model."""
from dataclasses import dataclass
from typing import Optional

from utils.view_models.view_model import ViewModel
from datetime import datetime


@dataclass
class Post(ViewModel):
    """Represents a Reddit post."""

    title: str
    created_at: datetime
    link: Optional[str] = None
