import pygame
from pygame import key
from pygame.constants import K_DOWN, K_LEFT, K_RIGHT, K_UP

class Player(pygame.sprite.Sprite):
    def __init__(self, **stats) -> None:
        super().__init__()
        self.hp = stats.get("hp", int)
        self.exp = stats.get("exp", int)
        self.lvl = stats.get("lvl", int)
        self.live = stats.get("live", int)
        self.plr_x = stats.get("plr_x", int)
        self.plr_y = stats.get("plr_y", int)
        self.speed = stats.get("speed", 3)
        self.stamina = stats.get("stamina", int)
        self.image = pygame.image.load("assets/player.png")
        self.rect = self.image.get_rect()
        self.estado = 0

    def update(self) -> None:
        keys = pygame.key.get_pressed()
        if keys[K_RIGHT]:
            self.rect.centerx += self.speed
            self.estado = 256
        elif keys[K_LEFT]:
            self.rect.centerx -= self.speed
            self.estado = 128
        elif keys[K_UP]:
            self.rect.centery -= self.speed
            self.estado = 0
        elif keys[K_DOWN]:
            self.rect.centery += self.speed

    def draw(self, screen):
        screen.blit(self.image, self.rect, (self.estado, 0, 128, 192))
