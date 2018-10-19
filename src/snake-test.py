import geneticControl

if __name__ == "__main__":
    geneticSnakeGame = geneticControl.GeneticControl(snakes_per_sim=10, n_simulations=1, visible=True)
    geneticSnakeGame.start()