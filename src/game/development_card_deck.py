import random
from typing import List, Optional

from src.game.constants import DevelopmentCardType


class DevelopmentCardDeck:
    def __init__(self):
        self.cards: List[DevelopmentCardType] = (
                [DevelopmentCardType.KNIGHT] * 14 +
                [DevelopmentCardType.MONOPOLY] * 2 +
                [DevelopmentCardType.ROAD_BUILDING] * 2 +
                [DevelopmentCardType.YEAR_OF_PLENTY] * 2 +
                [DevelopmentCardType.VICTORY_POINT] * 5
        )
        random.shuffle(self.cards)

    def draw(self) -> Optional[DevelopmentCardType]:
        return self.cards.pop() if self.cards else None
