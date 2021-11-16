from abc import ABC, abstractmethod
from typing import Optional, List

from .transform import Transform

"""
ECS (Entity Component System)
This is for a efficient entity management, to add for example an `Enemy` to the game
just make the `Enemy` class inherit from `Entity` implement its methods and add to it
functionality via components, for example the health might be a component also, texture of
the enemy, also its ai
"""

class Entity(object):
    pass

class Component(ABC):
    parent: Optional[Entity] = None

    @abstractmethod
    def update(self, dt: float):
        pass

    @abstractmethod
    def start(self):
        pass

    def render(self):
        pass

class Entity(object):
    name: str
    # No duplicates allowed
    components: List[Component] = []

    # Some special default components for every entity
    transform: Transform

    def __init__(self, name: str):
        self.name = name

    def get_comp(self, comp_class: type) -> Component:
        """ Gets a component given its class, just returns the first one
        """
        for c in self.components:
            if c.__class__ == comp_class:
                return c
        else:
            # NOTE(cdecompilador): Should this error be recovereable
            sys.exit("Component not found")

    def rm_comp(self, comp_class: type): 
        """ Gets a component given its class, just returns the first one
        """
        for c in self.components:
            if c.__class__ == comp_class:
                del c
        else:
            # NOTE(cdecompilador): Should this error be recovereable
            sys.exit("Component not found")

    def add_comp(self, comp: Component):
        self.components.append(comp)
        comp.parent = self

    def update(self, dt: float):
        for c in self.components:
            c.update(dt) 

    def start(self):
        for c in self.components:
            c.start(dt)

        
        

