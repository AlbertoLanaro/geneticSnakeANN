import geneticSnake
import field
import colors
import pygame
import random
import conf

N = conf.N_CROSS
TIMER = 1  #  [ms]
class Simulation:
    def __init__(self, n_snakes=1000, visible=False):
        # field of the current generation
        self.field = field.Field(visible)
        self.iteration = 0
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
    def simulateGeneration(self, turn=50):
        self.iteration = 0
        for _ in range(turn):
            self.update()
            

    '''
    Simulation duration is triggered by the death of one or more snakes
    '''
    def simulateUntilDeath(self, n_death=1):
        self.iteration = 0
        while self.death_counter < n_death:
            self.update()
            #print("dead snake: ", self.death_counter)
            
        self.death_counter = 0
    '''
    Simulation duration is triggered by the death of one or more snakes
    or timer ending
    '''
    def simulateUntilDeathOrTimer(self, n_death=1, N = 100):
        self.iteration = 0
        while self.death_counter < n_death and self.iteration < N :
            self.update()
            self.iteration+=1
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
    def upgradeGeneration(self ):
        # sort for fitness
        self.sortSnakesForFitness()
        max_fit = self.geneticSnakes[-1].fitness
        if max_fit >14:
            self.geneticSnakes[-1].brain.DNAsave()

        min_fit = self.geneticSnakes[0].fitness
        #topfitness = self.geneticSnakes[-1].fitness
        # Taking the first half and then reproduce them 
        fit = 0
        fit_top = 0 
        for i in self.geneticSnakes[:self.n_snakes - (conf.N_SNAKE_SURVIVING + 1)]:
            fit += i.fitness
            rnd = random.random()
            if rnd > conf.MUTATION_PROBABILITY:
                i.brain.crossDNA(self.geneticSnakes[random.randint(
                    self.n_snakes-(conf.N_CROSS), self.n_snakes - 1)].brain, self.geneticSnakes[random.randint(self.n_snakes-(conf.N_CROSS), self.n_snakes - 1)].brain)
            else:
                i.brain.crossDNAAndMutate(self.geneticSnakes[random.randint(
                    self.n_snakes-(conf.N_CROSS), self.n_snakes - 1)].brain, self.geneticSnakes[random.randint(self.n_snakes-(conf.N_CROSS), self.n_snakes - 1)].brain)
            i.clear()
        for i in self.geneticSnakes[self.n_snakes - self.n_snakes-conf.N_SNAKE_SURVIVING : self.n_snakes-conf.N_CROSS -1]:
            fit += i.fitness
        for i in self.geneticSnakes[self.n_snakes-conf.N_CROSS:]:
            fit_top += i.fitness
            i.clear()
        return (fit + fit_top)/self.n_snakes, (fit_top/N), max_fit, min_fit, self.iteration

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
        self.death_counter = 0
        self.iteration += 1
        for i in self.geneticSnakes:
            i.update()
            # update counter if a snake is dead
            if i.is_dead:
                self.death_counter += 1
        if self.field.visible:
            pygame.display.flip()
