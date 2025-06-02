import pytest

from src.game.board.constants import TOTAL_EDGES

from src.game.building import Building
from src.game.player import Player
from src.game.board.board import Board

from src.game.constants import ResourceType


def test_setup():
    board: Board = Board()

    resources = {}
    markers = {}
    for tile in board._tiles:
        if tile.resource not in resources:
            resources[tile.resource] = 1
        else:
            resources[tile.resource] += 1
        if tile.marker not in markers:
            markers[tile.marker] = 1
        else:
            markers[tile.marker] += 1

    assert 3 == resources[ResourceType.ROCK]
    assert 3 == resources[ResourceType.BRICK]
    assert 4 == resources[ResourceType.SHEEP]
    assert 4 == resources[ResourceType.WHEAT]
    assert 4 == resources[ResourceType.WOOD]
    assert 1 == resources[None]

    assert 1 == markers[2]
    assert 2 == markers[3]
    assert 2 == markers[4]
    assert 2 == markers[5]
    assert 2 == markers[6]
    assert 2 == markers[8]
    assert 2 == markers[9]
    assert 2 == markers[10]
    assert 2 == markers[11]
    assert 1 == markers[12]

    ports = {}
    for resourceType in board._port_resources:
        if resourceType not in ports:
            ports[resourceType] = 1
        else:
            ports[resourceType] += 1

    assert 1 == ports[ResourceType.ROCK]
    assert 1 == ports[ResourceType.BRICK]
    assert 1 == ports[ResourceType.SHEEP]
    assert 1 == ports[ResourceType.WHEAT]
    assert 1 == ports[ResourceType.WOOD]
    assert 4 == ports[None]


def test_road_length():
    # no roads (where we're going we don't need them)
    test: BoardTest = BoardTest()
    for edge in range(TOTAL_EDGES):
        test.assert_road_length(edge, 0)

    # a few random roads
    test: BoardTest = BoardTest().roads(10).p_roads(2, 11)
    for edge in range(TOTAL_EDGES):
        if edge not in [10, 11]:
            test.assert_road_length(edge, 0)
        else:
            test.assert_road_length(edge, 1)

    # extend them a bit
    test: BoardTest = BoardTest().roads(0, 1).p_roads(2, 6, 11)
    for edge in range(TOTAL_EDGES):
        if edge not in [0, 1, 6, 11]:
            test.assert_road_length(edge, 0)
        else:
            test.assert_road_length(edge, 2)

    # branching road
    test: BoardTest = BoardTest().roads(43, 44, 51, 57, 58)
    for edge in [43, 44, 51, 57, 58]:
        test.assert_road_length(edge, 3)

    # long branch road
    test: BoardTest = BoardTest().roads(43, 44, 51, 57, 58, 64, 70, 71, 65)
    for edge in [43, 44, 51, 57, 58, 64, 70, 71, 65]:
        test.assert_road_length(edge, 7)

    # double branch
    test: BoardTest = BoardTest().roads(26, 35, 42, 43, 44, 51, 57, 58, 64, 70, 71, 65)
    for edge in [26, 35, 42, 43, 44, 51, 57, 58, 64, 70, 71, 65]:
        test.assert_road_length(edge, 9)

    # break with settlement, test the splits
    test.p_settlements(2, 32)
    for edge in [26, 35, 42, 43]:
        test.assert_road_length(edge, 3)
    for edge in [51, 57, 58, 64, 70, 71, 65]:
        test.assert_road_length(edge, 6)
    test.assert_road_length(44, 1)


def test_assert_can_build():
    BoardTest() \
        .settlements(20) \
        .roads(35, 43) \
        .p_settlements(2, 12) \
        .p_roads(2, 20, 14, 15, 21) \
        .assert_settlement(32) \
        .assert_settlement(23, 2) \
        .assert_no_settlement(21, 2, "cannot build, building at corner index 20 is too close") \
        .assert_city(20) \
        .assert_city(12, 2) \
        .assert_no_city(12, err="settlement belongs to the wrong player: 2") \
        .assert_no_settlement(20, err="already a building at corner index 20") \
        .assert_no_city(23, 2, "no settlement at corner index 23") \
        .cities(20) \
        .assert_no_city(20, err="city already at corner index 20") \
        .assert_no_settlement(30, err="no connected road")


def test_assert_can_build_road():
    # standard error cases
    test: BoardTest = BoardTest().roads(29)
    for edge in range(TOTAL_EDGES):
        if edge != 29:
            test.assert_no_road(edge, 2, "no connected road")
        if edge not in [28, 21, 36, 30, 29]:
            test.assert_no_road(edge, err="no connected road")
        elif edge == 29:
            test.assert_no_road(edge, err=f"road already at edge {edge}, belongs to 1")
            test.assert_no_road(edge, 2, f"road already at edge {edge}, belongs to 1")
        else:
            test.assert_road(edge)

    # cycle
    BoardTest().roads(43, 35, 27, 28, 36).p_roads(2, 45) \
        .assert_no_road(44, err="will result in cycle") \
        .assert_road(44, 2)

    BoardTest().roads(42, 35, 26, 27, 19, 12, 20).assert_no_road(13, err="will result in cycle")
    BoardTest().roads(0, 1, 2, 3, 8, 15, 21, 29, 36, 44, 43, 42, 41, 34, 24, 18, 10) \
        .assert_no_road(6, err="will result in cycle")


def test_longest_road():
    # basic test with a break
    BoardTest().assert_no_longest_road().roads(0, 1, 2, 3)\
        .assert_no_longest_road()\
        .roads(4)\
        .assert_longest_road(1)\
        .p_roads(2, 66, 67, 68, 69, 70, 71) \
        .assert_longest_road(2)\
        .settlements(50)\
        .assert_longest_road(1)

    # break results in tie, stays with original winner
    BoardTest().roads(0, 1, 2, 3, 4)\
        .p_roads(2, 66, 67, 68, 69, 70)\
        .assert_longest_road(1)\
        .roads(5)\
        .settlements(5)\
        .assert_longest_road(1)\
        .p_settlements(2, 1)\
        .assert_longest_road(1)

    # break but original has another road that is longer, then break again
    BoardTest().roads(0, 1, 2, 3, 4, 5, 23, 24, 25, 26, 27) \
        .p_roads(2, 66, 67, 68, 69, 70)\
        .p_settlements(2, 3)\
        .assert_longest_road(1)\
        .p_settlements(2, 18)\
        .assert_longest_road(2)


def test_connected():
    # basic
    BoardTest().roads(0, 1).p_roads(2, 6, 11, 12) \
        .assert_connected(0, 1)\
        .assert_connected(0, 0)\
        .assert_connected(6, 11)\
        .assert_connected(11, 12)\
        .assert_connected(6, 12)\
        .assert_not_connected(0, 6)\
        .assert_not_connected(0, 2)\
        .assert_not_connected(56, 57)\
        .assert_not_connected(56, 56)

    # broken
    BoardTest().roads(0, 1, 2, 3, 4, 5, 7, 13, 20, 27, 28, 35, 36).p_settlements(2, 20).p_cities(3, 22) \
        .assert_connected(0, 5)\
        .assert_connected(0, 7)\
        .assert_connected(0, 27)\
        .assert_connected(13, 27)\
        .assert_connected(13, 28)\
        .assert_not_connected(0, 35)\
        .assert_not_connected(27, 35)\
        .assert_not_connected(0, 36)\
        .assert_not_connected(28, 36)


class BoardTest:
    # use 1 index for this for understandability (player '0' is not a concept)
    players = [None, Player("1"), Player("2"), Player("3"), Player("4")]

    def __init__(self):
        self.board: Board = Board()

    def roads(self, *edges: int):
        return self.p_roads(1, *edges)

    def p_roads(self, player: int, *edges: int):
        for edge in edges:
            self.board.build_road(self.players[player], edge)
        return self

    def settlements(self, *corners: int):
        return self.p_settlements(1, *corners)

    def p_settlements(self, player: int, *corners: int):
        for corner in corners:
            self.board.build(Building(self.players[player]), corner)
        return self

    def cities(self, *corners: int):
        return self.p_cities(1, *corners)

    def p_cities(self, player: int, *corners: int):
        for corner in corners:
            self.board.build(Building(self.players[player], True), corner)
        return self

    def assert_road_length(self, edge: int, length: int):
        assert length == self.board._road_length(edge)
        return self

    def assert_road(self, edge: int, player: int = 1):
        self.board.assert_can_build_road(self.players[player], edge)
        return self

    def assert_no_road(self, edge: int, player: int = 1, err=None):
        with pytest.raises(RuntimeError, match=err):
            self.board.assert_can_build_road(self.players[player], edge)
        return self

    def assert_settlement(self, corner: int, player: int = 1):
        self.board.assert_can_build(Building(self.players[player], False), corner)
        return self

    def assert_no_settlement(self, corner: int, player: int = 1, err=None):
        with pytest.raises(RuntimeError, match=err):
            self.board.assert_can_build(Building(self.players[player], False), corner)
        return self

    def assert_city(self, corner: int, player: int = 1):
        self.board.assert_can_build(Building(self.players[player], True), corner)
        return self

    def assert_no_city(self, corner: int, player: int = 1, err=None):
        with pytest.raises(RuntimeError, match=err):
            self.board.assert_can_build(Building(self.players[player], True), corner)
        return self

    def assert_connected(self, edge_one, edge_two):
        assert self.board._connected( edge_one, edge_two)
        return self

    def assert_not_connected(self, edge_one, edge_two):
        assert not self.board._connected(edge_one, edge_two)
        return self

    def assert_no_longest_road(self):
        assert None is self.board._longest_road_holder
        return self

    def assert_longest_road(self, player):
        assert self.players[player] == self.board._longest_road_holder
        return self
