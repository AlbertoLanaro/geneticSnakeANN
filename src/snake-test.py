import geneticControl

if __name__ == "__main__":
    fitness = []
    geneticSnakeGame = geneticControl.GeneticControl(n_snakes=15, visible=True)
    for i in range(200):
        print("generazione "+str(i))
        geneticSnakeGame.simulation.simulateUntilDeath(n_death=10) #simulateGeneration(turn=50)
        fitmoment = geneticSnakeGame.simulation.upgradeGeneration(N=10)
        print(fitmoment)
        fitness.append(fitmoment)
