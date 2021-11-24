from typing import Optional
from asyncpraw import Reddit

from settings import settings


async def get_reddit(refresh_token: Optional[str] = None) -> Reddit:
    reddit_client_id: Optional[str] = settings.get('reddit_client_id')
    reddit_secret: Optional[str] = settings.get('reddit_secret')
    if not reddit_client_id or not reddit_secret:
        raise Exception('Missing reddit credentials.')
    if refresh_token:
        return Reddit(
            client_id=reddit_client_id,
            client_secret=reddit_secret,
            refresh_token=refresh_token,
            user_agent='bigmuseum by u/parsifal'
        )
    return Reddit(
        client_id=reddit_client_id,
        client_secret=reddit_secret,
        user_agent='bigmuseum by u/parsifal'
    )
