
import pygame
from pygame.locals import *

from soulsrpg.player import Player


class Director(object):
    def __init__(self, scene, ALTO: int = 800, ANCHO: int = 600) -> None:
        pygame.init()
        self.scene = scene
        self.run = True
        self.screen = pygame.display.set_mode((ALTO, ANCHO), pygame.RESIZABLE)
        pygame.display.set_caption("soulsrpg")
        self.reloj = pygame.time.Clock()

    def loop(self) -> None:
        while self.run:
            self.reloj.tick(60)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.run = False
            self.scene.update()
            self.scene.draw(self.screen)
            pygame.display.update()
        pygame.quit()


class TileSet(object):
    def __init__(self, tile) -> None:
        self.tile = tile
