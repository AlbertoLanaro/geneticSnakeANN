import geneticControl

if __name__ == "__main__":
    fitness = []
    geneticSnakeGame = geneticControl.GeneticControl(n_snakes=1000)
    for i in range(1000):
        print("generazione "+str(i))
        geneticSnakeGame.simulation.simulateGeneration(turn=50)
        fitmoment = geneticSnakeGame.simulation.upgradeGeneration(N=10)
        print(fitmoment)
        fitness.append(fitmoment)
