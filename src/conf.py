import datetime

HIDDEN_LAYER_NEURONS = [5]
# number of snakes used in each generation
N_SNAKE = 1000
# simulate until N_DEATH deaths
N_DEATH = int(1 * N_SNAKE)
# select best N_CROSS snakes
N_CROSS = int(0.01 * N_SNAKE)
#number of snakes that remains in the next generation
N_SNAKE_SURVIVING = int(0.1 * N_SNAKE)
#output dimension (left, go on, right)
N_CLASS = 3
#snake field dimention
BORDER = 8
#if border are dangerous
BORDER_BOOL = True
INPUT_SIZE = 0
ITERATION = 500
#snake mutation probability
MUTATION_PROBABILITY = 1.0
#DNA mutation probability
MUTATION_RATE = 0.2
#mutation adding scale factor
EPSILON = 3
#how many turns a snake survives without eating
MAX_LIFE_WITHOUT_FOOD = BORDER*8
#scalar distri
UNIFORMSIZE = 7
#max fitness 
MAX_FITNESS = 25
# visualize the training process
VISIBLE = False
DNA_PATH = "./DNA/DNA_1"