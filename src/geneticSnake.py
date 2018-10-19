import snake
import brain
import fitness
import field

import math

class GeneticSnake:
    def __init__(self, field, DNA = None, reproduced = False, parent0 = None, parent0 = None): # TODO pass a DNA a BRAIN
        self.Nquad = field.Field.N ** 2
        self.field = field
        self.snake = snake.Snake()
        # brain input: N*N + curr_dir + head coord + angle
        if reproduced:
            self.brain = brain.Brain(field.Field.N ** 2 + 4, reproduced = True, parten0 = parent0, parent1 = parent1)
        if DNA = None:
            self.brain = brain.Brain(field.Field.N ** 2 + 4)
        else:
            self.brain = brain.Brain(field.Field.N ** 2 + 4 ,DNA = DNA)
        self.fitness = 0
        self.count = field.Field.N ** 2
        self.is_dead = False

    def update(self):
        # update genetic snake only if alive
        if not(self.is_dead):
            # get body + food + old direction
            curr_input = self.getCurrentInput()
            next_possible_dirs = self.getNextPossibleDir()
            # get new direction from brain
            # outputs:
            #   0: go on
            #   1: left
            #   2: right
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
        curr_dir = self.snake.getCurrDir()
        # left
        rel_left = (curr_dir - 1) % 4
        # go on
        rel_go_on = curr_dir
        # right
        rel_right = (curr_dir + 1) % 4

        return [rel_left, rel_go_on, rel_right]


    '''
    Constructs ANN's input
    '''
    def getCurrentInput(self):
        # get info from snake
        snake_body = self.snake.getBodyPosition()
        food = self.snake.getFoodPosition()
        snake_head = snake_body[0]
        norm_snake_head = [ snake_head[0] / field.Field.N , snake_head[1] / field.Field.N ]
        angle = math.atan2( (food[1] - snake_head[1]), (food[0] - snake_head[0]) ) # y / x [rad]
        curr_dir = (self.snake.getCurrDir() % 4) - 1
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
        input.append(curr_dir)
        input.append(angle)
        return input

    def changeVisibility(self, visibility):
        self.snake.visible(visibility)
        
