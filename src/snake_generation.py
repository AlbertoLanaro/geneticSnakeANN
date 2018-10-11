import snake
import numpy as np
import random
import debug

def create_snake_gen(snake_world, win, n):
	# create new popolation of snakes
	snakes = [snake.Snake(snake_world, win)]
	snakes_bodies = [snakes[0].body]
	while len(snakes) < n:
		tmp_snake = snake.Snake(snake_world, win)
		# check if snake's body is placed in an empty space
		if not(tmp_snake.body[0] in snakes_bodies):
			snakes.append(tmp_snake)
			snakes_bodies.append(tmp_snake.body[0])

	return snakes

def dec2bin(x): # return string
	x_bin = [(np.binary_repr(i, width=8)) for i in x]
	tmp = ''
	for i in x_bin:
		tmp += i

	return tmp

def mutate_bin(x, p_mutation):
	xx = ''
	for i in range(len(x)):
		p = random.random()
		if p < p_mutation: # mutate
			debug.f_ANN.write("mutation @ index: " + str(i) + "\n")
			if x[i] == '0':
				xx += '1'
			else:
				xx += '0'
		else:
			xx += x[i]

	return xx

def mutate(x, p_mutation):
	for i in range(len(x)):
		p = random.random()
		if p < p_mutation: # mutate
			debug.f_ANN.write("mutation @ index: " + str(i) + "\n")
			#j = random.randint(a=0, b=len(x)-1) 
			#tmp = x[j]
			#x[j] = x[i]
			#x[i] = tmp
			x[i] = 2 * random.random() - 1

class SnakeGeneration:
	def __init__(self, n_snakes, snake_world, win):
		self.snakes = create_snake_gen(snake_world, win, n_snakes)
		self.len = n_snakes
		self.dead_count = 0
		self.max_fitness = -1

	def get_max_fitness(self):
		best_fitness = -1
		for i in range(len(self.snakes)):
			if self.snakes[i].fitness > best_fitness:
				self.max_fitness = self.snakes[i].fitness

	def update(self, snake_world, win):
		win.addstr(0, 1, ' ' + str(self.dead_count) + ' ')
		win.addstr(snake_world.max_y - 1, 1, ' ' + str(round(self.max_fitness, 2)) + ' ')
		for j,i in enumerate(self.snakes):
			if i.is_dead == True:
				self.dead_count += 1
				self.snakes.pop(j) # remove dead snake
				# create a new snake by choosing as parents the snakes with max fitness
				# perform mutation + crossover when creating a new child
				self.add_child(snake_world, win)
			
			debug.f_debug.write("---------- SNAKE ID: " + str(j + 1) + " / " + str(len(self.snakes)) + " ------------\n")
			# update current snake
			i.update(snake_world, win)
			# update max fitness
			self.get_max_fitness()

	def crossover_mutation_bin(self, parent0, parent1, max_fitness, snake_world, win):
		debug.f_ANN.write('-------------------' + '\n')
		p_mutation = 1 / max_fitness

		debug.f_ANN.write('p_mutation: ' + str(p_mutation) + '\n')

		win.addstr(snake_world.max_y - 6, 0, ' ' + str(np.round(p_mutation, 2)) + ' ')
		DNA_p0_bin = dec2bin(np.array(1e2 * parent0.DNA, dtype=int))
		DNA_p1_bin = dec2bin(np.array(1e2 * parent1.DNA, dtype=int))
		
		debug.f_ANN.write('DNA0 ' + str(parent0.DNA) + '\n')
		debug.f_ANN.write('DNA1 ' + str(parent1.DNA) + '\n')

		split_dim = 3
		split0 = [DNA_p0_bin[x:x+split_dim] for x in range(0, len(DNA_p0_bin), split_dim)]
		split1 = [DNA_p1_bin[x:x+split_dim] for x in range(0, len(DNA_p1_bin), split_dim)]	

		newDNA = ''
		for i in range(len(split0)):
			if i % 2 ==0:
				newDNA += split0[i]
			else:
				newDNA += split1[i]

		newDNA = mutate_bin(newDNA, p_mutation)
		newDNA = 1e-2 * np.array([int(newDNA[i : i + 8], 2) for i in range(0, 8 * 108, 8)])
		debug.f_ANN.write('------> new DNA ' + str(newDNA) + '\n')

		return newDNA

	def crossover_mutation(self, parent0, parent1, max_fitness, snake_world, win):
		debug.f_ANN.write('--------------------------------------' + '\n')
	
		p_mutation = 1 / max_fitness
		debug.f_ANN.write('p_mutation: ' + str(p_mutation) + '\n')

		#DNA_p0_bin = dec2bin(np.array(1e2 * parent0.DNA, dtype=int))
		#DNA_p1_bin = dec2bin(np.array(1e2 * parent1.DNA, dtype=int))
		debug.f_ANN.write('DNA0 ' + str(parent0.DNA) + '\n')
		debug.f_ANN.write('DNA1 ' + str(parent1.DNA) + '\n')
		split_dim = 3
		#split0 = [parent0.DNA[x:x+split_dim] for x in range(0, len(parent0.DNA), split_dim)]
		#split1 = [parent0.DNA[x:x+split_dim] for x in range(0, len(parent1.DNA), split_dim)]	
		newDNA = np.zeros_like(parent0.DNA)
		for i in range(0, len(newDNA), 2 * split_dim):
			newDNA[i : i + split_dim] = parent0.DNA[i : i + split_dim]
			newDNA[i + split_dim : i + 2 * split_dim] = parent1.DNA[i + split_dim : i + 2 * split_dim]

		mutate(newDNA, p_mutation)

		debug.f_ANN.write('------> new DNA ' + str(newDNA) + '\n')
		
		return newDNA

	def add_child(self, snake_world, win):
		'''
		Select two parents and create a child by crossover + mutation procedure
		'''
		parent0, parent1, max_fitness = self.parents_selection()
		newDNA = self.crossover_mutation(parent0, parent1, max_fitness, snake_world, win)
		self.snakes.append(snake.Snake(snake_world, win, from_DNA=True, DNA=newDNA))

	def parents_selection(self):
		'''
		Select N/2 random snakes and pick as parent the one with higher fitness
		'''
		'''
		N = 3 * 2	
		try:	
			tmp_index = np.random.choice(range(len(self.snakes)), N, replace=False)
		except:			
			# not enough snakes alive
			N = len(self.snakes)
			tmp_index = range(N)

			debug.f_debug.write("[parents_selection] not enough snakes, using N = " + str(N)  + "\n")

		tmp_index_p0 = tmp_index[ : N//2]
		tmp_index_p1 = tmp_index[N//2 : ]
		# select the two with higher fitness
		parent0 = None
		parent_max_fitness0 = -1 
		parent1 = None
		parent_max_fitness1 = -1 
		for j in range(len(tmp_index_p0)):
			parent_tmp0 = self.snakes[tmp_index_p0[j]]
			parent_tmp1 = self.snakes[tmp_index_p1[j]]
			if parent_tmp0.fitness > parent_max_fitness0:
				parent0 = parent_tmp0
				parent_max_fitness0 = parent_tmp0.fitness
			if parent_tmp1.fitness > parent_max_fitness1:
				parent1 = parent_tmp1
				parent_max_fitness1 = parent_tmp1.fitness

		return parent0, parent1, max(parent_max_fitness0, parent_max_fitness1)
		'''

		# get the 2 snakes with higher fitness
		fitnesses = np.array([i.fitness for i in self.snakes])
		indeces = np.argsort(fitnesses)

		debug.f_debug.write("[ PARENTS SELECTION ] parents' fitnesses: " + str(self.snakes[indeces[-1]].fitness) + ", " + str(self.snakes[indeces[-2]].fitness) + " | "
					"all fitnesses: " + str(fitnesses) + "\n")


		return self.snakes[indeces[-1]], self.snakes[indeces[-2]], max(self.snakes[indeces[-1]].fitness, self.snakes[indeces[-2]].fitness)
		













