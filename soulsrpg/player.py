import pygame
from pygame.constants import K_LEFT, K_RIGHT

class Player(pygame.sprite.Sprite):
    def __init__(self, **stats) -> None:
        super().__init__()
        self.hp = stats.get("hp", int)
        self.exp = stats.get("exp", int)
        self.lvl = stats.get("lvl", int)
        self.live = stats.get("live", int)
        self.plr_x = stats.get("plr_x", int)
        self.plr_y = stats.get("plr_y", int)
        self.stamina = stats.get("stamina", int)
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
