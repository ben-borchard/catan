import random
from typing import List, Dict

from src.game.board.development_card import DevelopmentCard
from src.game.constants import ResourceType, DevelopmentCardType


class Player:
    def __init__(self, name: str):
        self._name = name
        self._roads_remaining = 15
        self._settlements_remaining = 5
        self._cities_remaining = 4
        self._resources: Dict[ResourceType, int] = {rtype: 0 for rtype in ResourceType}
        self._development_cards: List[DevelopmentCard] = []

    @property
    def name(self):
        return self._name

    @property
    def num_resources(self):
        return len(self._resources)

    def assert_can_build(self, city: bool):
        if city and self._cities_remaining == 0:
            raise RuntimeError("no cities remaining")
        elif not city and self._settlements_remaining == 0:
            raise RuntimeError("no settlements remaining")

    def assert_can_build_road(self):
        if self._roads_remaining == 0:
            raise RuntimeError("no roads remaining")

    def build(self, city: bool):
        if city:
            self._cities_remaining -= 1
            self._settlements_remaining += 1
        else:
            self._settlements_remaining -= 1

    def collect(self, rtype: ResourceType, num: int):
        self._resources[rtype] += num

    def build_road(self):
        self._roads_remaining -= 1

    def assert_can_develop(self, rtype: DevelopmentCardType):
        for card in self._development_cards:
            if card.get_type() == rtype and card.is_playable():
                return

        raise RuntimeError(f"Player {self._name} cannot play {rtype}")

    def discard(self, resources: Dict[ResourceType, int]):
        # validate all resources before deleting anything
        for rtype, remove in resources.items():
            num_resources = self._resources[rtype]
            if num_resources < remove:
                raise RuntimeError(f"Player {self.name} only has {num_resources} of {rtype}, cannot discard {remove}")

        for rtype, amount in resources.items():
            self._resources[rtype] = self._resources[rtype] - amount

    def discard_random_resource(self) -> ResourceType:
        rtype = random.choices(self._resources.keys(), weights=self._resources.values())
        self.discard({rtype: 1})
        return rtype
