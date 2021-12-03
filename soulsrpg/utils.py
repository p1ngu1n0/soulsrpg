
import pygame
from pygame.locals import *

from soulsrpg.player import Player


class Director(object):
    def __init__(self, scene, ALTO: int = 800, ANCHO: int = 600) -> None:
        pygame.init()
        self.scene = scene
        self.run = True
        self.alto = ALTO
        self.ancho = ANCHO
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
    def __init__(self, tile: str, numImgx: int, numImgy: int) -> None:
        self.tile = pygame.image.load(tile).convert()
        self.size = self.tile.get_size()
        self.tilemap = []
        self.numImgx = numImgx
        self.numImgy = numImgy
        self.startPos = (0, 0)
        self.x, self.y = self.size
        self.h, self.w = (self.x/self.numImgx), (self.y/self.numImgy)
        self.tdic = dict(enumerate((y, x)  for x in range(0, self.y, int(self.w)) for y in range(0, self.x, int(self.w))))
        
        
        
    def gen_tile(self, lvl: list, sizex: int) -> list:
        return [(x, y) for y in range(0, len(lvl)) for x in range(0, len(lvl[0]))]
    
    def gen_map(self, alto, ancho, material) -> list:
        self.tilemap = [[material]*int(alto/self.h)]*int(ancho/self.w)
    
    def change_material(self, x: int, y: int, material: int):
        self.tilemap[y][x] = material
    
    def draw(self, screen, lvl: list):
        for nx, ny in self.gen_tile(lvl, self.w):
            rx, ry = self.tdic[lvl[ny][nx]]
            screen.blit(self.tile, (nx*self.w, ny*self.w), (rx, ry, self.w, self.h))
            
                    
                    
