HIDDEN_LAYER_NEURONS = [6, 5]
N_SNAKE = 10000
# simulate until N_DEATH deaths
N_DEATH = int(0.95 * N_SNAKE)
# select best N_CROSS snakes
N_CROSS = int(0.01 * N_SNAKE)
#number of snakes that remains in the next generation
N_SNAKE_SURVIVING = int(0.4 * N_SNAKE)
#output dimension
N_CLASS = 3
#snake field dimention
BORDER = 8
#if true the snake see all the field if false 
#just his head position, the food and direction
FIELD_AS_IMPUT = False
#mutation adding scale factor
EPSILON = 0.3
DNA_SIZE = (BORDER**2+3)*HIDDEN_LAYER_NEURONS[0]
for i in range(len(HIDDEN_LAYER_NEURONS)-1):
    DNA_SIZE += HIDDEN_LAYER_NEURONS[i]*HIDDEN_LAYER_NEURONS[i+1]
DNA_SIZE += HIDDEN_LAYER_NEURONS[-1]*N_CLASS
#how many wight are changed
MUTATION_RATE = 0.01

ITERATION = 50
#ho many snakes are mutated
MUTATION_PROBABILITY = 100/(N_SNAKE)
#how many turns a snake survives without eating
MAX_LIFE_WITHOUT_FOOD = 45
#scala distri
UNIFORMSIZE = 7


