import geneticControl
import matplotlib.pyplot as plt
import numpy as np
import conf
 


if __name__ == "__main__":
    fitness = []
    plt.figure(figsize=(10, 10))
    geneticSnakeGame = geneticControl.GeneticControl(n_snakes=conf.Conf.N_SNAKE)
    for i in range(conf.Conf.ITERATION):
        print("generazione "+str(i))
        geneticSnakeGame.simulation.simulateUntilDeath(n_death=conf.Conf.N_DEATH) #simulateGeneration(turn=50)
        fitmedia = geneticSnakeGame.simulation.upgradeGeneration(N=conf.Conf.N_CROSS)
        print(fitmedia)
        fitness.append(fitmedia)
    plt.plot(np.array(fitness), c="pink")
    plt.show()
    
