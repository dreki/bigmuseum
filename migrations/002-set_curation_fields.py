"""
Add `created_at`, `updated_at`, and `image_url` to the `curation` collection.
"""
from datetime import datetime
import pymongo
from pymongo.database import Database

name = '002-set_curation_fields'
dependencies = ['001-add_curation_index']


def upgrade(db: Database):
    """Upgrade the database."""
    # Add index
    # db.curation.create_index([('post', pymongo.ASCENDING), ('user', pymongo.ASCENDING)], unique=True)

    # db.user.update_many(
    #     {'introduction': {'$exists': False}},
    #     {'$set': {'introduction': None}}
    # )

    # Run an aggregation on the `curation` collection to set `created_at` and `updated_at` fields.
    # db.curation.aggregate([
    #     {'$addFields': {
    #         'created_at': datetime.utcnow(),
    #         'updated_at': datetime.utcnow()
    #     }},
    #     # {
    #     #     '$project': {
    #     #         'created_at': {'$dateToString': {'format': '%Y-%m-%dT%H:%M:%S.%LZ', 'date': '$created_at'}},
    #     #         'updated_at': {'$dateToString': {'format': '%Y-%m-%dT%H:%M:%S.%LZ', 'date': '$updated_at'}},
    #     #     }
    #     # }
    # ])

    # Update all `curation` documents to have `created_at` and `updated_at` fields, and set them to the current time.
    # Also, add the `image_url` field.
    db.curation.update_many(
        {'created_at': {'$exists': False}},
        {'$set': {'created_at': datetime.utcnow(),
                  'updated_at': datetime.utcnow(),
                  'image_url': None}}
    )


def downgrade(db: Database):
    """Downgrade the database."""
    # Remove index
    # db.curation.drop_index([('post', pymongo.ASCENDING), ('user', pymongo.ASCENDING)])

    # Remove `created_at`, `updated_at`, and `image_url` fields from all `curation` documents.
    db.curation.update_many(
        {'created_at': {'$exists': True}},
        {'$unset': {'created_at': '',
                    'updated_at': '',
                    'image_url': ''}}
    )
