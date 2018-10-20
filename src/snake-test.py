import geneticControl
import matplotlib.pyplot as plt
import numpy as np
import conf
 


if __name__ == "__main__":
    fitness = []
    plt.figure(figsize=(10, 10))
    geneticSnakeGame = geneticControl.GeneticControl(visible=True, n_snakes=conf.N_SNAKE)
    for i in range(conf.ITERATION):
        print("@ generation "+str(i))
        geneticSnakeGame.simulation.simulateUntilDeath(n_death=conf.N_DEATH) #simulateGeneration(turn=50)
        geneticSnakeGame.simulation.showBestN(N=5)
        meanfit, maxfit, minfit = geneticSnakeGame.simulation.upgradeGeneration(N=conf.N_CROSS)
        print("\tmean fitness: %.3f [max: %.3f, min: %.3f]" % (meanfit, maxfit, minfit))
        fitness.append(meanfit)
    plt.plot(np.array(fitness), c="pink")
    plt.show()
    
