from typing import Optional


class Edge:
    """Connects two corners; a road can be built here"""

    def __init__(self):
        self.owner: Optional['Player'] = None
