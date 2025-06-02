import pytest

from src.game.game_state import GameState


def test_setup():
    # test default
    GameStateTest()

    # test 3 and 4 players
    GameStateTest(["1", "2", "3"])\
        .init_build(0, 0)\
        .init_build(16, 23)\
        .init_build(26, 38)\
        .init_build(2, 1)\
        .init_build(7, 18)\
        .init_build(36, 48)\
        .assert_setup_complete()

    GameStateTest(["1", "2", "3", "4"]) \
        .init_build(0, 0) \
        .init_build(5, 5) \
        .init_build(47, 66) \
        .init_build(53, 65) \
        .init_build(2, 1) \
        .init_build(14, 9) \
        .init_build(49, 67) \
        .init_build(44, 60) \
        .assert_setup_complete()

    # error cases
    GameStateTest(["1", "2"])\
        .invalid_init_build(0, 1, "road at 1 is not connected to settlement 0")\
        .init_build(0, 0)\
        .invalid_init_build(0, 0, "already a building at corner index 0")\
        .invalid_init_build(1, 1, "cannot build, building at corner index 0 is too close")\
        .invalid_init_build(8, 11, "cannot build, building at corner index 0 is too close")\
        .init_build(9, 11)\
        .init_build(20, 26)\
        .init_build(50, 69)\
        .assert_setup_complete()\
        .invalid_init_build(6, 9, "setup done, no more initial placements")


class GameStateTest:

    def __init__(self, players=None):

        if players is None:
            # default setup
            self.game_state: GameState = GameState(["1", "2"])
            self.init_build(0, 0).init_build(6, 5).init_build(53, 71).init_build(47, 66)\
                .assert_setup_complete()
        else:
            self.game_state: GameState = GameState(players)

    def init_build(self, settlement: int, road: int):
        self.game_state.initial_build(settlement, road)
        return self

    def invalid_init_build(self, settlement: int, road: int, err=None):
        with pytest.raises(RuntimeError, match=err):
            self.game_state.initial_build(settlement, road)
        return self

    def assert_setup_complete(self):
        assert self.game_state.is_setup_complete
        return self

