import os

global f_debug
global f_fitness
global f_ANN

f_fitness = open('/tmp/max_fitness.txt', 'w')
f_ANN = open('/tmp/ANN.txt', 'w')
f_debug = open("/tmp/debug.txt", "w")
    
def flush():
    # flush data to file    
    f_debug.flush()
    f_fitness.flush()
    f_ANN.flush()

    os.fsync(f_debug.fileno())
    os.fsync(f_fitness.fileno())
    os.fsync(f_ANN.fileno())
