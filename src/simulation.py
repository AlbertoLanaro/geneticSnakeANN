import geneticSnake
import field
import colors
import pygame
import random

TIMER = 100  #  [ms]
class Simulation:
    def __init__(self, n_snakes=1000, visible=False):
        # field of the current generation
        self.field = field.Field()
        self.n_snakes = n_snakes
        self.death_counter = 0
        self.visible = visible
        if self.field.gui:
            # set simulation update timer
            pygame.time.set_timer(1, TIMER)
        # list of snake created for the current simulation
        self.geneticSnakes = [geneticSnake.GeneticSnake(self.field) for _ in range(n_snakes)]

    '''
    Simulation duration is set to "turn" iteration
    '''
    def simulateGeneration(self, turn=100):
        for _ in range(turn):
            self.update()

    '''
    Simulation duration is triggered by the death of one or more snakes
    '''
    def simulateUntilDeath(self, n_death=1):
        while self.death_counter < n_death:
            self.update()
            
    '''
    Sort the list of geneticSnake from higher to lower fitness
    '''
    def sortSnakesForFitness(self):
        self.geneticSnakes.sort(key=lambda x: x.fitness, reverse=True)

    def reproduce(self):
        # sort for fitness
        self.sortSnakesForFitness()
        # Taking the first half and then reproduce them 
        for i in self.geneticSnakes[self.n_snakes/2:]:
            i.brain.crossDNAAndMutate(self.geneticSnakes[random.randint(
                0, self.n_snakes/2)].brain, self.geneticSnakes[random.randint(0, self.n_snakes/2)].brain)

    def showBestN(self, N=10): 
        self.field.gui = True
        self.visible = True
        self.sortSnakesForFitness()
        for i in self.geneticSnakes:
            i.changeVisibility(False)
        for i in self.geneticSnakes[self.n_snakes - N :]:
            i.changeVisibility(True)
        #i could create some pointer to the object that I will not longer show

    def changebestN(self, N=10):
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

    '''
    Update geneticSnakes and field
    '''
    def update(self):
        if self.visible:
            self.field.update()
        for i in self.geneticSnakes:
            i.update()
            # update counter if a snake is dead
            if i.is_dead:
                self.death_counter += 1
        if self.visible:
            pygame.display.flip()