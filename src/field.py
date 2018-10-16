import pygame
from colors import WHITE

class Field:
    SCALE = 10
    N = 40
    BORDERS = False
    def __init__(self):
        self.field = pygame.display.set_mode((Field.N * Field.SCALE, Field.N * Field.SCALE))
        self.field.fill(WHITE)
    
    def update(self):
        self.field.fill(WHITE)
        

        
