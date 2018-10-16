import random
import numpy as np
from activation_functions import sigmoid, softmax, relu

# brain parameters
HIDDEN_LAYERS = 1
HIDDEN_UNITS = 6

class Brain:
    def __init__(self, input_len):
        # create brain synapsis
        self.DNA = [ 2 * np.random.random(input_len * HIDDEN_UNITS) - 1 for _ in range(HIDDEN_LAYERS + 1)]
    
    def mutate(self, p_mutation=0.1):
        new_DNA = []
        for syn in self.DNA:
            for neuron in syn:
                p = random.random()
                if p < p_mutation:
                    syn[neuron] = 2 * random.random() - 1
            new_DNA.append(syn)
        self.DNA = new_DNA

    def predictOutput(self, input):
        l_tmp = sigmoid( np.dot(input, self.DNA[0] ) )
        for i in self.DNA[1:]:
            l_tmp = sigmoid( np.dot(l_tmp, i) )
        output = np.max(l_tmp)

        return output



