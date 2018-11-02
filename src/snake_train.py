import simulation
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import conf
import input
 

SHOW = 10
if __name__ == "__main__":
    input_type = input.PointOfViewUpgraded()
    plt.figure(figsize=(10, 10))
    simulation = simulation.Simulation(input_type, n_snakes=conf.N_SNAKE, visible=True)
    simulation.showBestN(N=SHOW)
    #geneticSnakeGame = geneticControl.GeneticControl(visible=True, n_snakes=conf.N_SNAKE)
    top_fit_mean_vec = []
    top_fit_mean_CIlow_vec = []
    top_fit_mean_CIup_vec = []
    for i in range(conf.ITERATION):
        print("@ generation "+str(i))
        simulation.simulateUntilDeath(n_death=conf.N_DEATH) #simulateUntilDeathOrTimer(n_death=conf.N_DEATH, N = 120) #simulateGeneration(turn=50)
        simulation.showBestN(N=SHOW)
        mean_fit, top_mean_fit, top_fit_CI, p_mutation, parents_fitness, maxfit, minfit, ret = simulation.upgradeGenerationNotUniform()
        print("\tmean fitness: %.3f, top_mean_fitness %.3f [p_mutation: %.3f parents fitness: %.3f max: %.3f, min: %.3f, iterations: %d]" % (mean_fit, top_mean_fit, p_mutation, parents_fitness, maxfit, minfit, ret))
        top_fit_mean_vec.append(top_mean_fit)
        top_fit_mean_CIlow_vec.append(top_fit_CI[0])
        top_fit_mean_CIup_vec.append(top_fit_CI[1])

    # plot results
    plt.plot(np.array(top_fit_mean_vec), c="red")
    plt.fill_between(range(conf.ITERATION), top_fit_mean_CIlow_vec, top_fit_mean_CIup_vec, alpha=0.4)
    plt.legend(["avg. top fitness", str("95%") +  " CI"])
    plt.show()
    
