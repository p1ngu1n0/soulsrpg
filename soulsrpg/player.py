import pygame
from pygame.constants import K_DOWN, K_LCTRL, K_LEFT, K_RIGHT, K_UP


class Player(pygame.sprite.Sprite):
    def __init__(self, **stats) -> None:
        super().__init__()
        self.hp = stats.get("hp", int)
        self.exp = stats.get("exp", int)
        self.lvl = stats.get("lvl", int)
        self.live = stats.get("live", bool)
        self.speed = stats.get("speed", 3)
        self.stamina = stats.get("stamina", int)
        self.pos = stats.get("pos", 0)
        self.rect = pygame.Rect(300, 300, 64, 64)
        self.attack = stats.get("attack", False)

    def update(self) -> None:
        keys = pygame.key.get_pressed()
        if keys[K_RIGHT]:
            self.rect.centerx += self.speed
            self.pos = 0
        elif keys[K_LEFT]:
            self.rect.centerx -= self.speed
            self.pos = 2
        elif keys[K_DOWN]:
            self.rect.centery += self.speed
            self.pos = 1
        elif keys[K_UP]:
            self.rect.centery -= self.speed
            self.pos = 3
        elif keys[K_LCTRL]:
            self.attack = True

    def draw(self, screen):
        pygame.draw.rect(screen, (255, 0, 0), self.rect, 2)
        if self.attack:
            rect = pygame.Rect(0, 0, 32, 32)
            rect.center = self.pos_attack(self.pos)
            pygame.draw.rect(screen, (255, 0, 0), self.rect, 2)
            if pygame.time.get_ticks() >= 500:
                self.attack = False

    def pos_attack(self, pos: int) -> int:
        self.pos = pos
        match self.pos:
            case 0: return (self.rect.x+32, self.rect.y)
            case 1: return (self.rect.x, self.rect.y+32)
            case 2: return (self.rect.x-32, self.rect.y)
            case 3: return (self.rect.x, self.rect.y-32)


class Enemy(pygame.sprite.Sprite):
    def __init__(self, **stats) -> None:
        super().__init__()
        self.hp = stats.get("hp", int)
        self.exp = stats.get("exp", int)
        self.lvl = stats.get("lvl", int)
        self.live = stats.get("live", bool)
        self.enm_x = stats.get("enm_x", 200)
        self.enm_y = stats.get("enm_y", 200)
        self.speed = stats.get("speed", 1)
        self.stamina = stats.get("stamina", int)
        self.pos = stats.get("pos", 0)
        self.attack = stats.get("attack", False)
        self.rect = pygame.Rect(self.enm_x, self.enm_y, 64, 64)
        self.move = True

    def update(self):
        if self.move:
            self.rect.centerx += 3
            if pygame.time.get_ticks() >= 500:
                self.move = False

    def draw(self, screen):
        pygame.draw.rect(screen, (0, 255, 0), self.rect, 2)
