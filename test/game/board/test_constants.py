from src.game.board.constants import CORNERS_TO_EDGES, connected
from src.game.board.constants import EDGES_TO_CORNERS
from src.game.board.constants import CORNER_NEIGHBORS


def test_edges_to_corners():
    # spot test
    assert [0, 8] == EDGES_TO_CORNERS[6]
    assert [14, 15] == EDGES_TO_CORNERS[17]
    assert [13, 23] == EDGES_TO_CORNERS[21]
    assert [22, 33] == EDGES_TO_CORNERS[36]
    assert [29, 30] == EDGES_TO_CORNERS[41]
    assert [41, 42] == EDGES_TO_CORNERS[57]
    assert [45, 53] == EDGES_TO_CORNERS[65]
    assert [52, 53] == EDGES_TO_CORNERS[71]


def test_corners_to_edges():
    # spot test
    assert [2, 3] == CORNERS_TO_EDGES[3]
    assert [15, 16, 21] == CORNERS_TO_EDGES[13]
    assert [24, 25, 34] == CORNERS_TO_EDGES[18]
    assert [41, 42, 50] == CORNERS_TO_EDGES[30]
    assert [38, 48] == CORNERS_TO_EDGES[37]
    assert [62, 66] == CORNERS_TO_EDGES[47]
    assert [70, 71] == CORNERS_TO_EDGES[52]


def test_corner_neighbors():
    # spot test
    assert {2, 3, 4} == CORNER_NEIGHBORS[3]
    assert {12, 13, 14, 23} == CORNER_NEIGHBORS[13]
    assert {16, 17, 27} == CORNER_NEIGHBORS[16]
    assert {19, 20, 21, 31} == CORNER_NEIGHBORS[20]
    assert {27, 28, 29, 38} == CORNER_NEIGHBORS[28]
    assert {34, 43, 44, 45} == CORNER_NEIGHBORS[44]


def test_connected():
    # spot test
    assert connected(24, 17)
    assert connected(50, 40)
    assert connected(70, 51)
    assert connected(28, 21)
    assert connected(0, 0)
    assert connected(6, 0)
    assert not connected(1, 0)
    assert not connected(34, 33)
    assert not connected(14, 30)
