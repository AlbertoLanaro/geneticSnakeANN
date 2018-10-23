import simulation
import field
import matplotlib.pyplot as plt
import numpy as np
import conf
import sys
import json
import time


if __name__ == "__main__":
    if len(sys.argv) == 1:
        print("Missing file_name argument")
    else:
        fileName = sys.argv[1]
        with open(fileName) as f:
            data = json.load(f)
        if not(data):
            print("FIle "+fileName+" doesn't exists.")
        else:
            conf.HIDDEN_LAYER_NEURONS = data["HIDDEN_LAYER"]
            conf.INPUT_SIZE = data["INPUT_LEN"]
            DNA = data["DNA"]
            npDNA = []
            for i in DNA:
                npDNA.append(np.array(i))
            j = 0
            simulation = simulation.Simulation(visible= True, n_snakes=1)
            simulation.geneticSnakes[0].brain.DNA = npDNA
            simulation.simulateUntilDeath(1)
            print(simulation.geneticSnakes[0].fitness)




        
