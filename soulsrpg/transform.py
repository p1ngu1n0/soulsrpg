import sys
import numpy as np

class Transform(object):
    position: np.array
    scale:    np.array

    def __init__(self, position: np.array, scale: np.array):
        if position.dtype != np.float32 or scale.dtype != np.float32:
            sys.exit("Only float32 supported for Transform")
        self.position = position
        self.scale    = scale
