import random
from typing import List

from src.game.constants import GamePhase
from src.game.game_state import GameState
from src.game.player_ai import PlayerAi
from src.game.player import Player


class Game:
    def __init__(self, players: List[PlayerAi]):
        if not 2 <= len(players) <= 4:
            raise ValueError("Game must have 2 to 4 players.")

        random.shuffle(players)
        self._players: List[PlayerAi] = players
        self._game_state: GameState = GameState([player.name for player in self._players])

    def start(self):
        # Setup
        while self._game_state.phase != GamePhase.PRE_ROLL:
            player: int = self._game_state.current_player_idx
            self._players[player].initial_build(self._game_state)
            if player == self._game_state.current_player_idx:
                raise RuntimeError(f"Player {self._players[player].name} did not take their initial turn")

        # Game loop
        while self._game_state.winner is None:
            # Pre-roll action (development card perhaps)
            self._current_player.pre_roll(self._game_state)

            self._game_state.assert_phase(GamePhase.ROLL_READY)

            robber: bool = self._game_state.roll()

            if robber:
                # check for discards
                while self._game_state.phase == GamePhase.DISCARD:
                    player: int = self._game_state.current_discard_player_idx
                    self._players[player].discard(self._game_state)
                    if player == self._game_state.current_discard_player_idx:
                        raise RuntimeError(f"Player {self._players[player].name} did not discard")

                self._game_state.assert_phase(GamePhase.ROBBER)
                self._current_player.move_robber(self._game_state)
                self._game_state.assert_phase(GamePhase.STEAL)
                self._current_player.steal(self._game_state)

            self._game_state.assert_phase(GamePhase.POST_ROLL)
            self._current_player.post_roll(self._game_state)

    @property
    def _current_player(self) -> PlayerAi:
        return self._players[self._game_state.current_player_idx]


