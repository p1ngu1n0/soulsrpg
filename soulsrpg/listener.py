from typing import Tuple, List
import pygame

# Cool optimizations that will make code more readable without performance overhead
# FIXME: Not working properly with python 3.10, maybe clone this depenency in repo
#from inliner import inline 

# Constants (Maybe using an enum?)
M_RIGHT  = 0
M_CENTER = 1
M_LEFT   = 2

class MouseListener(object):
    """ Registers all important mouse states and them let convenient methods to access them
        TODO: Maybe using numpy will impove performance
    """
    scroll:   Tuple[float, float]
    # Positions d(pos) = pos - last_pos
    pos:      Tuple[float, float]
    last_pos: Tuple[float, float]
    # If any is being pressed while movement
    is_dragging: bool
    # false=unpressed, true=pressed
    # TODO: Support more buttons
    buttons_pressed: List[bool] 

    def __init__(self):
        self.scroll      = (0.0, 0.0)
        self.pos         = (0.0, 0.0)
        self.last_pos    = (0.0, 0.0)
        self.is_dragging = False
        self.buttons_pressed  = [False, False, False]

    def retrieve(self, event: pygame.event.Event):
        """ Function use to update this class state, called in game loop """

        # In `SDL.h` there are just defined mouse events with type (int) [0x400-0x403], so 
        # I filter them before everything for the sake of speed
        if 0x400 <= event.type <= 0x403:
            # print(self.__dict__)
            match event.type:
                # Contains `pos`, `rel` and `buttons` fields
                case pygame.MOUSEMOTION:
                    self._motion(event)
                    # TODO(cdecompilador): MOUSEMOTION also contains a `buttons` field in the
                    # __dict__ so maybe also update buttons here
                # Contains `pos` and `button` fields
                case pygame.MOUSEBUTTONUP | pygame.MOUSEBUTTONDOWN:
                    # This order matters, if changes `is_dragging` brokes
                    self._button(event)
                    self._motion(event)
                case pygame.MOUSEWHEEL:
                    self._scroll(event)

    # NOTE(cdecompilador): Some of this functions are redundant A.prop() -> A.prop, but in the
    # future if the backtypes change the API will remain the same so its ok to do this, for 
    # example if the holder for `scroll` changes to `np.array` or `array`

    def get(self, button: int) -> bool:
        """ Get button state """
        return self.buttons_pressed[button]

    def scroll(self) -> Tuple[float, float]:
        """ Get scrolling """
        return self.scroll

    def rel(self) -> Tuple[float, float]:
        """ Get relative mouse displacement """
        return (self.pos[0] - self.last_pos[0], self.pos[1] - self.last_pos[1])

    def pos(self) -> Tuple[float, float]:
        return self.pos

    def reset(self):
        """ Reset the instant states to normal before every update cycle """
        self.scroll = (0.0, 0.0)
        self.last_pos = self.pos
    
    # -- Private methods --
    # @inline
    def _motion(self, event: pygame.event.Event):
        # Update the mouse pos
        self.pos = (self.pos[0] + event.pos[0], self.pos[1] + event.pos[1])
        self.is_dragging = any(self.buttons_pressed)

    # @inline
    def _button(self, event: pygame.event.Event):
        """ Will extract the pressed button and toggle its value in `self.buttons_pressed`
            Using the `^= True` trick
        """
        btn_idx = event.button
        if btn_idx <= 3:
            self.buttons_pressed[btn_idx-1] ^= True

    # @inline
    def _scroll(self, event: pygame.event.Event):
        self.last_scroll = self.scroll
        self.scroll = (self.scroll[0] + event.x, self.scroll[1] + event.y)
