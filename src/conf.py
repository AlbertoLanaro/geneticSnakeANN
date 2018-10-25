HIDDEN_LAYER_NEURONS = [4,4,4,4]
# number of snakes used in each generation
N_SNAKE = 10000
# simulate until N_DEATH deaths
N_DEATH = int(1 * N_SNAKE)
# select best N_CROSS snakes
N_CROSS = int(0.4 * N_SNAKE)
#number of snakes that remains in the next generation
N_SNAKE_SURVIVING = int(0.4 * N_SNAKE)
#output dimension (left, go on, right)
N_CLASS = 3
#snake field dimention
BORDER = 8
#if border are dangerous
BORDER_BOOL = True
#if true the snake see all the field if false 
#just his head position, the food and direction
FIELD_AS_INPUT = False

INPUT_SIZE = 0
#mutation adding scale factor
EPSILON = 1

#how many wight are changed
MUTATION_RATE = 0.5

ITERATION = 30
#ho many snakes are mutated
MUTATION_PROBABILITY = 1
#how many turns a snake survives without eating
MAX_LIFE_WITHOUT_FOOD = BORDER**2 / 2
#scala distri
UNIFORMSIZE = 7
#max fitness 
MAX_FITNESS = 18

