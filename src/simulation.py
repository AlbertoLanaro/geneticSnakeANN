import geneticSnake
import field
import colors
import pygame

TIMER = 100  #  [ms]
class Simulation:
    def __init__(self, n_snakes=5, visible = False):
        # field of the current generation
        self.field = field.Field()
        self.n_snakes = n_snakes
        self.visible = visible
        if self.field.gui:
            # set simulation update timer
            pygame.time.set_timer(1, TIMER)
        # list of snake created for the current simulation
        self.geneticSnakes = [geneticSnake.GeneticSnake(self.field) for _ in range(n_snakes)]

    def simulateGeneration(self, turn = 100):
        for i in range(turn):
            if self.visible:
                self.field.update()
            for i in self.geneticSnakes:
                i.update()
            if self.visible:
                pygame.display.flip()
        #now it should be completed:

    def sortSnakesForFitness(self):
        # TODO sort -> geneticSnakes(key=fitness)

    self reproduce(self):
        # sort for fitness
        self.sortSnakesForFitness()
        # Taking the first half and then reproduce them 
        for i in self.geneticSnakes[self.n_snakes/2:]:
            i.brain.crossDNAAndMutate(self.geneticSnakes[random.randint(
                0, self.n_snakes/2)].brain, self.geneticSnakes[random.randint(0, self.n_snakes/2)].brain)

    self showBestN(self, N = 10): 
        self.field.gui = True
        self.visible = True
        self.sortSnakesForFitness()
        for i in self.geneticSnakes:
            i.changeVisibility(False)
        for i in self.geneticSnakes[self.n_snakes - N :]:
            i.changeVisibility(True)
        #i could create some pointer to the object that I will not longer show

    def changebestN(self, N = 10)
        self.sortSnakesForFitness()
        for i in self.geneticSnakes:
            i.changeVisibility(False)
        for i in self.geneticSnakes[self.n_snakes - N:]:
            i.changeVisibility(True)


    def stopShowing(self):
        self.visible = False
        self.field.gui = False
        for i in self.geneticSnakes:
            i.changeVisibility(False)

    def update(self):

        # . . . 
        # update entire screen -> pygame.display.update() could update portion of the screen
        if self.field.gui:
            pygame.display.flip()

        
        
        
