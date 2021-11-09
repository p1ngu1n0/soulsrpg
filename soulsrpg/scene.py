from abc import ABC, abstractmethod
from OpenGL.GL import *
from typing import Dict, overload
import numpy as np
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
    mouse:      MouseListener
    keyboard:   KeyListener
    shader:     Shader  

    def __init__(self, keyboard: KeyListener, mouse: MouseListener):
        self.shader   = Shader("default")
        self.keyboard = keyboard
        self.mouse    = mouse

    def update(self, dt: float):
        pass

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


