
import datetime
from typing import Dict, Optional

# from models.model import TimestampingModel
from models.model import Model


# class Session(TimestampingModel):
class Session(Model):
    """A logged-in person's session."""
    key: str
    reddit_token: Optional[Dict]
    created_at: datetime.datetime
    updated_at: datetime.datetime
