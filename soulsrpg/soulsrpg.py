import pygame
from pygame.locals import *
from typing import NamedTuple, Tuple, overload
from abc import ABC, abstractmethod

class Scene(ABC):
    @abstractmethod
    def update(self, dt: float):
        pass

    @abstractmethod
    def render(self):
        pass

class Game(object):
    window_surface: pygame.Surface
    running: bool
    
    def __init__(self, title: str, size: Tuple[int, int]):
        self.running = True

        pygame.init()
        self.window_surface = pygame.display.set_mode(size, DOUBLEBUF | OPENGL)
        pygame.display.set_caption(title)

    def run(self):
        while self.running:
            self.update()
            self.draw()
            running = False

    def update(self):
        pass

    def draw(self):
        pass
