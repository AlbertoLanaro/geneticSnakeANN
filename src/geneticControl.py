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
    def __init__(self, snakes_per_sim=100000, n_simulations=1, visible=False):
        # create game simulations
        self.simulations = [simulation.Simulation(snakes_per_sim, visible=visible) for _ in range(n_simulations)]
        
    def start(self):
        for simulation in self.simulations:
            simulation.simulateGeneration(2000)
            simulation.reproduce()