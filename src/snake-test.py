import geneticControl
import matplotlib.pyplot as plt
import numpy as np
import conf
 


if __name__ == "__main__":
    fitness = []
    topfitness = []
    plt.figure(figsize=(10, 10))
    geneticSnakeGame = geneticControl.GeneticControl(visible=True, n_snakes=conf.N_SNAKE)
    for i in range(conf.ITERATION):
        print("@ generation "+str(i))
        geneticSnakeGame.simulation.simulateUntilDeathOrTimer(n_death=conf.N_DEATH, N = 120) #simulateGeneration(turn=50)
        geneticSnakeGame.simulation.showBestN(N=5)
        meanfit, top_mean, maxfit, minfit, ret = geneticSnakeGame.simulation.upgradeGeneration()
        print("\tmean fitness: %.3f, top_mean_fitness %.3f [max: %.3f, min: %.3f, iterations: %d]" % (meanfit,top_mean, maxfit, minfit, ret))
        fitness.append(meanfit)
        topfitness.append(top_mean)
    plt.plot(np.array(fitness), c="pink")
    plt.plot(np.array(topfitness), c="pink")

    plt.show()
    
