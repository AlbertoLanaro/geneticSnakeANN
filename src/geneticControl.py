import simulation

#
# TODO farei interagire con i tasti. 1) Parte la simulazione per un po' 
# senza mostrare nulla a parte la fitness nel tempo. Poi un tasto tipo "v" per 
# vedere o togliere la visualizzazzione che permette di vedere
# Per fare questo ho aggiunto un flag "visible" che se attivo in snake allora prova
# a realizzare la visualizzazione
# i migliori 10 della simulazione sull'interfaccia che abbiamo fatto
# e un classico "Q" per terminare e avere un resconto dei risultati
# a proposito: aggiungere dei dati da salvare tipo: numero generazioni
# fitness media a generazione ecc
#

'''
We should:
1) Create all the snake that we want to simulate
2) Start a simulation and keep the result
3) Create the new generation
'''

class GeneticControl:
    def __init__(self, otherset=None, n_snakes=10, visible=False):
        # create game simulations from zero
        self.simulation = simulation.Simulation(n_snakes=n_snakes, visible=visible)
        if not(otherset is None):
            if otherset.simulation.n_snakes < n_snakes:
                print("ERRORE; COPIO DA UN SET PICCOLO")
                return 
            otherset.simulation.sortSnakesForFitness()
            for i in range(n_snakes):
                self.simulation.geneticSnakes[i] = otherset.simulation.geneticSnakes[i]



    def start(self):
        self.simulation.simulateGeneration(turn = 100)
        print("Simulati un milione per 100 turni")
        self.simulation.showBestN()
        self.simulation.simulateGeneration(turn=100)
        # I should use:
        #1 simulations.simulateGeneration()
        #2 simulations.reproduce()
