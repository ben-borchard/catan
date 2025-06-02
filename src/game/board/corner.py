
class Corner:
    """Intersection point of up to 3 tiles"""

    def __init__(self):
        self.building: Optional['Building'] = None  # Settlement or City
