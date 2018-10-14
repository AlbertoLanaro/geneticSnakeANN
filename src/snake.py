'''

Create a snake with a random head position with a length of 1 blocks

Snake's possible directions:
	- 0: UP
	- 1: RIGHT
	- 2: DOWN
	- 3: LEFT

'''

from random import randint
from activation_functions import sigmoid, softmax, relu
import curses
import numpy as np
from time import time
import os
import debug

HEALTH_BONUS = 6 # initial health bonus

# ANN params
# what snake sees: 1) simple: 4, 2) box of view: h * w + min_food_distance
input_len = 5 * 5 + 1
n_hidden_units = 5 #4 # hidden layer neurons
n_class = 3 # output classes -> three possible direction

# total number of ANN entries: input_len * n_hidden_units + n_hidden_units * n_class

class Snake:
	def __init__(self, world, win, from_DNA=False, DNA=None):
		self.skin_color = randint(0, 2) # TODO 
		self.size = 1 # inital snake size
		body_done = False # position the snake in the world + check if position is correct 
		while not(body_done):
			body_tmp = [[randint(1, world.max_y - 2), randint(1, world.max_x - 2)]] # initialize the head of the snake
			if not(body_tmp in world.food):
				body_done = True
		self.body = body_tmp
		self.score = 0 # inital score value
		self.health = HEALTH_BONUS # initla health value
		self.fitness = self.score / 2 + self.health # initial fitness value
		self.prev_dir = None # previous direction
		self.curr_dir = randint(0, 3) # current direction
		self.prev_dir = randint(0, 3)  # previous direction
		self.curr_dir = self.prev_dir # current direction
		self.is_dead = False # flag to indicate if the snake is dead
		if from_DNA: # create a snake from a given DNA
			self.DNA = DNA
		else: # create a snake with a 'random brain'
			# initialize brain params
			self.syn0 = 2 * np.random.random(input_len * n_hidden_units) - 1 
			self.syn1 = 2 * np.random.random(n_hidden_units * n_class) - 1
			self.DNA = np.hstack([self.syn0, self.syn1])

	def update(self, world, win):
		if not(self.is_dead):
			# get next direction
			self.think(world, win) 
			#win.addstr(0, 10, ' Fitness: ' + str(round(self.fitness, 3)) + ' [Health: ' + str(round(self.health, 3)) + ' Score: ' + str(self.score) + '] ')
			# reduce health
			self.health -= self.health * 0.2 # update 
			if self.health < 1e-2:
				self.is_dead = True
			# update snake head position
			self.body.insert(0, [self.body[0][0] + (self.curr_dir == 2 and 1) + (self.curr_dir == 0 and -1), self.body[0][1] + (self.curr_dir == 3 and -1) + (self.curr_dir == 1 and 1)])
			# check if snake hit himself or hit borders
			if self.body[0] in self.body[1:] or self.body[0][0] == 0 or self.body[0][0] == world.max_y - 1 or self.body[0][1] == 0 or self.body[0][1] == world.max_x - 1: 
				self.is_dead = True
			# check if snake head is in some food coordinates
			if self.body[0] in world.food: 
				# detect the food index
				food_indx = [i for i, x in enumerate(world.food) if x == self.body[0]] 
				# delete eaten food
				food_coord = world.food[food_indx[0]]
				win.addch(food_coord[0], food_coord[1], ' ') 
				world.food[food_indx[0]] = []
				# update score
				self.score += 1
				self.health += (HEALTH_BONUS * 0.5)
				# check if saturated health
				if self.health > 3 * HEALTH_BONUS: # max possibile health is reached!
					self.health = 3 * HEALTH_BONUS
			else: 
				# update snake's body
				last = self.body.pop()
				win.addch(last[0], last[1], ' ')
			# update fitness
			self.fitness = self.score / 2 + self.health
			win.addch(self.body[0][0], self.body[0][1], 's', curses.color_pair(self.skin_color))
		else: # snake is dead or no health
			self.remove(win)
			#win.border(0)

		debug.f_debug.write("snake params:\n")
		debug.f_debug.write("\tlength: " + str(len(self.body)) + "\n")
		debug.f_debug.write("\thealth: " + str(self.health) + "\n")
		debug.f_debug.write("\tfitness: " + str(self.fitness) + "\n")

	# remove dead snake from the window
	def remove(self, win):
		for i in self.body:
			win.addch(i[0], i[1], ' ')
		self.body = []
		self.fitness = 0

	def think(self, world, win):

		debug.f_debug.write("head at: " + str(self.body[0]) + "\n")
		debug.f_debug.write("initial dir: " + str(self.curr_dir) + "\n")

		ANN_inputs, next_possible_dir_list = self.get_ANN_inputs(world, win)

		debug.f_debug.write("ANN_inputs: " + str(ANN_inputs) + "\n")

		# update self.curr_dir
		self.predict(ANN_inputs, next_possible_dir_list, win)

	def predict(self, X, next_possible_dir_list , win):
		# get the hidden layer of the ANN
		syn0_r = self.DNA[:input_len * n_hidden_units].reshape([input_len, n_hidden_units])
		syn1_r = self.DNA[input_len * n_hidden_units:].reshape([n_hidden_units, n_class])

		# compute ANN output for the three possible directions
		output = []
		for tmp_input in X:
			#debug.f_debug.write("tmp_input: " + str(tmp_input) + "\n")
			l1 = sigmoid( np.dot(tmp_input, syn0_r) )
			l2 = sigmoid( np.dot(l1, syn1_r) )
			output.append([ np.max(l2), next_possible_dir_list[np.argmax(l2)] ])

		debug.f_debug.write("outputs: " + str(output) + "\n")
		tmp_curr_dir = max(output)[1]
		self.curr_dir = tmp_curr_dir
		debug.f_debug.write("predicted dir: " + str(self.curr_dir) + "\n")

		# TODO FIX THIS -> take the second max value
	 	# check if current direction is valid (snake cannot go backwards)
		if self.prev_dir is not None:
			if abs(tmp_curr_dir - self.prev_dir) == 2:		
				self.curr_dir = self.prev_dir #randint(0, 3)
				debug.f_debug.write("backwards! keep going " + str(self.prev_dir) + "\n")

		self.prev_dir = self.curr_dir
		
	def get_ANN_inputs(self, world, win):
		'''
		rewards:
			wall or himself = -1
			food = 1
			nothing = 0
		'''

		# define next head pos
		# list of lists that contains the rewards for the three possible future direction of the snake
		ANN_inputs = [] 
		next_head_pos_list, next_possible_dir_list = self.get_next_possible_positions()

		debug.f_debug.write("food coord: " + str(world.food) + "\n")
		
		for next_head_pos, next_possible_dir in zip(next_head_pos_list, next_possible_dir_list):

			debug.f_debug.write("next_head_pos: " + str(next_head_pos) + " | next_possible_dir: " + str(next_possible_dir) +  "\n")
			
			try:
				# retrieve closest food
				min_food_distance = min([ np.sqrt( (next_head_pos[0] - world.food[i][0])**2 + (next_head_pos[1] - world.food[i][1])**2 )
				for i in range(len(world.food)) if len(world.food[i]) > 0])	
			 	# normalize to 0/1
				min_food_distance /= np.sqrt(world.max_y ** 2 + world.max_x ** 2)
				# shift to -1/1 and reverse sign -> 1 is better
				min_food_distance = - ( 2 * min_food_distance - 1) 
			except:
				# no food (?)
				min_food_distance = -1 

			left_rew, go_on_rew, right_rew  = self.get_rewards(next_head_pos, next_possible_dir, world)

			debug.f_debug.write("\tmin_food_distance " + str(min_food_distance) + "\n")
			debug.f_debug.write("\tleft_rew " + str(left_rew) + "\n")
			debug.f_debug.write("\tgo_on_rew " + str(go_on_rew) + "\n")
			debug.f_debug.write("\tright_rew " + str(right_rew) + "\n")

			ANN_inputs.append([min_food_distance, left_rew, go_on_rew, right_rew])
			'''

			curr_tmp_reward = self.get_box_of_view_rewards(next_head_pos, next_possible_dir, world)
			curr_tmp_reward.append(min_food_distance)

			ANN_inputs.append(curr_tmp_reward)	


		return ANN_inputs, next_possible_dir_list

	def get_next_possible_positions(self):
		
		curr_head_pos = self.body[0]
		next_pos = []
		next_possible_dir = []

		# snake is going UP
		if self.curr_dir == 0: 
			# left
			next_pos.append([ curr_head_pos[0], curr_head_pos[1] - 1 ])
			next_possible_dir.append(3)
			# go on
			next_pos.append([ curr_head_pos[0] - 1, curr_head_pos[1] ])
			next_possible_dir.append(0)
			# right
			next_pos.append([ curr_head_pos[0], curr_head_pos[1] + 1 ])
			next_possible_dir.append(1)

		# snake is going RIGHT
		if self.curr_dir == 1:
			# left
			next_pos.append([ curr_head_pos[0] - 1, curr_head_pos[1] ])
			next_possible_dir.append(0)
			# go on
			next_pos.append([ curr_head_pos[0], curr_head_pos[1] + 1 ])
			next_possible_dir.append(1)
			# right
			next_pos.append([ curr_head_pos[0] + 1, curr_head_pos[1] ])
			next_possible_dir.append(2)

		# snake is going DOWN
		if self.curr_dir == 2:
			# left
			next_pos.append([ curr_head_pos[0], curr_head_pos[1] + 1 ])
			next_possible_dir.append(1)
			# go on
			next_pos.append([ curr_head_pos[0] + 1, curr_head_pos[1] ])
			next_possible_dir.append(2)
			# right
			next_pos.append([ curr_head_pos[0], curr_head_pos[1] - 1 ])
			next_possible_dir.append(3)

		# snake is going LEFT
		if self.curr_dir == 3:
			# left
			next_pos.append([ curr_head_pos[0] + 1, curr_head_pos[1] ])
			next_possible_dir.append(2)
			# go on
			next_pos.append([ curr_head_pos[0], curr_head_pos[1] + 1 ])
			next_possible_dir.append(3)
			# right
			next_pos.append([ curr_head_pos[0] + 1, curr_head_pos[1] ])
			next_possible_dir.append(0)

		return next_pos, next_possible_dir


	def get_rewards(self, next_head_pos, next_possible_dir, world):
		'''
		return rewards given next_head_pos and the current direction of the snake
		'''
		# how far the snake can see
		horizon = min(world.max_x, world.max_y) // 2  #  max(world.max_x, world.max_y)
		debug.f_debug.write("horizon: " + str(horizon) + " [max_x: " + str(world.max_x) + ", max_y: " + str(world.max_y) + "]\n")

		# UP
		if next_possible_dir == 0: 
			left_rew = self.get_abs_left_reward(next_head_pos, horizon, world)
			go_on_rew = self.get_abs_up_reward(next_head_pos, horizon, world)
			right_rew = self.get_abs_right_reward(next_head_pos, horizon, world)
		# RIGHT
		elif next_possible_dir == 1:
			left_rew = self.get_abs_up_reward(next_head_pos, horizon, world)
			go_on_rew = self.get_abs_right_reward(next_head_pos, horizon, world)
			right_rew = self.get_abs_down_reward(next_head_pos, horizon, world)
		# DOWN
		elif next_possible_dir == 2:
			left_rew = self.get_abs_right_reward(next_head_pos, horizon, world)
			go_on_rew = self.get_abs_down_reward(next_head_pos, horizon, world)
			right_rew = self.get_abs_left_reward(next_head_pos, horizon, world)
		# LEFT
		elif next_possible_dir == 3:
			left_rew = self.get_abs_down_reward(next_head_pos, horizon, world)
			go_on_rew = self.get_abs_left_reward(next_head_pos, horizon, world)
			right_rew = self.get_abs_up_reward(next_head_pos, horizon, world)

		return left_rew, go_on_rew, right_rew

	def get_box_of_view_rewards(self, next_head_pos, next_possible_dir, world):
		'''
		what the snake sees
                        ________
                        |  box  |
			sssssssssss |  of   |
		    dir --->    | view  |
					    --------
		'''
		# box of view dim (odd)
		w = 5
		h = 5
		# create box of view
		rewards = []
		# UP
		if next_possible_dir == 0:
			box_of_view = [ [next_head_pos[0] - y, next_head_pos[1] - w//2  + x] for x in range(w) for y in range(h)]
		# RIGHT
		elif next_possible_dir == 1:
			box_of_view = [ [next_head_pos[0] - h//2 + y, next_head_pos[1] + x] for y in range(h) for x in range(w)]
		# DOWN
		elif next_possible_dir == 2:
			box_of_view = [ [next_head_pos[0] + y, next_head_pos[1] + w//2  - x] for x in range(w) for y in range(h)]
		# LEFT
		elif next_possible_dir == 3:
			box_of_view = [ [next_head_pos[0] + h//2 - y, next_head_pos[1] - x] for y in range(h) for x in range(w)]
		# get rewards
		for i in box_of_view:
			if i in world.food:
				rewards.append(1) # food
			elif i in self.body or i[0] <= 0 or i[1] <= 0 or i[0] >= world.max_y - 1 or i[1] >= world.max_x - 1:
				rewards.append(-1) # world's border or snake's body
			else:
				rewards.append(0) # nothing special 
		
		return rewards

	def get_abs_left_reward(self, next_head_pos, horizon, world):

		tmp_reward = 0
		for i in range(horizon):
			if [next_head_pos[0], next_head_pos[1] - i] in world.food:
				tmp_reward = 1
				return tmp_reward
			elif next_head_pos[1] - i == 0 or [next_head_pos[0], next_head_pos[1] - i] in self.body:
				tmp_reward = -1
				return tmp_reward

		return tmp_reward

	def get_abs_right_reward(self, next_head_pos, horizon, world):

		tmp_reward = 0
		for i in range(horizon):
			if [next_head_pos[0], next_head_pos[1] + i] in world.food:
				tmp_reward = 1
				return tmp_reward
			elif next_head_pos[1] + i == world.max_x - 1 or [next_head_pos[0], next_head_pos[1] + i] in self.body:
				tmp_reward = -1
				return tmp_reward

		return tmp_reward
			
	def get_abs_up_reward(self, next_head_pos, horizon, world):

		tmp_reward = 0
		for i in range(horizon):
			if [next_head_pos[0] - i, next_head_pos[1]] in world.food:
				tmp_reward = 1
				return tmp_reward
			elif (next_head_pos[0] - i) == 0 or [next_head_pos[0] - i, next_head_pos[1]] in self.body:
				tmp_reward = -1
				return tmp_reward

		return tmp_reward

	def get_abs_down_reward(self, next_head_pos, horizon, world):

		tmp_reward = 0
		for i in range(horizon):
			if [next_head_pos[0] + i, next_head_pos[1]] in world.food:
				tmp_reward = 1
				return tmp_reward
			elif (next_head_pos[0] + i) == world.max_y - 1 or [next_head_pos[0] + i, next_head_pos[1]] in self.body:
				tmp_reward = -1
				return tmp_reward

		return tmp_reward


