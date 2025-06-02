import random
from typing import List, Optional

from src.game.constants import ResourceType


class ResourceDeck:
    def __init__(self):
        self.cards: List[ResourceType] = (
            [r for r in ResourceType for _ in range(19)]
        )
        random.shuffle(self.cards)

    def draw(self) -> Optional[ResourceType]:
        return self.cards.pop() if self.cards else None
