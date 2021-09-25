from datetime import datetime
from typing import TypeVar

from odmantic import EmbeddedModel as ODManticEmbeddedModel
from odmantic import Model as ODManticModel

ModelType = TypeVar('ModelType', bound='Model')


class EmbeddedModel(ODManticEmbeddedModel):
    pass


class Model(ODManticModel):
    async def pre_save(self):
        # raise NotImplementedError()
        now: datetime = datetime.utcnow()
        if hasattr(self, 'created_at') and not self.created_at:
            self.created_at = now
        if hasattr(self, 'updated_at'):
            self.updated_at = now


# class TimestampingModel(Model):
#     """A `Model` that automatically sets `created_at` and `updated_at`, if present."""
#     async def pre_save(self):
#         now: datetime = datetime.utcnow()
#         if hasattr(self, 'created_at') and not self.created_at:
#             self.created_at = now
#         if hasattr(self, 'updated_at'):
#             self.updated_at = now
