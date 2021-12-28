"""Holds Post model."""
from datetime import datetime

import ujson
from odmantic import Field

from models.model import Model


class Post(Model):
    """Post model."""

    post_id: str
    title: str
    image_url: str
    post_created_at: datetime = Field(default_factory=datetime.utcnow)

    class Config:
        """Post model configuration."""

        # json_loads = lambda self, value: datetime.strptime(value, '%Y-%m-%dT%H:%M:%S.%fZ')
        # json_loads = orjson.loads
        # json_dumps = orjson.dumps
        json_loads = ujson.loads
        json_dumps = ujson.dumps
