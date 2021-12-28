import datetime
import json

from odmantic.bson import ObjectId
import bson.objectid

from utils.log import logger


class JSONEncoder(json.JSONEncoder):
    """JSONEncoder subclass with extended type support."""

    def default(self, obj):
        """Handles data of unknown type."""
        # if isinstance(obj, set):
        #     return list(obj)
        if isinstance(obj, datetime.datetime):
            # return obj.strftime('%Y-%m-%dT%H:%M:%S.%f %z')
            # logger.debug(f'> Encoding datetime: {obj} {obj.tzinfo}')
            obj = obj.astimezone(tz=datetime.timezone.utc)
            return {'__type__': 'datetime', 'value': obj.strftime('%Y-%m-%dT%H:%M:%S.%f %z')}
        if isinstance(obj, ObjectId) or isinstance(obj, bson.objectid.ObjectId):
            # return str(obj)
            return {'__type__': 'ObjectId', 'value': str(obj)}
        logger.debug(f'Unknown type: {type(obj)}')
        return json.JSONEncoder.default(self, obj)


class JSONDecoder(json.JSONDecoder):
    """
    JSONDecoder subclass with extended type support.
    
    `datetime.datetime` is converted to UTC and made naive.
    """

    def __init__(self, *args, **kwargs):
        """Initialize."""
        super().__init__(object_hook=self.object_hook, *args, **kwargs)
        # json.JSONDecoder.__init__(
        #     self, object_hook=self.object_hook, *args, **kwargs)

    def object_hook(self, obj):
        """Handles data of unknown type."""
        if isinstance(obj, dict):
            if '__type__' in obj:
                if obj['__type__'] == 'datetime':
                    # Ensure datetime is naive.
                    return (datetime.datetime.strptime(obj['value'],
                                                       '%Y-%m-%dT%H:%M:%S.%f %z')
                            .astimezone(tz=datetime.timezone.utc)
                            .replace(tzinfo=None))
                if obj['__type__'] == 'ObjectId':
                    return ObjectId(obj['value'])
            # return Obj(**obj)
        return obj


def dumps(obj):
    """Dump object to JSON."""
    return json.dumps(obj, cls=JSONEncoder)


def loads(obj):
    """Load object from JSON."""
    return json.loads(obj, cls=JSONDecoder)
