import random
import numpy as np
from activation_functions import sigmoid, softmax, relu

# brain parameters
HIDDEN_UNITS = [6] # more hidden layers -> [6 10 10 ...]
N_CLASS = 3

class Brain:
    def __init__(self, input_len, DNA=None):
        if DNA == None:
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

    def crossDNA(self1, self2):





    def predictOutput(self, input):
        l_tmp = sigmoid( np.dot(input, self.DNA[0] ) )
        for i in self.DNA[1:]:
            l_tmp = sigmoid( np.dot(l_tmp, i) )
        output = np.argmax(l_tmp)

        return output
