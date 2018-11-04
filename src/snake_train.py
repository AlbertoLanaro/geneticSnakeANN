import simulation
import datetime
import time
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import conf
import input
 
SHOW = 5
if __name__ == "__main__":
    simulation.print_conf()
    input_type = input.PointOfViewUpgraded()
    plt.figure(figsize=(10, 10))
    simulation = simulation.Simulation(input_type, n_snakes=conf.N_SNAKE, visible=conf.VISIBLE)
    if conf.VISIBLE:
        simulation.showBestN(N=SHOW)
    top_fit_mean_vec = []
    top_fit_mean_CIlow_vec = []
    top_fit_mean_CIup_vec = []
    for i in range(conf.ITERATION):
        start_time = time.time()
        print("[" + datetime.datetime.today().strftime("%H:%M.%S")  + "] " + "------------------------------ GENERATION " + str(i) + " ------------------------------")
        simulation.simulateUntilDeath(n_death=conf.N_DEATH)
        if conf.VISIBLE:
            simulation.showBestN(N=SHOW)
        mean_fit, top_mean_fit, top_fit_CI, p_mutation, parents_fitness, maxfit, minfit, ret = simulation.upgradeGenerationNotUniform()
        print("\tmean fitness: %.3f, top_mean_fitness %.3f [p_mutation: %.3f parents fitness: %.3f max: %.3f, min: %.3f, iterations: %d]" % (mean_fit, top_mean_fit, p_mutation, parents_fitness, maxfit, minfit, ret))
        top_fit_mean_vec.append(top_mean_fit)
        top_fit_mean_CIlow_vec.append(top_fit_CI[0])
        top_fit_mean_CIup_vec.append(top_fit_CI[1])
        print("\telapsed time [s]: %.2f" % (time.time() - start_time))

    # plot results
    plt.plot(np.array(top_fit_mean_vec), c="red")
    plt.fill_between(range(conf.ITERATION), top_fit_mean_CIlow_vec, top_fit_mean_CIup_vec, alpha=0.4)
    plt.xlabel("generation")
    plt.legend(["avg. top fitness", str("95%") +  " CI"])
    plt.savefig('./fitness.png', bbox_inches='tight')
    plt.show()