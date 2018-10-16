import snake
import pygame
from pygame.locals import *
from random import randint
import os, sys
import curses
from random import randint
import itertools
import colors
import field

WHITE = (255,255,255)
RED = (255,0,0)
N = field.Field.N
SCALE = field.Field.SCALE

def main():
    #creo campo
    sn = snake.Snake()
    field = pygame.display.set_mode((N * SCALE, N * SCALE))
    
    field.fill(WHITE)
    clock = pygame.time.Clock()
    pygame.time.set_timer(1, 100)
    direction = 1
    while True:
        e = pygame.event.wait()
        if e.type == QUIT:
            pygame.quit()
        elif e.type == MOUSEBUTTONDOWN:
            if e.button == 3:
                direction = (direction+1) % 4
                print("dx")
            elif e.button == 1:
                print("sx")
                direction = (direction+3) % 4
        field.fill((255, 255, 255))
        if sn.update(field, direction) == -1:
            print("DEAD")
            return False

        pygame.display.flip()

main()
