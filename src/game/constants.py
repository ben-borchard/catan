from enum import Enum


class ResourceType(Enum):
    ROCK = "rock"
    BRICK = "brick"
    WHEAT = "wheat"
    WOOD = "wood"
    SHEEP = "sheep"

class DevelopmentCardType(Enum):
    KNIGHT = "knight"
    MONOPOLY = "monopoly"
    ROAD_BUILDING = "road building"
    YEAR_OF_PLENTY = "year of plenty"
    VICTORY_POINT = "victory point"

class GamePhase(Enum):
    SETUP = "setup"
    PRE_ROLL = "pre-roll"
    ROLL_READY = "roll-ready"
    POST_ROLL = "post-roll"
    DISCARD = "discard"
    STEAL = "steal"
    ROBBER = "robber"
