import pygame
from pygame.locals import *
from random import randint
import os, sys
import world


'''
Class that draw the words with their color
'''
colors = [(255,0,0)]
WHITE = (255,255,255)
SCALE = 10
N = 8

'''
This class implements the simulation of a generation given a vector of DNA.
It represents the field that we view and simulate each snake. It could be started and
ended by the "god" class.
The API should improove also function for obtaining the fitness/DNA/ecc.. of the simulation
'''
class Simulation:
    #DNA array should be filled with none if it's just random
    def __init__(DNAarray):
        count = 0
        self.aliveWorld = []
        for i in DNAarray:
            self.aliveWorld.append(world.world(i,colors[count%len(colors)]))
            count = count + 1
        #create the white N*N field
        self.alive = count
        self.dead = 0
        self.deadWorld = []
        self.field = pygame.display.set_mode((N * SCALE, N * SCALE))

    def updateWorld(self):
        self.field.fill(WHITE)
        for i in self.aliveWorld:
            if i.update(self.field) == 0:#the snake is is dead
                #remove from active simulations and append to dead simulation
                self.alive = self.alive -1
                self.dead = self.dead + 1
                self.deadWorld.append(i)
                self.aliveWorld.pop(i)
                if self.alive == 0:
                    self.end()


class displaySingleSimulation:
    def __init__(world, color):
        self.world = world
        self.color = color
        #create the cube object with the color of the snake
        self.cube = pygame.Surface((10, 10))
        self.cube.fill(color)

    '''
    The idea of this function is to update the display where the simulation
    is showed. Whe should draw just a colored cube for the new head position and
    eventually remove the tail
    '''
    def updateSingleSiumation(self)
