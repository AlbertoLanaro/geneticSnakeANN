import simulation
import matplotlib.pyplot as plt
import numpy as np
import conf
import input
 

SHOW = 6
if __name__ == "__main__":
    input_type = input.PointOfView()
    fitness = []
    topfitness = []
    plt.figure(figsize=(10, 10))
    simulation = simulation.Simulation(
        input_type, n_snakes=conf.N_SNAKE, visible=True)
    simulation.showBestN(N=SHOW)
    #geneticSnakeGame = geneticControl.GeneticControl(visible=True, n_snakes=conf.N_SNAKE)
    for i in range(conf.ITERATION):
        print("@ generation "+str(i))
        simulation.simulateUntilDeath(n_death=conf.N_DEATH) #simulateUntilDeathOrTimer(n_death=conf.N_DEATH, N = 120) #simulateGeneration(turn=50)
        simulation.showBestN(N=SHOW)
        #meanfit, top_mean, maxfit, minfit, ret = geneticSnakeGame.simulation.upgradeGeneration()
        meanfit, top_mean, Average_parent, maxfit, minfit, ret = simulation.upgradeGenerationNotUniform()
        print("\tmean fitness: %.3f, top_mean_fitness %.3f, avg_parent %.3f [max: %.3f, min: %.3f, iterations: %d]" % (
            meanfit, top_mean, Average_parent,  maxfit, minfit, ret))
        fitness.append(meanfit)
        topfitness.append(top_mean)
    plt.plot(np.array(fitness), c="pink")
    plt.plot(np.array(topfitness), c="pink")

    plt.show()
    
