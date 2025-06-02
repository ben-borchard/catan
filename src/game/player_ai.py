from typing import Protocol

from src.game.game_state import GameState


class PlayerAi(Protocol):

    def initial_build(self, game: GameState):
        """
        Make initial placement using `game.initial_build(settlement, road)`
        """
        ...

    def pre_roll(self, game: GameState):
        """
        Take pre-roll action, if desired. Must invoke `game.next()` if not taking an action
        """
        ...

    def post_roll(self, game: GameState):
        """
        Take any number of valid post roll actions. When done with actions, must invoke `game.next()` to continue the game
        """
        ...

    def discard(self, game: GameState):
        """
        Discard cards using `game.discard(resources)`
        """
        ...

    def move_robber(self, game: GameState):
        """
        Move the robber using `game.move_robber(tile)`
        """
        ...

    def steal(self, game: GameState):
        """
        Steal from a valid player (on the robber tile) using `game.steal(player_index)`
        """
        ...

    @property
    def name(self) -> str:
        ...
