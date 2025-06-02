from game.board.road_tree import RoadTree


def test_basic():
    road_tree: RoadTree = RoadTree(51)
    assert road_tree.get_max_len() == 1
    road_tree.add(58, 51)
    assert road_tree.get_max_len() == 2
    road_tree.add(43, 51)
    assert road_tree.get_max_len() == 3
    road_tree.add(35, 43)
    assert road_tree.get_max_len() == 4
    road_tree.add(26, 35)
    assert road_tree.get_max_len() == 5
    road_tree.add(64, 58)
    assert road_tree.get_max_len() == 6


def test_branching():
    road_tree: RoadTree = RoadTree(51)
    road_tree.add(43, 51)
    road_tree.add(44, 51)
    road_tree.add(58, 51)
    road_tree.add(57, 51)
    assert road_tree.get_max_len() == 3

    road_tree.add(35, 43)
    road_tree.add(42, 43)
    road_tree.add(36, 44)
    road_tree.add(45, 44)
    assert road_tree.get_max_len() == 4

    road_tree.add(56, 57)
    road_tree.add(63, 57)
    road_tree.add(64, 58)
    road_tree.add(59, 58)
    assert road_tree.get_max_len() == 5

    # uneven branch
    road_tree.add(26, 35)
    road_tree.add(19, 26)
    road_tree.add(11, 19)
    assert road_tree.get_max_len() == 8


def test_sub_tree():
    road_tree: RoadTree = RoadTree(51)
    road_tree.add(43, 51)
    road_tree.add(44, 51)
    assert road_tree.get_max_len() == 2

    road_tree.add(36, 44)
    assert road_tree.get_max_len() == 3

    # sub tree wins
    road_tree.add(35, 43)
    assert road_tree.get_max_len() == 4

    road_tree.add(58, 51)
    assert road_tree.get_max_len() == 4

    # span wins
    road_tree.add(64, 58)
    assert road_tree.get_max_len() == 5

    road_tree.add(29, 36)
    assert road_tree.get_max_len() == 6

    road_tree.add(30, 29)
    assert road_tree.get_max_len() == 7

    road_tree.add(26, 35)
    assert road_tree.get_max_len() == 7

    # sub tree wins
    road_tree.add(25, 26)
    assert road_tree.get_max_len() == 8
