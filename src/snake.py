#-*- coding: utf-8 -*-
'''
Create the world with borders and food coordinates

World coordinates system

^  0
>  1
V  2
<  3

/  -----------------------------  \
|  00,01,02,03,04,05,06,07,08,09  |
|  10,11,12,13,14,15,16,17,18,19  |
|  .............................  |
|  .............................  |
|  .............................  |
|  .............................  |
|  90,91,92,93,94,95,96,97,98,99  |
\  -----------------------------  /





(0, 0)----- X - ------->         ^
  |           .                  |
  |           .                  0
  |			  .			         UP
  |           .                  |
  |           .      <-- 3 LEFT -*- RIGHT 1->
  | . . . . (x, y)               |
  Y                            DOWN
  |								 2
  |                              V
  v

'''

import pygame

from random import randint
import field
import colors

class Snake:
    def __init__(self):
        #graphics
        self.cube = pygame.Surface((field.Field.SCALE, field.Field.SCALE))
        self.cube.fill(colors.random())
        self.timer = 0
        self.size = 1
		#define head start
        self.body =  [[randint(1, field.Field.N - 1), randint(1, field.Field.N - 1)]]
        self.score = 0 # inital score value
        self.curr_dir = randint(0, 3)  # previous direction
        self.is_dead = False # flag to indicate if the snake is dead
        self.createFood()

    def createFood(self):
        self.food = [randint(2, field.Field.N - 2), randint(2, field.Field.N - 2)]
		# food must not be in the same position of the snake
        while(self.foodOnSnake() == True):
            self.food = [randint(2, field.Field.N - 2), randint(2, field.Field.N - 2)]

    def foodOnSnake(self):
        for i in self.body:
            if i == self.food:
                return True
        return False

    def getCurrDir(self):
        return self.curr_dir

    def getFoodPosition(self):
        return self.food

    def getBodyPosition(self):
        return self.body


    '''
    1)Update snake position knowed the direction
    2)Check if it'dead -> return -1
    3)Check if it ate some food -> return 1 and create new food
    4)eventually delete the tail
    5)draw the snake and the food
    '''
    def update(self, fld, direction):
        self.timer += 1
        self.body.insert(0, [self.body[0][0] + (direction == 1 and 1) +
            (direction == 3 and -1), self.body[0][1] +
            (direction == 2 and 1) + (direction == 0 and -1)])

        # check if snake hit borders
        if self.body[0] in self.body[1:]:
            return -1
        elif self.body[0][0] == -1 or self.body[0][0] == field.Field.N or self.body[0][1] == -1 or self.body[0][1] == field.Field.N:
            if field.Field.BORDERS == True:
                return -1
            else:
                # snake appears on the other side of the screen
                if direction == 0:
                    self.body.pop(0)
                    self.body.insert(0, [self.body[0][0], field.Field.N - 1])
                if direction == 1:
                    self.body.pop(0)
                    self.body.insert(0, [0 , self.body[0][1]])
                if direction == 2:
                    self.body.pop(0)
                    self.body.insert(0, [self.body[0][0], 0])
                if direction == 3:
                    self.body.pop(0)
                    self.body.insert(0, [field.Field.N - 1, self.body[0][1]])

        # check if snake head is in some food coordinates
        if self.body[0] == self.food:
            # update score
            self.score += 1
            self.createFood()
            ret = 1
        else:
            # update snake's body
            last = self.body.pop()
            ret = 0
        if fld.visible:
            self.show(fld.field)
            
        return ret

    def show(self, fld):
        for bit in self.body:
            fld.blit(self.cube, (bit[0] * field.Field.SCALE, bit[1] * field.Field.SCALE))
        fld.blit(self.cube, (self.food[0] * field.Field.SCALE, self.food[1] * field.Field.SCALE))
