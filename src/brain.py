import random
import numpy as np
from activation_functions import sigmoid, softmax, relu
import conf 
import json
import os
import copy

# brain parameters
HIDDEN_UNITS = conf.HIDDEN_LAYER_NEURONS # more hidden layers -> [6 10 10 ...]
N_CLASS = conf.N_CLASS

# create folder to store json file of the best snakes
try:
    os.makedirs("./jsonstore")
except:
    pass

class Brain:
    def __init__(self, input_len, DNA = None, reproduced = False, parent0 = None, parent1 = None):
        if reproduced:
            self.crossDNA(parent0, parent1)
            self.mutate()
        elif DNA == None:
            # create random brain synapsis
            # first layer
            self.DNA = [ conf.UNIFORMSIZE*(2 * np.random.random(input_len * HIDDEN_UNITS[0]) - 1) ]
            # hidden layers
            for n in range(len(HIDDEN_UNITS) - 1):
                self.DNA.append(conf.UNIFORMSIZE*( 2 * np.random.random(HIDDEN_UNITS[n] * HIDDEN_UNITS[n+1]) - 1) )
            # output layers
            self.DNA.append(conf.UNIFORMSIZE*(2 * np.random.random(HIDDEN_UNITS[-1] * N_CLASS) - 1))
        else:
            # create brain from DNA
            self.DNA = DNA
    
    def mutate(self, p_mutation):
        new_DNA = []
        for syn in self.DNA:
            section = []
            for s in range(len(syn)):
                p = random.random()
                # completely change neuron value
                if conf.EPSILON > 7:
                    if p < p_mutation:
                        # not perturbate but initialize new neuron
                        section.append(conf.UNIFORMSIZE * (2*random.random() - 1))
                    else:
                        section.append(syn[s])
                else:
                    if p < conf.MUTATION_RATE:
                        app = syn[s]
                        app = app + conf.EPSILON * (2*random.random() - 1)
                        section.append(app)
                    else:
                        section.append(syn[s])
            new_DNA.append(np.array(section))
        self.DNA = new_DNA

    def crossDNA(self, parent0, parent1):
        split_dim = random.randint(2, 10)
        newDNA = copy.deepcopy(parent0.DNA)
        for i in range(len(newDNA)):
            for j in range(0, len(newDNA[i]),2* split_dim):
                newDNA[i][j + split_dim: j + 2 *split_dim] = parent1.DNA[i][j + split_dim: j + 2*split_dim]
        self.DNA = newDNA

    def crossDNAAndMutate(self, parent0, parent1, p_mutation=0.0):
        self.crossDNA(parent0, parent1)
        self.mutate(p_mutation=p_mutation)

    def predictOutput(self, input):
        # input layer
        l_tmp = sigmoid( np.dot(input, self.DNA[0].reshape([len(input), HIDDEN_UNITS[0]])) )
        # hidden layers
        # self.DNA[1:-1]
        for d in range(1, len(self.DNA) - 1):
            l_tmp = sigmoid( np.dot(l_tmp, self.DNA[d].reshape([len(l_tmp), HIDDEN_UNITS[d]])))
        # prediction layer
        pred = softmax( np.dot(l_tmp, self.DNA[-1].reshape(len(l_tmp), N_CLASS)) )
        # prediction
        output = np.argmax(pred)

        return output
    
    def DNAsave(self, fitness):
        DNA = []
        for i in self.DNA:
            DNA.append(i.tolist())
        store = {
            "HIDDEN_LAYER": conf.HIDDEN_LAYER_NEURONS,
            "INPUT_LEN": conf.INPUT_SIZE,
            "DNA": DNA
        }
        with open("./jsonstore/DNA_fitness="+str(fitness) +
                  ".json", 'w') as f:
            json.dump(store, f, ensure_ascii=False)



