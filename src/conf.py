HIDDEN_LAYER_NEURONS = [6,6]
# number of snakes used in each generation
N_SNAKE = 10000
# simulate until N_DEATH deaths
N_DEATH = int(1 * N_SNAKE)
# select best N_CROSS snakes
N_CROSS = int(0.05 * N_SNAKE)
#number of snakes that remains in the next generation
N_SNAKE_SURVIVING = int(0.6 * N_SNAKE)
#output dimension (left, go on, right)
N_CLASS = 3
#snake field dimention
BORDER = 8
#if border are dangerous
BORDER_BOOL = False
#if true the snake see all the field if false 
#just his head position, the food and direction
FIELD_AS_INPUT = False
#input size
if FIELD_AS_INPUT:
    INPUT_SIZE = BORDER**2 + 4
else:
    INPUT_SIZE = 5 + 4

#mutation adding scale factor
EPSILON = 0.1

DNA_SIZE = (BORDER**2+3)*HIDDEN_LAYER_NEURONS[0]
for i in range(len(HIDDEN_LAYER_NEURONS)-1):
    DNA_SIZE += HIDDEN_LAYER_NEURONS[i]*HIDDEN_LAYER_NEURONS[i+1]
DNA_SIZE += HIDDEN_LAYER_NEURONS[-1]*N_CLASS
#how many wight are changed
MUTATION_RATE = 0.01

ITERATION = 100
#ho many snakes are mutated
MUTATION_PROBABILITY = 2000/(N_SNAKE)
#how many turns a snake survives without eating
MAX_LIFE_WITHOUT_FOOD = BORDER**2 / 2
#scala distri
UNIFORMSIZE = 3
#max fitness 
MAX_FITNESS = 18

