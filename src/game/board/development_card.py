from src.game.constants import DevelopmentCardType


class DevelopmentCard:

    def __init__(self, type: DevelopmentCardType):
        self._type: DevelopmentCardType = None
        # cards not playable until one after purchase
        self._playable = False

    def get_type(self) -> DevelopmentCardType:
        return self._type

    def is_playable(self) -> bool:
        return self._playable
