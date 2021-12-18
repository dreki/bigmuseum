"""Holds the Curation `Model`, which associates a `Post` with a `User`."""
from odmantic import Reference

from models.model import Model
from models.post import Post
from models.user import User


class Curation(Model):
    """A curation a user makes of a work of a post/work of art."""

    post: Post = Reference()
    user: User = Reference()
