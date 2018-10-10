import os

global f_debug
global f_fitness
global f_ANN

f_debug = open("../debug/debug.txt", "w")
f_fitness = open('../debug/max_fitness.txt', 'w')
f_ANN = open('../debug/ANN.txt', 'w')

def flush():
    # flush data to file    
    f_debug.flush()
    f_fitness.flush()
    f_ANN.flush()

    os.fsync(f_debug.fileno())
    os.fsync(f_fitness.fileno())
    os.fsync(f_ANN.fileno())
