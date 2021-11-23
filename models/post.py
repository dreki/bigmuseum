"""Holds Post model."""
from datetime import datetime

from odmantic import Field

from models.model import Model


class Post(Model):
    """Post model."""

    post_id: str
    title: str
    image_url: str
    post_created_at: datetime = Field(default_factory=datetime.utcnow)
