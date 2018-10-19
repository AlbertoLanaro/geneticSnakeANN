import geneticControl

if __name__ == "__main__":
    geneticSnakeGame = geneticControl.GeneticControl(n_snakes=100000)
    geneticSnakeGame.simulation.simulateGeneration(turn=10)
    print("Simulati un milione per 100 turni")
    geneticSnakeGame2 = geneticControl.GeneticControl(
        otherset=geneticSnakeGame, visible =True, n_snakes=10)
    print(geneticSnakeGame2.simulation.n_snakes)
    geneticSnakeGame2.simulation.simulateGeneration(turn=100)
