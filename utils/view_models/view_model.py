"""Holds shared view model behavior."""
from dataclasses import asdict
from typing import Dict


class ViewModel:
    """Superclass for view model classes."""

    def to_dict(self) -> Dict:
        """Convert this view model to a `Dict`."""
        return asdict(self)
