import os
from typing import Dict

settings: Dict = {}

# Default to the environment.
settings.update(
    # Lower-case all the keys.
    dict([(k.lower(), v) for (k, v) in os.environ.items()])
)
