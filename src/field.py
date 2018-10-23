import pygame
from colors import WHITE
import conf

class Field:
    SCALE = 30
    TIMER = 10  #  [ms]
    N = conf.BORDER
    BORDERS = conf.BORDER_BOOL
    def __init__(self, visible=False):
        self.visible = visible
        if visible:
            # set simulation update timer
            pygame.time.set_timer(1, self.TIMER)
        self.field = pygame.display.set_mode((Field.N * Field.SCALE, Field.N * Field.SCALE))
        self.field.fill(WHITE)

    def update(self):
        if self.visible:
            _ = pygame.event.wait()
            self.field.fill(WHITE)

    def view(self):
        self.visible = True
    
    def hide(self):
        self.visible = False
