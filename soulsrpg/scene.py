from abc import ABC, abstractmethod
from OpenGL.GL import *
from typing import Dict, overload
import numpy as np
from math import sin, cos, pi
import sys
import time
import pyrr

from .ecs import Entity, Component
from .shaders import Shader
from .texture import Texture
from .mesh import Mesh
from .listener import *
from .camera import Camera

class Scene(ABC):
    is_running: bool = False
    entities: List[Entity] = []

    def start(self):
        self.is_running = True
        for e in self.entities:
            e.start()

    def update(self, dt: float):
        for e in self.entities:
            e.update(dt)

    def render(self):
        for e in self.entities:
            e.render()

class SceneManager(object):
    it: float
    scenes: Dict[str, Scene]
    default_order: List[str]
    curr_scene: Optional[str] = None

    def __init__(self, default_order: List[str], scenes: Dict[str, Scene]):
        self.it = time.time()
        self.default_order = default_order
        self.scenes = scenes
        self.change_scene(default_order[0])

    def add_scene(self, scene_name: str, scene: Scene):
        self.scenes.append({scene_name, scene})

    def del_scene(self, scene_name: str):
        try:
            del self.scenes[scene_name]
            del self.default_order[0]
            self.curr_scene = None
        except KeyError:
            sys.exit(f"Scene with name: {scene_name} failed to delete")

    def set_order(self, new_order: List[str]):
        self.default_order = new_order

    def check(self):
        if self.curr_scene == None:
            try: 
                self.scenes[self.default_order[0]]
                self.curr_scene = self.default_order[0]
            except IndexError:
                sys.exit("Cannot get current scene")

    def change_scene(self, scene_name: Optional[str] = None):
        self.check()
        if scene_name == None:
            # NOTE: Should I remove scenes on change?
            # del self.default_order[0]
            if len(self.default_order) > 0:
                self.scenes[self.curr_scene].is_running = False
                self.curr_scene = self.default_order[1]
                self.scenes[self.curr_scene].start()
                return
            else:
                sys.exit("Cannot change scene, EOG")
        if not scene_name in self.default_order:
            sys.exit("Scecne not avaible")
        
        for k, v in self.scenes.items():
            if k == scene_name:
                v.start()
                self.curr_scene = scene_name
                return
        sys.exit("Unexpected error")

    def update(self):
        self.check()
        dt = time.time() - self.it
        self.it = time.time()
        self.scenes[self.curr_scene].update(dt)

    def render(self):
        self.check()
        self.scenes[self.curr_scene].render()

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

    def add_entity(self, e: Entity):
        if not self.is_running:
            self.entities.append(e)
        else:
            self.entities.append(e)
            e.start()

    def start(self):
        print("Starting Level Scene")
        super().start()

    def update(self, dt: float):
        super().update(dt)
        self.camera.position[0] -= dt * 50.0
        self.camera.position[1] -= dt * 50.0

        self.shader.use()
        self.shader.upload("uView", self.camera.get_view())
        self.shader.upload("uProj", self.camera.get_proj())

        self.it = abs(sin(time.time()))
        self.shader.upload("uTime", self.it)
        self.shader.detach()

    def render(self):
        super().render()
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
