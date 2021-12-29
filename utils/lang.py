"""Defines 'language-level' utilities."""
from typing import (Any, Dict, Optional, Sequence, Tuple, Type, TypeVar,
                    get_args, get_origin)

T = TypeVar('T')


def ensure_type(expected_type: Type[T], value: Any) -> Optional[T]:
    """Ensure value is of expected type."""
    # If expected_type is a parameterized generic, check it and its parameter.
    type_args: Tuple = get_args(expected_type)
    type_origin: Optional[Any] = get_origin(expected_type)
    if not type_origin:  # For `str`, `int`, etc.
        type_origin = expected_type
    if not isinstance(value, type_origin):
        raise Exception(
            f'Expected type {expected_type} but got {type(value)}.')
    if type_args:
        # Note: Only checks first element.
        if isinstance(value, Sequence) and len(value) > 0:
            if not isinstance(value[0], type_args[0]):
                raise Exception(
                    f'Expected subscripted type {expected_type} but got {type(value)}.')
        # Note: Only checks first key-value pair.
        if isinstance(value, Dict) and len(value) > 0:
            first_key: Any = list(value.keys())[0]
            if not isinstance(first_key, type_args[0]):
                raise Exception(f'Expected subscripted key type {expected_type} '
                                f'but got {type(first_key)}.')
            first_value: Any = list(value.values())[0]
            if not isinstance(first_value, type_args[1]):
                raise Exception(f'Expected subscripted value type {expected_type} '
                                f'but got {type(first_value)}.')
    return value  # type: ignore
