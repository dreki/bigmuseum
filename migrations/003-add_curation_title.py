"""
Add `created_at`, `updated_at`, and `image_url` to the `curation` collection.
"""
from datetime import datetime

import pymongo
from pymongo.command_cursor import CommandCursor
from pymongo.database import Database

name = '003-add_curation_title'
dependencies = ['002-set_curation_fields']


def upgrade(db: Database):
    """Upgrade the database."""
    # Run an aggregation to lookup the `title` field from the `post` collection.
    cursor: CommandCursor = db.curation.aggregate([
        {'$lookup': {
            'from': 'post',
            'localField': 'post',
            'foreignField': '_id',
            'as': 'post'
        }},
        {'$unwind': '$post'},
        {'$addFields': {
            'title': '$post.title'
        }},
        {'$project': {
            'title': 1,
        }}
    ])

    # Add field to all `curation` documents.
    for curation in cursor:
        # Update curation document to have `title` field from the `post` collection.
        db.curation.update_one({'_id': curation['_id']},
                               {'$set': {'title': curation['title']}})


def downgrade(db: Database):
    """Downgrade the database."""
    # Remove `title` from all `curation` documents.
    db.curation.update_many(
        {'created_at': {'$exists': True}},
        {'$unset': {'title' ''}}
    )
