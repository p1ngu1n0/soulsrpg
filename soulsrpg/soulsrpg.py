import pygame
from pygame.locals import *
from typing import NamedTuple, Tuple, overload

class Game(object):
    window_surface: pygame.Surface
    
    def __init__(self, title: str, size: Tuple[int, int]):
        pygame.init()
        self.window_surface = pygame.display.set_mode(size, DOUBLEBUF | OPENGL)
        pygame.display.set_caption(title)

"""
def main() -> int:
    g = Game("Hello pygame", (500, 500))
    return 0

if __name__ == "__main__":
    exit(main())
"""
