import snake
import brain
import fitness
import field

import math

class GeneticSnake:
    def __init__(self, field, DNA = None): # TODO passa DNA a BRAIN
        self.Nquad = field.Field.N ** 2
        self.field = field
        self.snake = snake.Snake()
        # brain input: N*N + prev_dir + head coord + angle
        if DNA = None:
            self.brain = brain.Brain(field.Field.N ** 2 + 4)
        else:
            self.brain = brain.Brain(field.Field.N ** 2 + 4 , DNA)
        self.fitness = 0
        self.count = field.Field.N ** 2
        self.is_dead = False

    def update(self):
        # update genetic snake only if alive
        if not(self.is_dead):
            # get body + food + old direction
            curr_input = self.getCurrentInput()
            # get new direction from brain
            # outputs:
            #   0: go on
            #   1: left
            #   2: right

            next_possible_dirs = self.getNextPossibleDir()
            tmp_dir = self.brain.predictOutput(curr_input)
            # map output to possible snake directions
            new_dir = next_possible_dirs[tmp_dir]
            # update snake body
            curr_reward = self.snake.update(self.field, new_dir)
            # update fitness

            self.count -= 1
            if curr_reward == -1 or self.count == 0:
                self.is_dead = True
            elif curr_reward == 1:
                self.fitness += curr_reward
                self.count = self.Nquad
            '''
            self.fitness.update(curr_reward)
            # check if snake is dead
            if curr_reward == -1 or self.fitness < 1e-1:
                #compute final fitness
                self.fitness = self.fitness / self.snake.timer # TODO check: use [self.fitness] or [self.snake.score] ???
                self.is_dead = True
            '''

    def getNextPossibleDir(self):
        prev_dir = self.snake.getPrevDir()
        # left
        rel_left = (prev_dir - 1) % 4
        # go on
        rel_go_on = prev_dir
        # right
        rel_right = (prev_dir + 1) % 4

        return [rel_left, rel_go_on, rel_right]


    '''
    Funtion that construct the net input as
    '''
    def getCurrentInput(self):
        # get info from snake
        snake_body = self.snake.getBodyPosition()
        food = self.snake.getFoodPosition()
        snake_head = snake_body[0]
        norm_snake_head = [ snake_head[0] / field.Field.N , snake_head[1] / field.Field.N ]
        angle = math.atan2( (food[1] - snake_head[1]), (food[0] - snake_head[0]) ) # y / x [rad]
        prev_dir = (self.snake.getPrevDir()%4) - 1
        input = []
        # map field's rewards
        for i in range(field.Field.N):
            for j in range(self.field.N):
                if [i,j] == food:
                    input.append(1)
                elif [i,j] in snake_body:
                    input.append(-1)
                elif [i,j] == -1 or [i,j] == field.Field.N:
                    input.append(-2)
                else:
                    input.append(0)
        input.append(norm_snake_head[0])
        input.append(norm_snake_head[1])
        input.append(prev_dir)
        input.append(angle)
        return input

    '''
    It return the new DNA 
    '''
    def repreoduce(self1, self2):
        return newDNA = self1.brain.reproduce(self2)
