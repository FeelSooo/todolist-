from functools import cached_property
from typing import TypeVar


T = TypeVar("T")


def get_repository[T](repo_cls: type[T]) -> T:
    """Get repository."""

    def _get_repository(self) -> T:
        return repo_cls(self.session)

    return cached_property(_get_repository)
