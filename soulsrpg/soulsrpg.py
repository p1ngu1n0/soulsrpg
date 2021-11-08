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
    # The surface where to draw
    window_surface: pygame.Surface
    # Variable to know when to stop the game
    running: bool
    
    def __init__(self, title: str, size: Tuple[int, int]):
        self.running = True

        # Initialize pygame and the window
        pygame.init()
        self.window_surface = pygame.display.set_mode(size, DOUBLEBUF | OPENGL)
        pygame.display.set_caption(title)

    def run(self):
        """ Game main loop 
        """
        while self.running:
            self.update()
            self.draw()

         # No cleanup `pygame.quit()` needed as the application is going to fully close
         # Here state saves will be placed
         # Exit the application with no errors
        sys.exit(0)

    def update(self):
        """ Gets pygame events and register them in the `MouseListener`, `KeyListener` and
            `PadListener`** `PencilListener`**. Also handles high level events like QUIT.

            When scene manager defined requires on it to call `update` method on the active 
            scenes

            ** = super optional
        """

        for event in pygame.event.get():
            if event.type == QUIT:
                running = False

    def draw(self):
        """ Main rendering

            When scene manager defined requires on it to call `render` method in the active
            scenes
        """
        pygame.display.update()
