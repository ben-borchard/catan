from src.game.constants import ResourceType
from src.game.player import Player


class Building:

    def __init__(self, player: Player, is_city: bool = False):
        self._player = player
        self._is_city = is_city
        self._is_built = False

    @property
    def is_city(self):
        return self._is_city

    @property
    def player(self) -> Player:
        return self._player

    def collect(self, rtype: ResourceType):
        self._player.collect(rtype, 2 if self._is_city else 1)

    def assert_can_build(self):
        self._player.assert_can_build(self._is_city)

    def build(self):
        if self._is_built:
            raise RuntimeError("already built")
        else:
            self._player.build(self._is_city)
            self._is_built = True
