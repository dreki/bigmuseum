"""
Add `created_at`, `updated_at`, and `image_url` to the `curation` collection.
"""
from datetime import datetime

import pymongo
from pymongo.command_cursor import CommandCursor
from pymongo.database import Database

name = '002-set_curation_fields'
dependencies = ['001-add_curation_index']


def upgrade(db: Database):
    """Upgrade the database."""
    # Run an aggregation to lookup the `image_url` field from the `post` collection.
    cursor: CommandCursor = db.curation.aggregate([
        {'$lookup': {
            'from': 'post',
            'localField': 'post',
            'foreignField': '_id',
            'as': 'post'
        }},
        {'$unwind': '$post'},
        {'$addFields': {
            'image_url': '$post.image_url'
        }},
        {'$project': {
            'image_url': 1,
            'created_at': 1,
            'updated_at': 1,
            'post': 1,
            'user': 1
        }}
    ])

    # Add fields to all `curation` documents.
    for curation in cursor:
        # Update curation document to have `created_at` and `updated_at` fields,
        # and the `image_url` field from the `post` collection.
        db.curation.update_one({'_id': curation['_id']},
                               {'$set': {
                                   'created_at': datetime.utcnow(),
                                   'updated_at': datetime.utcnow(),
                                   'image_url': curation['image_url']}})


def downgrade(db: Database):
    """Downgrade the database."""
    # Remove `created_at`, `updated_at`, and `image_url` fields from all `curation` documents.
    db.curation.update_many(
        {'created_at': {'$exists': True}},
        {'$unset': {'created_at': '',
                    'updated_at': '',
                    'image_url': ''}}
    )
