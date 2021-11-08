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
    keyboard: KeyListener
    # pad: PadListener**
    # pencil: PencilListener**
    # mic: AudioListener**
    
    def __init__(self, title: str, size: Tuple[int, int], scene: None):
        # Initialize pygame and the window
        pygame.init()
        self.window_surface = pygame.display.set_mode(size) #, DOUBLEBUF | OPENGL)
        pygame.display.set_caption(title)

        # States initialization
        self.running = True
        self.mouse = MouseListener()
        self.keyboard = KeyListener()
        self.img = pygame.image.load("assets/cara.png")
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

        if self.keyboard.key(K_a):
            print("Pressed A")

    def render(self):
        """ Main rendering

            When scene manager defined requires on it to call `render` method in the active
            scenes
        """

        # Clear backbuffer
        # gl.glClearColor(0.3, 0.2, 0.1, 1.0)
        # gl.glClear(gl.GL_COLOR_BUFFER_BIT)
        self.window_surface.blit(self.img, (-30, -30))
        # self.scene.draw()

        # Swap buffers
        pygame.display.flip()
