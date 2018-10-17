class Fitness:
    INIT_BONUS = 5
    def __init__(self):
        self.value = Fitness.INIT_BONUS
        
    def update(self, reward):
        # health decreases at each iteration
        self.value -= 0.1 * self.value
        if reward == 0: # do nothing
            pass
        if reward == -2 or reward == -1: # snake hit himself or borders
            pass
        if reward == 1:
            self.value += Fitness.INIT_BONUS * 0.5
        
            
