from typing import Optional
from asyncpraw import Reddit

from settings import settings


async def get_reddit(refresh_token: Optional[str] = None) -> Reddit:
    reddit: Reddit = Reddit(
        client_id=settings.get('reddit_client_id'),
        client_secret=settings.get('reddit_secret'),
        refresh_token=refresh_token,
        user_agent='bigmuseum by u/parsifal'
    )
    return reddit
