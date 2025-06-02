from typing import Dict

from src.game.constants import ResourceType
from src.game.player import Player


class Discard:

    def __init__(self, player: Player, num_discards: int):
        self._player = player
        self._num_discards = num_discards

    def execute(self, resources: Dict[ResourceType, int]):
        num_discards = len(resources)

        if len(resources) != self._num_discards:
            raise RuntimeError(f"Need to discard {self._num_discards}, not {num_discards}")

        self._player.discard(resources)
