from abc import ABC, abstractmethod
from OpenGL.GL import *
from typing import Dict, overload
import numpy as np
from math import sin, cos, pi
import time

from .shaders import Shader, Mesh, Texture
from .listener import *

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

    def __init__(self, keyboard: KeyListener, mouse: MouseListener):
        self.it       = time.time()
        self.shader   = Shader("default")
        self.keyboard = keyboard
        self.mouse    = mouse

    def update(self, dt: float):
        self.it = time.time() * 40
        mat = rot_x(deg(self.it)) @ rot_y(deg(self.it)) @ scale(0.5, 0.5, 0.5)
        self.shader.upload("transform", mat)

    def render(self):
        VERTICES = np.array([
            -0.7, -0.7, 0.0,    0.0, 0.0,
            -0.7,  0.7, 0.0,    0.0, 1.0,
            0.7,   0.7, 0.0,    1.0, 1.0,
            0.7,  -0.7, 0.0,    1.0, 0.0
        ], dtype=np.float32)
        INDICES = np.array([0, 1, 3, 1, 2, 3])

        self.shader.use()
        triangle = Mesh(VERTICES, INDICES)
        wall = Texture("wall.jpg")

        triangle.draw()

def trans(tx: float, ty: float, tz: float = 0.0) -> np.array: 
    return np.array([[1.0, 0.0, 0.0, tx],
                     [0.0, 1.0, 0.0, ty],
                     [0.0, 0.0, 1.0, tz],
                     [0.0, 0.0, 0.0, 1.0]],
                    dtype=np.float64)

def scale(sx: float, sy: float, sz: float = 1.0) -> np.array: 
    return np.array([[sx, 0.0, 0.0, 0.0],
                     [0.0, sy, 0.0, 0.0],
                     [0.0, 0.0, sz, 0.0],
                     [0.0, 0.0, 0.0, 1.0]],
                    dtype=np.float64)

def rot_x(rad: float) -> np.array: 
    return np.array([[1.0, 0.0,      0.0,       0.0],
                     [0.0, cos(rad), -sin(rad), 0.0],
                     [0.0, sin(rad), cos(rad),  0.0],
                     [0.0, 0.0,      0.0,       1.0]],
                    dtype=np.float64)

def rot_y(rad: float) -> np.array: 
    return np.array([[cos(rad),  0.0, sin(rad), 0.0],
                     [0.0,       1.0, 0.0,      0.0],
                     [-sin(rad), 0.0, cos(rad), 0.0],
                     [0.0,       0.0, 0.0,      1.0]],
                    dtype=np.float64)

def rot_z(rad: float) -> np.array: 
    return np.array([[cos(rad),  -sin(rad), 0.0, 0.0],
                     [sin(rad),  cos(rad),  0.0, 0.0],
                     [0.0,       0.0,       1.0, 0.0],
                     [0.0,       0.0,       0.0, 1.0]],
                    dtype=np.float64)

def deg(deg: float) -> float:
    return deg * ((2 * pi) / 360.0)
