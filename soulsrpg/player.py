import pygame
from pygame.constants import K_LEFT, K_RIGHT


class Player(pygame.sprite.Sprite):
    def __init__(self, hp: int = 10, stamina: int = 10, exp: int = 0, lvl: int = 0, live: bool = True, souls: int = 0, plr_x: int = 0, plr_y: int = 0) -> None:
        super().__init__()
        self.hp = hp
        self.exp = exp
        self.lvl = lvl
        self.live = live
        self.plr_x = plr_x
        self.plr_y = plr_y
        self.stamina = stamina
        self.image = pygame.image.load("assets/cara.png").convert()
        self.rect = self.image.get_rect()

    def update(self) -> None:
        keys = pygame.key.get_pressed()
        if keys[K_RIGHT]:
            self.rect.centerx += 1
        elif keys[K_LEFT]:
            self.rect.centerx -= 1

    def draw(self, screen):
        screen.blit(self.image, (self.plr_x, self.plr_y))
