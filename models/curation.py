"""Holds the Curation `Model`, which associates a `Post` with a `User`."""
from datetime import datetime
from odmantic import Reference, Field

from models.model import Model
from models.post import Post
from models.user import User


class Curation(Model):
    """A curation a user makes of a work of a post/work of art."""

    image_url: str
    title: str
    post: Post = Reference()
    user: User = Reference()
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    @classmethod
    def from_post_and_user(cls, post: Post, user: User) -> 'Curation':
        """Create a curation from a post."""
        return Curation(image_url=post.image_url,
                        title=post.title,
                        post=post,
                        user=user)
