"""
Add `created_at`, `updated_at`, and `image_url` to the `curation` collection.
"""
from datetime import datetime

import pymongo
from pymongo.command_cursor import CommandCursor
from pymongo.database import Database
from rich import print
from rich.markdown import Markdown

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

    # print(f'> {len(list(cursor))} curations found.')
    print('> curations:')
    for curation in cursor:
        print(Markdown(f'# Curation'))
        print(f'  {curation["_id"]}')
        print(f'    image_url: {curation["image_url"]}')
        # print(f'    created_at: {curation["created_at"]}')
        # print(f'    updated_at: {curation["updated_at"]}')
        print(f'    post: {curation["post"]["_id"]}')
        # print(f'    user: {curation["user"]["_id"]}')
        print(flush=True)

        # Update curation document to have `created_at` and `updated_at` fields,
        # and the `image_url` field from the `post` collection.
        db.curation.update_one(
            {'_id': curation['_id']},
            {'$set': {
                'created_at': datetime.utcnow(),
                'updated_at': datetime.utcnow(),
                'image_url': curation['image_url']}}
        )

    # raise NotImplementedError(f'Implementation not yet complete.')

    # Update all `curation` documents to have `created_at` and `updated_at` fields, and set them to the current time.
    # Also, add the `image_url` field.
    # db.curation.update_many(
    #     {'created_at': {'$exists': False}},
    #     {'$set': {'created_at': datetime.utcnow(),
    #               'updated_at': datetime.utcnow(),
    #               'image_url': None}}
    # )


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
