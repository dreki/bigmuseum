"""Holds the User model."""
from typing import List, Optional, Set

from odmantic import Field
from odmantic.bson import ObjectId

from models.model import Model
from pydantic import validator


class User(Model):
    """User model."""

    username: str
    hidden_posts: Optional[List[ObjectId]]

    # def add_hidden_post(self, post_id: ObjectId) -> None:
    #     """Add a hidden post."""
    #     if self.hidden_posts is None:
    #         self.hidden_posts = list(set())
    #     self.hidden_posts.append(post_id)
    #     # Ensure uniqueness.
    #     self.hidden_posts = list(set(self.hidden_posts))

    @validator('hidden_posts')
    def ensure_unique_hidden_posts(cls, v: List[ObjectId]) -> List[ObjectId]:
        """Ensure unique hidden posts."""
        return list(set(v))
