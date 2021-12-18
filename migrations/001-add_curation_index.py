"""
Add index to (`Curation.post`, `Curation.user`).
"""
import pymongo
from pymongo.database import Database

name = '001-add_curation_index'
# dependencies = ['001-add_curation_index']
dependencies = []


def upgrade(db: Database):
    """Upgrade the database."""
    # Add index
    db.curation.create_index([('post', pymongo.ASCENDING), ('user', pymongo.ASCENDING)], unique=True)

    # db.user.update_many(
    #     {'introduction': {'$exists': False}},
    #     {'$set': {'introduction': None}}
    # )


def downgrade(db: Database):
    """Downgrade the database."""
    # Remove index
    db.curation.drop_index([('post', pymongo.ASCENDING), ('user', pymongo.ASCENDING)])
