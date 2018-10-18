import random
import numpy as np
from activation_functions import sigmoid, softmax, relu

# brain parameters
HIDDEN_UNITS = [6] # more hidden layers -> [6 10 10 ...]
N_CLASS = 3

class Brain:
    def __init__(self, input_len, DNA = None, reproduced = False, parent0 = None, parent1 = None):
        if reproduced:
            self.DNA = self.crossDNA(parent0, parent1)
            self.mutate(0.01)
        elif DNA == None:
            # create random brain synapsis
            # first layer
            self.DNA = [ 2 * np.random.random(input_len * HIDDEN_UNITS[0]) - 1]
            # hidden layers
            for n in range(len(HIDDEN_UNITS) - 1):
                self.DNA.append(2 * np.random.random(HIDDEN_UNITS[n] * HIDDEN_UNITS[n+1]) - 1)
            # output layers
            self.DNA.append(2 * np.random.random(HIDDEN_UNITS[-1] * N_CLASS) - 1)
        else:
            # create brain from DNA
            self.DNA = DNA

    def mutate(self, p_mutation=0.1):
        new_DNA = []
        for syn in self.DNA:
            for neuron in syn:
                p = random.random()
                if p < p_mutation:
                    syn[neuron] = 2 * random.random() - 1
            new_DNA.append(syn)
        self.DNA = new_DNA

    def crossDNA(self, parent0, parent1):
        split_dim = random.randint(2, 5)
        newDNA = np.zeros_like(parent0.DNA)
        for i in range(0, len(newDNA), 2 * split_dim):
			newDNA[i : i + split_dim] = parent0.DNA[i : i + split_dim]
			newDNA[i + split_dim : i + 2 * split_dim] = parent1.DNA[i + split_dim : i + 2 * split_dim]
        self.DNA = newDNA

    def crossDNAAndMutate(self, parent0, parent1):
        self.crossDNA(parent0, parent1)
        self.mutate(0.05)



    def predictOutput(self, input):
        l_tmp = sigmoid( np.dot(input, self.DNA[0] ) )
        for i in self.DNA[1:]:
            l_tmp = sigmoid( np.dot(l_tmp, i) )
        output = np.argmax(l_tmp)

        return output
