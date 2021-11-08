from typing import ClassVar
import pygame
from pygame.locals import *

class Director(object):
    def __init__(self, scene ,ALTO: int = 800, ANCHO: int = 600) -> None:
        pygame.init()
        self.scene = scene
        self.run = True
        self.screen = pygame.display.set_mode((ALTO, ANCHO))
        pygame.display.set_caption("soulsrpg")
        self.reloj = pygame.time.Clock()
    
    def loop(self) -> None:
        while self.run:
            self.scene.update(self)
            self.scene.draw(self)
        pygame.quit()
