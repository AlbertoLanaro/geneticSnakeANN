import geneticSnake
import field
import colors
import pygame
import random
import conf

TIMER = 100  #  [ms]
class Simulation:
    def __init__(self, n_snakes=1000, visible=False):
        # field of the current generation
        self.field = field.Field(visible)
        if visible:
            # set simulation update timer
            pygame.time.set_timer(1, TIMER)
        self.n_snakes = n_snakes
        self.death_counter = 0
        # list of snake created for the current simulation
        self.geneticSnakes = [geneticSnake.GeneticSnake(self.field, visible = visible) for _ in range(n_snakes)]

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
            #print("dead snake: ", self.death_counter)
            
        self.death_counter = 0
    '''
    Sort the list of geneticSnake from higher to lower fitness
    '''
    def sortSnakesForFitness(self):
        self.geneticSnakes.sort(key=lambda x: x.fitness)

    # This function improves the natural selection
    # We take the second half of the simulation sorted by fitness
    # and change their DNA with the DNA of the better snakes
    def upgradeGeneration(self, N = 10 ):
        # sort for fitness
        self.sortSnakesForFitness()
        #topfitness = self.geneticSnakes[-1].fitness
        # Taking the first half and then reproduce them 
        fit = 0
        rnd = random.random()
        for i in self.geneticSnakes:
            fit += i.fitness
        for i in self.geneticSnakes[:self.n_snakes- N ]:
            if rnd > conf.Conf.MUTATION_PROBABILITY:
                i.brain.crossDNA(self.geneticSnakes[random.randint(
                self.n_snakes-(N),self.n_snakes -1)].brain, self.geneticSnakes[random.randint(self.n_snakes-(N),self.n_snakes -1)].brain)
            else:
                i.brain.crossDNAAndMutate(self.geneticSnakes[random.randint(
                    self.n_snakes-(N), self.n_snakes - 1)].brain, self.geneticSnakes[random.randint(self.n_snakes-(N), self.n_snakes - 1)].brain)
            i.clear()
        for i in self.geneticSnakes[self.n_snakes-(N):]:
            i.clear()
            
        return fit/self.n_snakes

    def showBestN(self, N=10): 
        self.field.view()
        self.sortSnakesForFitness()
        for i in self.geneticSnakes[:self.n_snakes - N]:
            i.snake.hide()
        for i in self.geneticSnakes[self.n_snakes - N :]:
            i.snake.view()
        #i could create some pointer to the object that I will not longer show

    def updateBestN(self, N=10):
        self.sortSnakesForFitness()
        for i in self.geneticSnakes[:self.n_snakes - N]:
            i.snake.hide()
        for i in self.geneticSnakes[self.n_snakes - N:]:
            i.snake.view()

    def stopShowing(self):
        self.field.hide()
        for i in self.geneticSnakes:
            i.snake.hide()

    '''
    Update geneticSnakes and field
    '''
    def update(self):
        self.field.update()
        for i in self.geneticSnakes:
            i.update()
            # update counter if a snake is dead
            if i.is_dead:
                self.death_counter += 1
        if self.field.visible:
            pygame.display.flip()
