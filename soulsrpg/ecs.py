from abc import ABC, abstractmethod
from typing import Optional, List

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

class Entity(object):
    name: str
    # No duplicates allowed
    components: List[Component]

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

        
        

