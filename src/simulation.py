import geneticSnake
import field
import colors
import pygame
import random
import conf
import numpy as np

N = conf.N_CROSS

class Simulation:
    def __init__(self, n_snakes=1000, visible=False):
        # field of the current generation
        self.field = field.Field(visible)
        self.iteration = 0
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
    Simulation end is triggered by the death of one or more snakes
    '''
    def simulateUntilDeath(self, n_death=1):
        self.iteration = 0
        while self.death_counter < n_death:
            self.update()
            #print("dead snake: ", self.death_counter)
            
        self.death_counter = 0
    '''
    Simulation end is triggered by the death of one or more snakes
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
    Sort the list of geneticSnake from lower to higher fitness
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
        if max_fit > conf.MAX_FITNESS:
            self.geneticSnakes[-1].brain.DNAsave(max_fit)
            conf.MAX_FITNESS = max_fit
        min_fit = self.geneticSnakes[0].fitness
        #topfitness = self.geneticSnakes[-1].fitness
        # Taking the first half and then reproduce them 
        fit = 0
        fit_top = 0 
        for i in self.geneticSnakes[:self.n_snakes - conf.N_SNAKE_SURVIVING]:
            fit += i.fitness
            rnd = random.random()
            if rnd > conf.MUTATION_PROBABILITY:
                i.brain.crossDNA(self.geneticSnakes[random.randint(
                    self.n_snakes - conf.N_CROSS, self.n_snakes - 1)].brain, self.geneticSnakes[random.randint(self.n_snakes - conf.N_CROSS, self.n_snakes - 1)].brain)
            else:
                i.brain.crossDNAAndMutate(self.geneticSnakes[random.randint(
                    self.n_snakes- conf.N_CROSS, self.n_snakes - 1)].brain, self.geneticSnakes[random.randint(self.n_snakes- conf.N_CROSS, self.n_snakes - 1)].brain)
            i.clear()
        for i in self.geneticSnakes[-conf.N_SNAKE_SURVIVING : self.n_snakes-conf.N_CROSS]:
            fit += i.fitness
            i.clear()
        for i in self.geneticSnakes[self.n_snakes - conf.N_CROSS:]:
            fit_top += i.fitness
            i.clear()
        return (fit + fit_top)/self.n_snakes, (fit_top/N), max_fit, min_fit, self.iteration

    '''
    Function that upgrate generation with a different distribution of parents
    It choose the parents with higher fitness with more prbability
    We   1)choose the N parents best parents of the simulation
         2) Create the vector of their ftinesses
         3) CumSum the fitnesses vector
         4) Create a random int from 0 to sum(fitnesses)
         5) Choose the snake which fitness is nearer ahead the random int
    '''
    def upgradeGenerationNotUniform(self):
        # sort for fitness
        self.sortSnakesForFitness()        
        max_fit = self.geneticSnakes[-1].fitness
        if max_fit > conf.MAX_FITNESS:
            self.geneticSnakes[-1].brain.DNAsave(max_fit)
            conf.MAX_FITNESS = max_fit
        min_fit = self.geneticSnakes[0].fitness
        # Creating the fitnesses vector
        fit_array = []
        for i in self.geneticSnakes[self.n_snakes - conf.N_CROSS:]:
            fit_array.append(i.fitness)
        fit_array = np.cumsum(np.array(fit_array))
        # Taking the (n_snakes - N_SNAKE_SURVIVING) worst snakes and 
        # substitute them with other reproduced from the better snakes
        fit = 0
        average_distribution = 0
        fit_top = 0
        # 1. new snakes (with mutation)
        for i in self.geneticSnakes[:self.n_snakes - conf.N_SNAKE_SURVIVING]:
            fit += i.fitness
            rnd = random.random()
            if rnd > conf.MUTATION_PROBABILITY:
                random_index0 = random_array(fit_array)
                random_index1 = random_array(fit_array)
                average_distribution += self.geneticSnakes[random_index1].fitness
                i.brain.crossDNA(
                    self.geneticSnakes[random_index0].brain, self.geneticSnakes[random_index1].brain)
            else:
                random_index0 = random_array(fit_array)
                random_index1 = random_array(fit_array)
                value = self.geneticSnakes[random_index1].fitness
                average_distribution += value
                i.brain.crossDNAAndMutate(
                    self.geneticSnakes[random_index0].brain, self.geneticSnakes[random_index1].brain)
            i.clear()
        # 2. snakes that survive to the next generation
        # 2.1 snakes that are not used for crossover
        for i in self.geneticSnakes[-conf.N_SNAKE_SURVIVING: self.n_snakes-conf.N_CROSS]:
            fit += i.fitness
            i.clear()
        # 2.2 snakes with highest fitness that are used for crossover 
        for i in self.geneticSnakes[self.n_snakes - conf.N_CROSS:]:
            fit_top += i.fitness
            i.clear()
        return (fit + fit_top)/self.n_snakes, (fit_top/N), (average_distribution/conf.N_SNAKE_SURVIVING), max_fit, min_fit, self.iteration

    def showBestN(self, N=10): 
        self.field.view()
        self.sortSnakesForFitness()
        for i in self.geneticSnakes[:self.n_snakes - N]:
            i.snake.hide()
        for i in self.geneticSnakes[self.n_snakes - N :]:
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
'''
Utility function 
given a sorted array it gives a random index. 
The distrubution is not uniform: it's proportional to the distance from the previus element
'''
def random_array(fit_array):
    rnd = random.randint(1, fit_array[-1])
    i = 1
    while True:
        if i == len(fit_array):
            return -(i)
        if rnd > fit_array[-i-1]:
            return -i
        i += 1
