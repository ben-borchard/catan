from random import random


class Dice:
    @staticmethod
    def roll() -> int:
        return random.randint(1, 6) + random.randint(1, 6)
