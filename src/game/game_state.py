import random
from typing import List, Set, Dict

from src.game.discard import Discard
from src.game.board.board import Board
from src.game.board.constants import connected
from src.game.building import Building
from src.game.constants import GamePhase, DevelopmentCardType, ResourceType
from src.game.development_card_deck import DevelopmentCardDeck
from src.game.player import Player
from src.game.resource_deck import ResourceDeck


class GameState:

    def __init__(self, players: List[str]):
        self._players = [Player(player) for player in players]
        self._board = Board()
        self._resource_deck = ResourceDeck()
        self._development_deck = DevelopmentCardDeck()
        self._current_player_index = 0
        self._setup_index = 0
        self._player_setup_order: List[int] = list(range(len(players))) + list(reversed(range(len(players))))
        self._phase: GamePhase = GamePhase.SETUP
        self._next_phase: GamePhase = None
        self._buildings: Set[Building] = {}
        self._developed: bool = False
        self._current_discards: List[Discard] = []

    @property
    def current_player_idx(self) -> int:
        return self._current_player_index

    @property
    def current_discard_player_idx(self) -> int:
        return self._current_player_index

    @property
    def is_setup_complete(self) -> bool:
        return self._phase != GamePhase.SETUP

    @property
    def phase(self) -> GamePhase:
        return self._phase

    @property
    def winner(self) -> str:
        return None

    @property
    def _current_player(self) -> Player:
        return self._players[self._current_player_index]

    def roll(self) -> bool:
        """
        Roll the dice and adjust the state accordingly
        :return: `True` if a 7 was rolled and the robber must be moved, otherwise `False`
        """
        dice_total = random.randint(1, 6) + random.randint(1, 6)
        self._roll(dice_total)
        return dice_total == 7

    # test seam
    def _roll(self, dice_total):
        self.assert_phase(GamePhase.ROLL_READY)
        if dice_total == 7:
            # discards
            self._check_for_discards()
            if len(self._current_discards) > 0:
                self._phase = GamePhase.DISCARD
                return
            # robber
            self._phase = GamePhase.ROBBER
        else:
            self._board.distribute_resources(dice_total)
            self._phase = GamePhase.POST_ROLL

    def assert_phase(self, phase: GamePhase):
        if self.phase != phase:
            raise RuntimeError(f"In phase {self.phase}, need to be in {phase}")

    def discard(self, resources: Dict[ResourceType, int]):
        self.assert_phase(GamePhase.DISCARD)
        self._current_discards[-1].execute(resources)
        del self._current_discards[-1]
        if len(self._current_discards) == 0:
            self._phase = GamePhase.ROBBER

    def robber(self, tile: int):
        self.assert_phase(GamePhase.ROBBER)
        self._board.move_robber(tile)
        self._phase = GamePhase.STEAL
        self._next_phase = GamePhase.POST_ROLL

    def steal(self, player_index: int):
        # validation
        self.assert_phase(GamePhase.STEAL)
        player = self._players[player_index]
        if player == self._current_player:
            raise RuntimeError(f"One cannot steal from oneself")
        self._board.assert_can_steal(player)

        # execution
        self._current_player.collect(player.discard_random_resource(), 1)
        self._phase = self._next_phase
        self._next_phase = None

    def _check_for_discards(self):
        for player in self._players:
            if player.num_resources > 7:
                self._current_discards.append(Discard(player, player.num_resources // 2))

    def initial_build(self, settlement_corner: int, road_edge: int):
        # check setup
        if self.is_setup_complete:
            raise RuntimeError('setup done, no more initial placements')

        # check connection
        if not connected(road_edge, settlement_corner):
            raise RuntimeError(f'road at {road_edge} is not connected to settlement {settlement_corner}')

        player: Player = self._current_player

        # note: validations are slightly different for the initial build
        building: Building = Building(player, False)
        self._board.assert_has_space(building, settlement_corner)
        self._board.build(building, settlement_corner)
        player.build_road()
        self._board.build_road(player, road_edge)

        # next player or finish setup
        self._setup_index += 1
        if self._setup_index != len(self._player_setup_order):
            self._current_player_index = self._player_setup_order[self._setup_index]
        else:
            self._phase = GamePhase.PRE_ROLL
            self._current_player_index = 0

    def next(self):
        if self.phase == GamePhase.PRE_ROLL:
            self._phase = GamePhase.ROLL_READY

    def knight(self, tile):

        # validation
        self._assert_can_develop()
        self._current_player.assert_can_develop(DevelopmentCardType.KNIGHT)
        if self._board.robber_tile == tile:
            raise RuntimeError(f"Robber already at time {tile}")

        # execution
        self._board.move_robber(tile)
        self._developed = True

        # next phase (steal)
        if self.phase == GamePhase.PRE_ROLL:
            self._next_phase = GamePhase.ROLL_READY
        else:
            self._next_phase = GamePhase.POST_ROLL
        self._phase = GamePhase.STEAL

    def _assert_can_develop(self):
        if self._phase not in [GamePhase.PRE_ROLL, GamePhase.POST_ROLL]:
            raise RuntimeError(f"Cannot develop in phase {self._phase}")

    def _assert_can_build(self, building: Building, corner: int):
        building.assert_can_build(building)
        self._board.assert_can_build(building, corner)

    def _assert_can_build_road(self, edge: int, player: Player):
        player.assert_can_build(edge)
        self._board.assert_can_build_road(edge)

    def _build_settlement(self, settlement_corner: int, player: Player):
        self._build(settlement_corner, Building(player, False))

    def _build_city(self, city_corner: int, player: Player):
        self._build(city_corner, Building(player, True))

    def _build_road(self, edge: int, player: Player):
        player.build_road()
        self._board.build_road(edge, player)

    def _build(self, corner: int, building: Building):
        # validate the move
        self._assert_can_build(building, corner)

        # build
        building.build()
        self._board.build(corner, building)
