
from datetime import datetime
from enum import Enum
from typing import Dict, Optional

from odmantic import Field

# from models.model import TimestampingModel
from models.model import EmbeddedModel, Model


class TokenType(str, Enum):
    """The types of Reddit credential tokens."""
    BEARER = 'bearer'


class RedditCredentials(EmbeddedModel):
    """Holds data regarding Reddit credentials."""
    access_token: str
    token_type: TokenType
    expires_in: int
    refresh_token: str
    scope: str

    @property
    def expires_in_minutes(self) -> float:
        """In how many minutes will these credentials expire?"""
        return self.expires_in / 60

    pass

# class Session(TimestampingModel):


class Session(Model):
    """A logged-in person's session."""
    key: str
    # reddit_token: Optional[Dict]
    reddit_credentials: Optional[RedditCredentials]
    # created_at: datetime.datetime
    # updated_at: datetime.datetime
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
