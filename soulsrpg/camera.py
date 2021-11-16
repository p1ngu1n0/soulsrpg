import numpy as np
import pyrr

from .shaders import Shader
from .mesh import Mesh
from .texture import Texture


class Camera(object):
    proj_matrix: np.array
    view_matrix: np.array
    position:    np.array

    def __init__(self, position: np.array):
        self.proj_matrix = np.zeros((4, 4))
        self.view_matrix = np.zeros((4, 4))
        self.position = position
        self.adjust_proj()

    def adjust_proj(self):
        B = 0.0
        T = 32.0 * 21.0
        L = 0.0
        R = 32.0 * 40.0
        F = 100.0
        N = -1.0
        self.proj_matrix = np.array([[2/(R-L), 0.0,     0.0,      0.0],
                                     [0.0,     2/(T-B), 0.0,      0.0],
                                     [0.0,     0.0,     -2/(F-N), 0.0],
                                     [-(R+L)/(R-L),     -(T+B)/(T-B),    -(F+N)/(F-N),      1.0]],
                                     dtype=np.float32)
        test = pyrr.matrix44.create_orthogonal_projection(L, R, B, T, N, F, dtype=np.float32)
        assert np.array_equal(test, self.proj_matrix)
        """
        self.proj_matrix = pyrr.matrix44.create_orthogonal_projection(
            0.0, 32.0 * 40.0,
            0.0, 32.0 * 21.0,
            0.0, 100.0, dtype=np.float32)
        """

    def get_proj(self) -> np.array:
        return self.proj_matrix

    def get_view(self) -> np.array:
        # Where the camera is looking
        camera_target = np.array([0.0, 0.0, 0.0], dtype=np.float32)
        camera_dir = self.position - np.array([0.0, 0.0, -1.0], dtype=np.float32)
        camera_dir = camera_dir / np.linalg.norm(camera_dir, ord=1)

        # Setup where is up and right from where the camera is
        up = np.array([0.0, 1.0, 0.0], dtype=np.float32)
        camera_right = np.cross(up, camera_dir)
        camera_right = camera_right / np.linalg.norm(camera_right, ord=1)
        camera_up    = np.cross(camera_dir, camera_right)
        camera_up    = camera_up / np.linalg.norm(camera_up, axis=0)

        self.view_matrix =  np.array([
            [camera_right[0], camera_right[1], camera_right[2], 0.0],
            [camera_up[0],    camera_up[1],    camera_up[2],    0.0],
            [camera_dir[0],   camera_dir[1],   camera_dir[2],   0.0],
            [0.0, 0.0, 0.0, 1.0]
            ], dtype=np.float32) @ np.array([[1.0, 0.0, 0.0, -self.position[0]],
                                             [0.0, 1.0, 0.0, -self.position[1]],
                                             [0.0, 0.0, 1.0, -self.position[2]],
                                             [0.0, 0.0, 0.0, 1.0]], dtype=np.float32)
        self.view_matrix = self.view_matrix.transpose()
        
        camera_front = np.array([0.0, 0.0, -1.0])
        camera_up    = np.array([0.0, 1.0, 0.0])
        test = pyrr.matrix44.create_look_at(self.position, 
                np.array([self.position[0], self.position[1], 0.0]), up, dtype=np.float32)

        return test

    """
    def get_view(self) -> np.array:
        camera_front = np.array([0.0, 0.0, -1.0], dtype=np.float32)
        camera_up    = np.array([0.0, 1.0,  0.0], dtype=np.float32)
        self.view_matrix = pyrr.matrix44.create_look_at(
            self.position, camera_front + np.array([
                self.position[0],
                self.position[1],
                0.0
            ], dtype=np.float32), camera_up, dtype=np.float32
        )
        return self.view_matrix
    """


