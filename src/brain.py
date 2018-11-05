import random
import numpy as np
from activation_functions import sigmoid, softmax, relu
import conf 
import json
import os
import copy 
import datetime

# brain parameters
MAX_NEURON_VAL = 7.0

# create folder to store json file of the best snakes
try:
    dna_path = conf.DNA_PATH
    os.makedirs(dna_path)
except:
    pass

class Brain:
    def __init__(self, input_len):
        # create random brain synapsis
        # first layer
        self.DNA = [ np.random.uniform(-MAX_NEURON_VAL, MAX_NEURON_VAL, input_len * conf.HIDDEN_LAYER_NEURONS[0]) ]
        # hidden layers
        for n in range(len(conf.HIDDEN_LAYER_NEURONS) - 1):
            self.DNA.append(np.random.uniform(-MAX_NEURON_VAL, MAX_NEURON_VAL, (conf.HIDDEN_LAYER_NEURONS[n] * conf.HIDDEN_LAYER_NEURONS[n+1])))
        # output layers
        self.DNA.append(np.random.uniform(-MAX_NEURON_VAL, MAX_NEURON_VAL, conf.HIDDEN_LAYER_NEURONS[-1] * conf.N_CLASS))
    
    # def mutate(self, p_mutation):
    #     for syn in self.DNA:
    #         for s in syn:
    #             p = random.random()
    #             # completely change neuron value
    #             if conf.EPSILON > 7:
    #                 if p < p_mutation:
    #                     # not perturbate but initialize new neuron
    #                     s = random.uniform(-MAX_NEURON_VAL, MAX_NEURON_VAL)
    #             else:
    #             # perturbate the correspondent neuron
    #                 if p < p_mutation:
    #                     s = s + conf.EPSILON * (2*random.random() - 1)

    def mutate(self, p_mutation):
        new_DNA = []
        for syn in self.DNA:
            section = []
            for s in range(len(syn)):
                p = random.random()
                if conf.EPSILON > 7:
                    if p < p_mutation:
                        # not perturbate but initialize new neuron
                        section.append(random.uniform(-MAX_NEURON_VAL, MAX_NEURON_VAL))
                    else:
                        section.append(syn[s])
                else:
                    # perturbate the correspondent neuron
                    if p < p_mutation:
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
            for j in range(0, len(newDNA[0]), 2 * split_dim):
                newDNA[i][j + split_dim : j + 2 * split_dim] = parent1.DNA[i][j + split_dim : j + 2 * split_dim]
        self.DNA = newDNA

    def crossDNAAndMutate(self, parent0, parent1, p_mutation=0.0):
        self.crossDNA(parent0, parent1)
        self.mutate(p_mutation=p_mutation)

    def predictOutput(self, input):
        # input layer
        l_tmp = sigmoid( np.dot(input, self.DNA[0].reshape([len(input), conf.HIDDEN_LAYER_NEURONS[0]])) )
        # hidden layers
        for d in range(1, len(self.DNA) - 1):
            l_tmp = sigmoid( np.dot(l_tmp, self.DNA[d].reshape([len(l_tmp), conf.HIDDEN_LAYER_NEURONS[d]])))
        # prediction layer
        pred = softmax( np.dot(l_tmp, self.DNA[-1].reshape(len(l_tmp), conf.N_CLASS)) )
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
        with open( dna_path + "/DNA_"+str(fitness) + ".json", 'w') as f:
            json.dump(store, f, ensure_ascii=False)



