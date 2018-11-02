import geneticSnake
import field
import colors
import pygame
import random
import conf
import numpy as np
import time
import scipy.stats as st

N = conf.N_CROSS

class Simulation:
    def __init__(self, input_type, n_snakes=1000, visible=False, timer = None):
        self.timer = timer
        # field of the current generation
        self.field = field.Field(visible)
        self.iteration = 0
        self.n_snakes = n_snakes
        self.death_counter = 0
        # list of snake created for the current simulation
        self.geneticSnakes = [geneticSnake.GeneticSnake(
            self.field, input_type, visible=visible) for _ in range(n_snakes)]

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

    '''
    Function that upgrate generation with a different distribution of parents
    It choose the parents with higher fitness with more prbability
    We   1)choose the N parents best parents of the simulation
         2) Create the vector of their fitnesses
         3) CumSum the fitnesses vector
         4) Create a random int from 0 to sum(fitnesses)
         5) Choose the snake which fitness is nearer ahead the random int
    '''
    def upgradeGenerationNotUniform(self):
        # sort for fitness
        self.sortSnakesForFitness()        
        max_fit = self.geneticSnakes[-1].fitness
        min_fit = self.geneticSnakes[0].fitness
        # store snake's DNA
        if max_fit > conf.MAX_FITNESS:
            self.geneticSnakes[-1].brain.DNAsave(max_fit)
            conf.MAX_FITNESS = max_fit
        # Creating the fitnesses cumulative density function
        fit_array_cdf = []
        for i in self.geneticSnakes[self.n_snakes - conf.N_CROSS:]:
            fit_array_cdf.append(i.fitness**2)
        fit_array_cdf = np.cumsum(np.array(fit_array_cdf))
        fit = []
        fit_top = []
        parents_fitness = 0
        for i in self.geneticSnakes[: self.n_snakes - conf.N_CROSS]:
            fit.append(i.fitness)
        # top-performing snakes used for reproduction
        for i in self.geneticSnakes[self.n_snakes - conf.N_CROSS:]:
            fit_top.append(i.fitness)
        
        # generation statistics
        mean_fit = np.mean(fit)
        # confidence interval (95%)
        mean_top_fit = np.mean(fit_top)
        top_fit_CI = st.t.interval(0.95, len(fit_top)-1, loc=mean_top_fit, scale=st.sem(fit_top))

        # DNA mutation probability
        p_mutation = min(conf.MUTATION_RATE, conf.MUTATION_RATE / (mean_top_fit))
        
        # Taking the (n_snakes - N_SNAKE_SURVIVING) worst snakes and 
        # substitute them with other reproduced from the best snakes
        # 1. new snakes (with probable mutation)
        for i in self.geneticSnakes[:self.n_snakes - conf.N_SNAKE_SURVIVING]:
            rnd = random.random()
            # do not mutate DNA
            if rnd > conf.MUTATION_PROBABILITY:
                random_index0 = random_sampling(fit_array_cdf)
                random_index1 = random_sampling(fit_array_cdf)
                parents_fitness += self.geneticSnakes[random_index1].fitness
                i.brain.crossDNA(self.geneticSnakes[random_index0].brain, self.geneticSnakes[random_index1].brain)
            # possibly mutate DNA
            else: 
                random_index0 = random_sampling(fit_array_cdf)
                random_index1 = random_sampling(fit_array_cdf)
                value = self.geneticSnakes[random_index1].fitness
                parents_fitness += value
                i.brain.crossDNAAndMutate(self.geneticSnakes[random_index0].brain, self.geneticSnakes[random_index1].brain, p_mutation)
            i.clear()
        # 2. snakes that survive to the next generation
        for i in self.geneticSnakes[self.n_snakes - conf.N_SNAKE_SURVIVING:]:
            i.clear()

        return mean_fit, mean_top_fit, top_fit_CI, p_mutation, parents_fitness/(self.n_snakes- conf.N_SNAKE_SURVIVING), max_fit, min_fit, self.iteration
        
    '''
    Shows the snake with higher fitness
    '''
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
        if self.timer:
            time.sleep(self.timer)
'''
Utility function 
given a sorted array it gives a random index. 
The distrubution is not uniform: it's proportional to the distance from the previus element
'''
def random_sampling(fit_array):
    rnd = random.randint(1, fit_array[-1])
    
    i = 1
    while True:
        if i == len(fit_array):
            return -(i)
        if rnd > fit_array[-i-1]:
            return -i
        i += 1
