import snake
import brain
import field
import colors
import pygame

TIMER = 100  #  [ms]
class Simulation:
    def __init__(self, n_snakes=5):
        # set simulation update timer
        pygame.time.set_timer(1, TIMER)
        # list of snake created for the current simulation
        self.snakes = [snake.Snake(colors.random()) for _ in range(n_snakes)]
        # create snakes's brain
        self.brains = [brain.Brain(field.Field.N ** 2) for _ in range(n_snakes)]
        # field of the current generation
        self.field = field.Field()

    def update(self):
        # . . . 
        # update entire screen -> pygame.display.update() could update portion of the screen
        pygame.display.flip()

        
        
        
