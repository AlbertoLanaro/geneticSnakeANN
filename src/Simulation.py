import geneticSnake
import field
import colors
import pygame

TIMER = 100  #  [ms]
class Simulation:
    def __init__(self, n_snakes=5):
        # field of the current generation
        self.field = field.Field()
        if self.field.gui:
            # set simulation update timer
            pygame.time.set_timer(1, TIMER)
        # list of snake created for the current simulation
        self.geneticSnakes = [geneticSnake.GeneticSnake(self.field) for _ in range(n_snakes)]

    def update(self):
        # . . . 
        # update entire screen -> pygame.display.update() could update portion of the screen
        if self.field.gui:
            pygame.display.flip()

        
        
        
