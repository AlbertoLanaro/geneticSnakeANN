import snake
import brain
import fitness
import field
import conf
import math

class GeneticSnake:
    def __init__(self, fld, input_type, visible=False, DNA=None, reproduced=False, parent0=None, parent1=None):  #  TODO pass a DNA a BRAIN
        self.field = fld
        self.input = input_type
        # array used to detect if a snake is looping
        self.exposition = [[-1, -1], [-1, -1], [-1, -1], [-1, -1]]
        self.snake = snake.Snake(visible = visible)
        if reproduced:
            self.brain = brain.Brain(self.input.size, reproduced = True, parent0 = parent0, parent1 = parent1)
        if DNA == None:
            self.brain = brain.Brain(self.input.size)
        else:
            self.brain = brain.Brain(self.input.size, DNA = DNA)
        self.fitness = 0
        # max number of steps the snake can take without eating anything
        self.count = conf.MAX_LIFE_WITHOUT_FOOD
        self.is_dead = False

    '''
    Update the state of the current snake:
        1. get its next possible directions
        2. compute features and predict output
        3. update is_dead flag and fitness
    '''
    def update(self):
        # update genetic snake only if alive
        if not(self.is_dead):
            # get body + food + old direction
            curr_input = self.input.getInput(self.snake)
            next_possible_dirs = self.getNextPossibleDir()
            # get new direction from brain
            # outputs:
            #   0: left
            #   1: go on
            #   2: right
            tmp_dir = self.brain.predictOutput(curr_input)
            # map output to possible snake directions
            new_dir = next_possible_dirs[tmp_dir]
            # update snake body
            curr_reward = self.snake.update(self.field, new_dir)
            # update fitness
            self.count = self.count - 1
            # snake hit walls/himself or no food found for self.count turns
            if curr_reward == -1 or self.count == 0 or (curr_reward != 1 and self.loop()):
                #self.fitness -=  2
                self.is_dead = True
            # snake found food
            elif curr_reward == 1:
                self.exposition = [[-1, -1], [-1, -1], [-1, -1], [-1, -1]]
                self.fitness += curr_reward
                self.count = conf.MAX_LIFE_WITHOUT_FOOD

    '''
    Returns the possible direction of the snakes mapped w.r.t. its current direction
    '''
    def getNextPossibleDir(self):
        curr_dir = self.snake.getCurrDir()
        # left
        rel_left = (curr_dir - 1) % 4
        # go on
        rel_go_on = curr_dir
        # right
        rel_right = (curr_dir + 1) % 4

        return [rel_left, rel_go_on, rel_right]


    '''
    reset the state of the current snake
    '''
    def clear(self):
        visible = self.snake.visible
        color = self.snake.color
        self.snake.__init__(visible=visible, color=color)
        self.fitness = 0
        self.count = conf.MAX_LIFE_WITHOUT_FOOD
        self.is_dead = False
        self.exposition = [[-1, -1], [-1, -1], [-1, -1], [-1, -1]]

    '''
    Check if snake is looping (bad!)
    '''
    def loop(self):
        head = self.snake.getBodyPosition()[0]
        if head == self.exposition[0]:
            return True
        else:
            self.exposition[:] = self.exposition[1:]
            self.exposition.append(head)
            return False
