from soulsrpg.listener import MouseListener
from pygame.event import Event
from pygame.locals import *

def test_mouselistener():
    events = [
        Event(MOUSEMOTION, { "pos" : (0.0, 0.0) }),
        Event(MOUSEMOTION, { "pos" : (0.0, 1.0) }),
        Event(MOUSEMOTION, { "pos" : (1.0, 0.0) }),
        Event(MOUSEMOTION, { "pos" : (1.0, 1.0) }) 
    ]
    mouse = MouseListener()
    for e in events:
        mouse.retrieve(e)
        print(mouse)

    assert mouse.rel() == (2.0, 2.0)

    mouse.reset()
    assert mouse.rel() == (0.0, 0.0)
    
