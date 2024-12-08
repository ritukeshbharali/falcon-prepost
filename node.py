import numpy as np

class Node:
    def __init__(self, coords):
        self._coords = np.array(coords, dtype=float)

    def dim(self):
        return len(self._coords)

    def getCoords(self):
        return self._coords