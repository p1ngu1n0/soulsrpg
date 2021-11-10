import pygame
from pygame import draw
from .player import Player, Enemy
from .utils import Director


class lvl1(Director):
    def __init__(self) -> None:
        super().__init__(self)
        self.plr = Player()
        self.enm = Enemy()

    def update(self):
        self.plr.update()
        self.enm.update()

        if pygame.sprite.collide_rect(self.plr, self.enm):
            if self.plr.pos in [1, 3]:
                if self.plr.rect.top <= self.enm.rect.bottom and self.enm.rect.bottom < self.plr.rect.bottom:
                    self.plr.rect.top = self.enm.rect.bottom
                elif self.plr.rect.bottom >= self.enm.rect.top and self.enm.rect.top > self.plr.rect.top:
                    self.plr.rect.bottom = self.enm.rect.top

            if self.plr.pos in [0, 2]:
                if self.plr.rect.left <= self.enm.rect.right and self.enm.rect.right < self.plr.rect.right:
                    self.plr.rect.left = self.enm.rect.right
                elif self.plr.rect.right >= self.enm.rect.left and self.enm.rect.left > self.plr.rect.left:
                    self.plr.rect.right = self.enm.rect.left

    def draw(self, screen):
        screen.fill((0, 0, 0))
        self.plr.draw(self.screen)
        self.enm.draw(self.screen)
