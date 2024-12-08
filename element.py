import numpy as np

class Element:
    def __init__(self, nodes, gmshType=-1):
        self._nodes      = np.array(nodes, dtype=int)
        self._gmshtype   = int(gmshType)

    def getNodeCount(self):
        return len(self._nodes)

    def getNodes(self):
        return self._nodes

    def getGMSHType(self):
        return self._gmshtype