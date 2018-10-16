import simulation


'''
We should:
1) Create all the snake that we want to simulate
2) Start a simulation and keep the result
3) Create the new generation
'''

SNAKES_PER_SIMULATION = 10
N_SIMULATION = 1

class GenticControl:
    def __init__(self):
        # create game simulations
        self.simulations = [simulation.Simulation(SNAKES_PER_SIMULATION) for _ in range(N_SIMULATION)]
