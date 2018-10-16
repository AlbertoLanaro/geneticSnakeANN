'''
Create the world with borders and food coordinates

World coordinates system

>  2
^  1
V  3
<  0

/  -----------------------------  \
|  00,01,02,03,04,05,06,07,08,09  |
|  10,11,12,13,14,15,16,17,18,19  |
|  .............................  |
|  .............................  |
|  .............................  |
|  .............................  |
|  90,91,92,93,94,95,96,97,98,99  |
\  -----------------------------  /





(0, 0)----- X - ------->        ^
  |           .                 |
  |           .                 2
  |						        UP
  |           .      <-- LEFT --*-- RIGHT ->
  | . . . . (y, x)              |
  Y                           DOWN
  |								0
  |                             V
  v

'''
import curses
from random import randint
import itertools
import debug
 '''
 Class just simulate snake until he die or it's stopped
 '''
N = 10

class Snake:
    def __init__(self, color):
        #graphics
		self.cube = pygame.Surface((SCALE, SCALE))
		self.cube.fill(color)
        self.color = color
        self.timer = 0
        self.size = 1
		#define head start
		self.body =  [[randint(1, N - 1), randint(1, N - 1)]]
		self.score = 0 # inital score value
		self.prev_dir = randint(0, 3)  # previous direction
		self.curr_dir = self.prev_dir # current direction
		self.is_dead = False # flag to indicate if the snake is dead
        self.createFood()
		self.brain = brain

    def createFood(self):
        self.food = [randint(2, N - 2), randint(2, N - 2)]
		# food must not be in the same position of the snake
        while(self.foodOnSnake() == True):
            self.food = [randint(2, N - 2), randint(2, N - 2)]

    def foodOnSnake(self):
        for i in self.body:
            if i == self.food:
                return True
        return False


'''
1)Update snake position knowed the direction
2)Check if it'dead -> return -1
3)Check if it ate some food -> return 1 and create new food
4)eventually delete the tail
5)draw the snake and the food
'''
	def update(self, field, direction):
        self.timer += 1
		self.body.insert(0, [self.body[0][0] + (direction == 2 and 1) +
            (direction == 0 and -1), self.body[0][1] +
            (direction == 3 and 1) + (direction == 1 and -1)])

        # check if snake hit himself or hit borders
        if self.body[0] in self.body[1:] or self.body[0][0] == -1 or
                        self.body[0][0] == self.N or
                        self.body[0][1] == -1 or self.body[0][1] == self.N:
            return -1
        # check if snake head is in some food coordinates
        if self.body[0] == self.food:
            # update score
            self.score += 1
            self.createFood()
            return 1
        else:
            # update snake's body
            last = self.body.pop()
            return 0
		self.show(field)
