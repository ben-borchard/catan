import random
from typing import List, Set, Dict

from src.game.board.constants import TOTAL_CORNERS, TOTAL_EDGES, TOTAL_TILES, CORNER_NEIGHBORS, EDGES_TO_CORNERS, \
    CORNERS_TO_EDGES, common_corner, TOTAL_MARKERS, TILE_TO_CORNERS
from src.game.board.road_tree import RoadTree
from src.game.board.tile import Tile
from src.game.building import Building
from src.game.constants import ResourceType
from src.game.player import Player

import logging


logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


class LongestRoad:
    def __init__(self):
        self.length = 0
        self.edge = -1


class Board:

    def __init__(self):
        self._robber_tile: int = None
        self._port_resources: List[ResourceType] = None
        # one index the markers
        self._marker_to_tiles: List[List[Tile]] = [[] for _ in range(TOTAL_MARKERS + 1)]
        self._tiles: List[Tile] = [None] * TOTAL_TILES
        self._generate_board()
        self._buildings: List[Building] = [None] * TOTAL_CORNERS
        self._roads: List[Player] = [None] * TOTAL_EDGES
        self._longest_roads: Dict[Player, LongestRoad] = {}
        self._longest_road_holder: Player = None

    def _generate_board(self):
        # Resource assignment and shuffling
        resources = (
                [ResourceType.ROCK] * 3 +
                [ResourceType.BRICK] * 3 +
                [ResourceType.WHEAT] * 4 +
                [ResourceType.WOOD] * 4 +
                [ResourceType.SHEEP] * 4 +
                [None]  # desert
        )
        markers = [5, 2, 6, 3, 8, 10, 9, 12, 11, 4] * 2
        markers.remove(2)
        markers.remove(12)
        self._port_resources: List[ResourceType] = (
                [ResourceType.ROCK] +
                [ResourceType.BRICK] +
                [ResourceType.WHEAT] +
                [ResourceType.WOOD] +
                [ResourceType.SHEEP] +
                [None] * 4  # 3 for 1
        )

        random.shuffle(self._port_resources)
        random.shuffle(resources)
        random.shuffle(markers)

        for tile_idx in range(TOTAL_TILES):
            resource = resources.pop()
            marker = None if resource is None else markers.pop()
            tile = Tile(resource, marker, tile_idx)
            if marker is not None:
                self._marker_to_tiles[marker].append(tile)
            self._tiles[tile_idx] = tile

            # robber starts in desert
            if resource is None:
                self._robber_tile = tile_idx

    def tiles(self, marker: int) -> List[Tile]:
        return self._marker_to_tiles[marker]

    def buildings(self, tile: int) -> List[Building]:
        buildings: List[Building] = []
        for corner in TILE_TO_CORNERS[tile]:
            building = self._buildings[corner]
            if building is not None:
                buildings.append(building)
        return buildings

    def distribute_resources(self, dice_total: int):
        for tile in self.tiles(dice_total):
            if tile.has_robber:
                return
            for building in self.buildings(tile.index):
                building.collect(tile.resource)

    def assert_has_space(self, building: Building, corner: int):
        existing: Building = self._buildings[corner]
        if building.is_city:
            if existing is None:
                raise RuntimeError(f"no settlement at corner index {corner}")
            elif existing.is_city:
                raise RuntimeError(f"city already at corner index {corner}")
            elif existing.player != building.player:
                raise RuntimeError(f"settlement belongs to the wrong player: {existing.player.name}")
        else:
            if existing is not None:
                raise RuntimeError(f"already a building at corner index {corner}")
            for neighbor in CORNER_NEIGHBORS[corner]:
                if self._buildings[neighbor] is not None:
                    raise RuntimeError(f"cannot build, building at corner index {neighbor} is too close")

    def assert_connected(self, building: Building, corner: int):
        for edge in CORNERS_TO_EDGES[corner]:
            if self._roads[edge] == building.player:
                return
        raise RuntimeError(f"no connected road")

    def assert_can_build(self, building: Building, corner: int):
        self.assert_has_space(building, corner)
        self.assert_connected(building, corner)

    def build(self, building: Building, corner: int):
        self._buildings[corner] = building

        # check for breaking
        if not building.is_city:
            # get the roads by player
            player_roads = {}
            for edge in CORNERS_TO_EDGES[corner]:
                player = self._roads[edge]
                # disregard the player who is building
                if player is not None and player != building.player:
                    if player in player_roads:
                        player_roads[player] += 1
                    else:
                        player_roads[player] = 1

            # if any player has more than one connected roads, break the road
            for player, roads in player_roads.items():
                if roads > 1:
                    self._remeasure_roads(player)

    @property
    def robber_tile(self) -> int:
        return self._robber_tile

    def move_robber(self, tile: int):
        if self._robber_tile == tile:
            raise RuntimeError(f"Robber is already on {tile}. It must be moved to a new tile")
        self._robber_tile = tile

    def assert_can_steal(self, player: Player):
        for corner in TILE_TO_CORNERS[self._robber_tile]:
            building: Building = self._buildings[corner]
            if building is not None and building.player == player:
                return
        raise RuntimeError(f"Player {player.name} is not on tile {self._robber_tile} and cannot be stolen from")

    def _remeasure_roads(self, player):
        # reset longest road
        longest_road: LongestRoad = self._longest_roads[player]
        longest_road.length = -1

        # go through all the roads
        roads_measured = set()
        for edge in range(TOTAL_EDGES):
            if edge not in roads_measured and self._roads[edge] == player:
                road_len = self._road_length(edge, roads_measured)
                if road_len > longest_road.length:
                    longest_road.length = road_len
                    longest_road.edge = edge

        # update the longest road - only needed if remeasured player holds it
        top_len = longest_road.length
        if self._longest_road_holder == player:
            for other_player, road_len in self._longest_roads.items():
                if road_len.length > top_len:
                    top_len = road_len.length
                    self._longest_road_holder = other_player

    def assert_can_build_road(self, player: Player, edge: int):
        if self._roads[edge] is not None:
            raise RuntimeError(f"road already at edge {edge}, belongs to {self._roads[edge].name}")

        roads: Set[int] = set()
        if self._check_for_cycle(-1, edge, player, roads):
            raise RuntimeError(f"will result in cycle")

        for corner in EDGES_TO_CORNERS[edge]:
            for neighbor_edge in CORNERS_TO_EDGES[corner]:
                if self._roads[neighbor_edge] == player:
                    return
        raise RuntimeError(f"no connected road")

    def _connected(self, check_edge: int, target_edge: int):
        roads = set()
        self._road_length(check_edge, roads)
        return target_edge in roads

    def _check_for_cycle(self, from_edge: int, edge: int, player: Player, visited: Set[int]):
        cycle: bool = False
        from_corner: int = -1
        if from_edge != -1:
            from_corner = common_corner(edge, from_edge)
        for corner in EDGES_TO_CORNERS[edge]:
            if corner == from_corner:
                continue
            for neighbor_edge in CORNERS_TO_EDGES[corner]:
                if edge != neighbor_edge and self._roads[neighbor_edge] == player:
                    if neighbor_edge in visited:
                        return True
                    else:
                        visited.add(neighbor_edge)
                        check = self._check_for_cycle(edge, neighbor_edge, player, visited)
                        cycle = cycle or check
        return cycle

    def belongs_to_other(self, corner: int, player: Player) -> bool:
        building: Building = self._buildings[corner]
        return building is not None and player != building.player

    def build_road(self, player: Player, edge: int):
        # add to the board
        self._roads[edge] = player

        self._update_longest_road(player, edge)

    def _road_length(self, edge, roads_visited:Set = None):
        player: Player = self._roads[edge]
        if player is None:
            return 0

        # build tree recursively
        if roads_visited is not None:
            roads_visited.add(edge)
        road_tree: RoadTree = RoadTree(edge)
        self._expand_tree(-1, edge, player, road_tree, roads_visited)

        # get length
        return road_tree.get_max_len()

    def _expand_tree(self, from_edge: int, edge: int, player: Player, road_tree: RoadTree, roads_visited:Set):
        from_corner: int = -1
        if from_edge != -1:
            from_corner = common_corner(edge, from_edge)
        for corner in EDGES_TO_CORNERS[edge]:
            # ignore corner we expanded from and any corner that belongs to another player
            if corner == from_corner or self.belongs_to_other(corner, player):
                continue
            for neighbor_edge in CORNERS_TO_EDGES[corner]:
                if edge != neighbor_edge and self._roads[neighbor_edge] == player:
                    # confirmed neighbor, add and recurse
                    if roads_visited is not None:
                        roads_visited.add(neighbor_edge)
                    road_tree.add(neighbor_edge, edge)
                    self._expand_tree(edge, neighbor_edge, player, road_tree, roads_visited)

    def _update_longest_road(self, player: Player, *edges_to_check: int):
        # init longest road for player if needed
        if player not in self._longest_roads:
            self._longest_roads[player] = LongestRoad()

        # update longest road for the player if necessary
        for edge in edges_to_check:
            candidate = self._road_length(edge)
            if self._longest_roads[player].length < candidate:
                self._longest_roads[player].length = candidate
                self._longest_roads[player].edge = edge

        # update longest road on the board
        if self._longest_road_holder is None:
            if self._longest_roads[player].length > 4:
                self._longest_road_holder = player
        elif self._longest_roads[self._longest_road_holder].length < self._longest_roads[player].length:
            self._longest_road_holder = player

