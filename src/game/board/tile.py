from typing import Optional

from src.game.constants import ResourceType


class Tile:
    def __init__(self, resource_type: Optional[ResourceType], marker: Optional[int], index: int):
        self._resource_type = resource_type
        self._marker = marker  # None for desert
        self._has_robber = resource_type is None
        self._index = index

    def __repr__(self):
        return f"Tile({self._resource_type}, {self._marker}, Robber={self._has_robber})"

    @property
    def index(self) -> int:
        return self._index

    @property
    def marker(self) -> int:
        return self._marker

    @property
    def has_robber(self) -> bool:
        return self._has_robber

    @property
    def resource(self) -> ResourceType:
        return self._resource_type
