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

N_FOOD = 10
MIN_FOOD = N_FOOD * 0.5
MAX_FOOD = N_FOOD * 1.5
FOOD_TIMING = 20 # new food appears after FOOD_TIMING iterations
class World:

	def __init__(self, win, max_x, max_y):
		self.max_x = max_x
		self.max_y = max_y
		self.timer = 0
		# create food
		self.food = []
		while len(self.food) < N_FOOD:
			food_rnd_coord = [randint(2, max_y - 2), randint(2, max_x - 2)]
			if not(food_rnd_coord in self.food):
				self.food.append(food_rnd_coord)
				win.addch(food_rnd_coord[0], food_rnd_coord[1], '*', curses.color_pair(1))

	def update(self, win, snakes):
		self.timer += 1
		snakes_bodies = [i.body for i in snakes if i.is_dead == False]
		snakes_bodies = list(itertools.chain(*snakes_bodies))
		tmp_count = len(self.food) - len([i for i,x in enumerate(self.food) if x==[]])
		done = False
		if (tmp_count < MIN_FOOD or self.timer % FOOD_TIMING == 0) and tmp_count < MAX_FOOD:
			while not done:
				food_rnd_coord = [randint(2, self.max_y - 2), randint(2, self.max_x - 2)]
				if not(food_rnd_coord in self.food and food_rnd_coord in snakes_bodies):
					self.food.append(food_rnd_coord)
					done = True
					win.addch(food_rnd_coord[0], food_rnd_coord[1], '*', curses.color_pair(1))
					
