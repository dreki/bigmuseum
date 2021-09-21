
import inspect
from dataclasses import dataclass
from enum import Enum
from typing import Any, Dict, Mapping, Optional, Type, TypeVar

# `TModel` is used to enable generic functionality in `Model`.
TModel = TypeVar('TModel', bound='Model')


class Model:
    @classmethod
    def from_json(cls: Type[TModel],
                  d: Dict[str, Any],
                  ignore_unknown_fields: Optional[bool] = False) -> TModel:
        # Allow optionally ignoring fields not defined by `cls`.
        if ignore_unknown_fields:
            defined_attributes: \
                Mapping[str, Any] = inspect.signature(cls).parameters
            d: Dict[str, Any] = \
                dict([(k, v) for k, v in d.items() if k in defined_attributes])
        return cls(**d)


class TokenType(str, Enum):
    """The types of Reddit credential tokens."""
    BEARER = 'bearer'


@dataclass
class RedditCredentials(Model):
    """Holds data regarding Reddit credentials."""
    access_token: str
    token_type: TokenType
    expires_in: int
    refresh_token: str
    scope: str

    @property
    def expires_in_minutes(self) -> float:
        """In how many minutes will these credentials expire?"""
        return self.expires_in / 60
