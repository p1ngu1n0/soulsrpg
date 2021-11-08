import sys
import pygame
from pygame.locals import *
from typing import NamedTuple, Tuple, overload
from abc import ABC, abstractmethod
import OpenGL.GL as gl
from OpenGL.GLU import *

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
    # keyboard: KeyListener
    # pad: PadListener**
    # pencil: PencilListener**
    # mic: AudioListener**
    
    def __init__(self, title: str, size: Tuple[int, int], scene: None):
        # Initialize pygame and the window
        pygame.init()
<<<<<<< HEAD
        self.window_surface = pygame.display.set_mode(size) #, DOUBLEBUF | OPENGL)
        pygame.display.set_caption(title)

        # States initialization
        self.running = True
        self.mouse = MouseListener()
        self.img = pygame.image.load("assets/cara.png")
=======
        # self.scene = scene
        self.window_surface = pygame.display.set_mode(size, DOUBLEBUF | OPENGL)
        pygame.display.set_caption(title)
        # pygame.mouse.set_visible(False)
        # self.img = pygame.image.load("assets/cara.png")
>>>>>>> df25ae5c50b29a7e6c5046884951a3f8d7b16fae
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

        if self.mouse.is_dragging:
            print("Dragging")

    def render(self):
        """ Main rendering

            When scene manager defined requires on it to call `render` method in the active
            scenes
        """

        # Clear backbuffer
<<<<<<< HEAD
        # gl.glClearColor(0.3, 0.2, 0.1, 1.0)
        # gl.glClear(gl.GL_COLOR_BUFFER_BIT)
        self.window_surface.blit(self.img, (-30, -30))
=======
        gl.glClearColor(0.3, 0.2, 0.1, 1.0)
        gl.glClear(gl.GL_COLOR_BUFFER_BIT | gl.GL_DEPTH_BUFFER_BIT)
        # self.window_surface.blit(self.img, (-30, -30))
>>>>>>> df25ae5c50b29a7e6c5046884951a3f8d7b16fae
        # self.scene.draw()

        # Swap buffers
        pygame.display.flip()
