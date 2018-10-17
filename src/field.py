import pygame
from colors import WHITE

class Field:
    SCALE = 40
    N = 10
    BORDERS = False
    def __init__(self, gui=True):
        self.gui = gui
        if gui:
            self.field = pygame.display.set_mode((Field.N * Field.SCALE, Field.N * Field.SCALE))
            self.field.fill(WHITE)

    def update(self):
        if self.gui:
            self.field.fill(WHITE)
