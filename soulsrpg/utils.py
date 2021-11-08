import pygame
from pygame.locals import *
from typing import NamedTuple, Tuple, overload
from abc import ABC, abstractmethod
from OpenGL.GL import *
from OpenGL.GLU import *
import numpy as np

from .shaders import Shader, Mesh
from .listener import *

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
    # Listeners
    mouse: MouseListener
    keyboard: KeyListener
    # pad: PadListener**
    # pencil: PencilListener**
    # mic: AudioListener**
    
    def __init__(self, title: str, size: Tuple[int, int], scene: None):
        # Initialize pygame and the window
        pygame.init()
        self.window_surface = pygame.display.set_mode(size, DOUBLEBUF | OPENGL)
        pygame.display.set_caption(title)

        # States initialization
        self.running = True
        self.mouse = MouseListener()
        self.keyboard = KeyListener()
        self.clock = pygame.time.Clock()

    def run(self):
        """ Game main loop 
        """
        while self.running:
            self.clock.tick(60)
            self.update()
            self.render()

         # No cleanup `pygame.quit()` needed as the application is going to fully close
         # Here state saves will be placed
         # Exit the application with no errors

    def update(self):
        """ Gets pygame events and register them in the `MouseListener`, `KeyListener` and
            `PadListener`** `PencilListener`**. Also handles high level events like QUIT.

            When scene manager defined requires on it to call `update` method on the active 
            scenes

            ** = super optional
        """
        
        self.mouse.reset()
        for event in pygame.event.get():
            if event.type == QUIT:
                self.running = False
            else:
                self.mouse.retrieve(event)
        self.keyboard.retreive()

        if self.mouse.is_dragging:
            print("Dragging")
        if self.mouse.rel() != (0.0, 0.0) and not self.mouse.is_dragging:
            print("Just Mouse move")

    def render(self):
        """ Main rendering

            When scene manager defined requires on it to call `render` method in the active
            scenes
        """
        VERTICES = np.array([
            -0.2, -0.2, 0.0,
            0.0,   0.2, 0.0,
            0.2,  -0.2, 0.0
        ], dtype=np.float32)
        def_shader = Shader("default")
        def_shader.use()
        triangle = Mesh(VERTICES)
        # Clear backbuffer
        glClearColor(0.3, 0.2, 0.1, 1.0)
        glClear(GL_COLOR_BUFFER_BIT)
        triangle.draw()
        # Swap buffers
        pygame.display.flip()
