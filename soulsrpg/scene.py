from abc import ABC, abstractmethod
from OpenGL.GL import *
from typing import Dict, overload
import numpy as np
from math import sin, cos, pi
import sys
import time
import pyrr

from .shaders import Shader, Mesh, Texture
from .listener import *
from .camera import Camera

class Scene(ABC):
    @abstractmethod
    def update(self, dt: float):
        pass

    @abstractmethod
    def render(self):
        pass

class SceneManager(object):
    it: float
    scenes: Dict[str, Scene]
    default_order: List[str]

    def __init__(self, default_order: List[str], scenes: Dict[str, Scene] = []):
        self.it = time.time()
        self.default_order = default_order
        self.scenes = scenes

    def add_scene(self, scene_name: str, scene: Scene):
        self.scenes.append({scene_name, scene})

    def del_scene(self, scene_name: str):
        try:
            del self.scenes[scene_name]
        except KeyError:
            sys.exit(f"Scene with name: {scene_name} failed to delete")

    def set_order(self, order: List[str]):
        self.default_order = order

    def update(self):
        try:
            dt = time.time() - self.it
            self.it = time.time()
            self.scenes[self.default_order[0]].update(dt)
        except IndexError:
            sys.exit("Scene Manager got out of scenes")

    def render(self):
        try:
            self.scenes[self.default_order[0]].render()
        except IndexError:
            sys.exit("Scene Manager got out of scenes")

class LevelScene(Scene, object):
    it: float
    mouse:      MouseListener
    keyboard:   KeyListener
    shader:     Shader  
    camera:     Camera

    def __init__(self, keyboard: KeyListener, mouse: MouseListener):
        self.it       = time.time()
        self.shader   = Shader("default")
        self.keyboard = keyboard
        self.mouse    = mouse
        self.camera = Camera(np.array([0.0, 0.0, 20.0], dtype=np.float32))

    def update(self, dt: float):
        self.shader.use()
        self.camera.adjust_proj()
        self.shader.upload("uView", self.camera.get_view())
        self.shader.upload("uProj", self.camera.get_proj())

        self.it = abs(sin(time.time()))
        self.shader.upload("uTime", self.it)
        self.shader.detach()

    def render(self):
        VERTICES = np.array([
            -50.7, -50.7, 0.0,    0.0, 0.0,
            -50.7,  50.7, 0.0,    0.0, 1.0,
            50.7,   50.7, 0.0,    1.0, 1.0,
            50.7,  -50.7, 0.0,    1.0, 0.0
        ], dtype=np.float32)
        INDICES = np.array([0, 1, 3, 1, 2, 3])

        self.shader.use()
        # self.shader.upload("uView", self.camera.get_view())
        triangle = Mesh(VERTICES, INDICES)
        wall = Texture("wall.jpg")

        triangle.draw()
        self.shader.detach()

def trans(tx: float, ty: float, tz: float = 0.0) -> np.array: 
    """ Returns a translation matrix
    """
    return np.array([[1.0, 0.0, 0.0, tx],
                     [0.0, 1.0, 0.0, ty],
                     [0.0, 0.0, 1.0, tz],
                     [0.0, 0.0, 0.0, 1.0]],
                    dtype=np.float32).transpose()

def scale(sx: float, sy: float, sz: float = 1.0) -> np.array: 
    """ Returns a scaling matrix
    """
    return np.array([[sx, 0.0, 0.0, 0.0],
                     [0.0, sy, 0.0, 0.0],
                     [0.0, 0.0, sz, 0.0],
                     [0.0, 0.0, 0.0, 1.0]],
                    dtype=np.float32).transpose()

def rot_x(rad: float) -> np.array: 
    """ Returns rotation matrix (x axis)
    """
    return np.array([[1.0, 0.0,      0.0,       0.0],
                     [0.0, cos(rad), -sin(rad), 0.0],
                     [0.0, sin(rad), cos(rad),  0.0],
                     [0.0, 0.0,      0.0,       1.0]],
                    dtype=np.float32).transpose()

def rot_y(rad: float) -> np.array: 
    """ Returns rotation matrix (y axis)
    """
    return np.array([[cos(rad),  0.0, sin(rad), 0.0],
                     [0.0,       1.0, 0.0,      0.0],
                     [-sin(rad), 0.0, cos(rad), 0.0],
                     [0.0,       0.0, 0.0,      1.0]],
                    dtype=np.float32).transpose()

def rot_z(rad: float) -> np.array: 
    """ Returns rotation matrix (z axis)
    """
    return np.array([[cos(rad),  -sin(rad), 0.0, 0.0],
                     [sin(rad),  cos(rad),  0.0, 0.0],
                     [0.0,       0.0,       1.0, 0.0],
                     [0.0,       0.0,       0.0, 1.0]],
                    dtype=np.float32).transpose()

def deg(deg: float) -> float:
    """ degrees -> radians """
    return deg * ((2 * pi) / 360.0)
