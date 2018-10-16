'''
Create the world with borders and food coordinates

World coordinates system

(0, 0)----- X - ------->        ^
  |           .                 |
  |           .                 |
  |						        UP
  |           .      <-- LEFT --*-- RIGHT ->
  | . . . . (y, x)              |
  Y                           DOWN
  |								|
  |                             V
  v

'''
import curses
from random import randint
import itertools
import debug

HEALTH_BONUS = 6 # initial health bonus

# ANN params
# what snake sees: 1) simple: 4, 2) box of view: h * w + nromalized min_food_distance + normalized snake head pos
input_len = 5 * 5 + 1 + 2
n_hidden_units = 5 #4 # hidden layer neurons
n_class = 3 # output classes -> three possible direction
#dimention of the field
N = 10

class Snake:
    def __init__(self, Color, DNA):
        #graphics
		self.cube = pygame.Surface((SCALE, SCALE))
		self.cube.fill(color)
        self.color = color
        self.N = N
        self.timer = 0
        self.size = 1
		#define head start
		self.body =  [[randint(1, N - 2), randint(1, N - 2)]]
		self.score = 0 # inital score value
		self.health = HEALTH_BONUS # initla health value
		self.fitness = self.health # initial fitness value
		self.prev_dir = randint(0, 3)  # previous direction
		self.curr_dir = self.prev_dir # current direction
		self.is_dead = False # flag to indicate if the snake is dead
        self.createFood()
		if DNA == None: #  create a snake with a 'random brain'
			self.DNA = DNA
            # initialize brain params
			self.syn0 = 2 * np.random.random(input_len * n_hidden_units) - 1
			self.syn1 = 2 * np.random.random(n_hidden_units * n_class) - 1
			self.DNA = np.hstack([self.syn0, self.syn1])
		else: #create a snake from a given DNA
			self.DNA = DNA

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

	def update(self, field):
        self.timer += 1
		if not(self.is_dead):
			ret = True
			# get next direction
			self.think(world, win)
			#win.addstr(0, 10, ' Fitness: ' + str(round(self.fitness, 3)) + ' [Health: ' + str(round(self.health, 3)) + ' Score: ' + str(self.score) + '] ')

			if DEBUG:
				debug.f_debug.write("min food dist " + str(curr_food_distance) + "\n")
			# if curr_food_distance >= self.last_food_distance:
			# 	self.health -= self.health * 0.1 # update
			# 	debug.f_debug.write("stepped away from food!\n")

			self.health -= self.health * 0.1 # update

			if self.health < 1e-2 or self.fitness < 1e-2:
				self.is_dead = True

			self.body.insert(0, [self.body[0][0] + (self.curr_dir == 2 and 1) +
                (self.curr_dir == 0 and -1), self.body[0][1] +
                (self.curr_dir == 3 and -1) + (self.curr_dir == 1 and 1)])

            # check if snake hit himself or hit borders
            if self.body[0] in self.body[1:] or self.body[0][0] == 0 or
                            self.body[0][0] == self.N - 1 or
                            self.body[0][1] == 0 or self.body[0][1] == self.N - 1:
                self.is_dead = True
            # check if snake head is in some food coordinates
            if self.body[0] == self.food:
                # update score
                self.score += 1
                self.health += (HEALTH_BONUS * 0.5)
                # check if saturated health
                if self.health > 3 * HEALTH_BONUS: # max possibile health is reached!
                    self.health = 3 * HEALTH_BONUS
                self.createFood()
            else:
                # update snake's body
                last = self.body.pop()
			self.show(field)
		else:
			self.die()
		if DEBUG:
			debug.f_debug.write("snake params:\n")
			debug.f_debug.write("\tdead: " + str(self.is_dead) + "\n")
			debug.f_debug.write("\tlength: " + str(len(self.body)) + "\n")
			debug.f_debug.write("\thealth: " + str(self.health) + "\n")
			debug.f_debug.write("\tfitness: " + str(self.fitness) + "\n")
		return ret



'''class that implements a single simulation.
It has its wall, his food and his snake
'''
max_x = N
max_x = N
class World:
    def __init__(self, DNA, color):
        self.color = color
		self.max_x = max_x
		self.max_y = max_y
		self.timer = 0
        if DNA == None:
            self.snake = snake.Snake(self, color)
        else:
            self.snake = snake.Snake(self,DNA = DNA, color)
        #create food
        self.createFood()

    def createFood(self):
        self.food = [randint(2, max_y - 2), randint(2, max_x - 2)]
		# food must not be in the same position of the snake
        while(self.foodOnSnake() == True):
            self.food = [randint(2, max_y - 2), randint(2, max_x - 2)]

    def foodOnSnake(self):
        for i in self.snake.body:
            if i == self.food:
                return True
        return False

	def update(self, field):
		self.timer += 1
        if snake.update() == False:
            self.die()
