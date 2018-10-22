import snake
import brain
import fitness
import field
import conf
import math

class GeneticSnake:
    def __init__(self, fld, visible = False, DNA = None, reproduced = False, parent0 = None, parent1 = None): # TODO pass a DNA a BRAIN
        self.field = fld
        self.exposition = [[-1, -1], [-1, -1], [-1, -1], [-1, -1]]
        self.snake = snake.Snake(visible = visible)
        # brain input: N*N + curr_dir + head coord + angle
        if conf.FIELD_AS_INPUT:
            fieldarea = conf.BORDER **2
        else:
            #food position and tale position = 4
            fieldarea = 7
        input_size = 4 + fieldarea # field.Field.N ** 2 + 4
        if reproduced:
            self.brain = brain.Brain(input_size, reproduced = True, parent0 = parent0, parent1 = parent1)
        if DNA == None:
            self.brain = brain.Brain(input_size)
        else:
            self.brain = brain.Brain(input_size, DNA = DNA)
        self.fitness = 0
        self.count = conf.MAX_LIFE_WITHOUT_FOOD
        self.is_dead = False

    def update(self):
        # update genetic snake only if alive
        if not(self.is_dead):
            # get body + food + old direction
            curr_input = self.getCurrentInput()
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
                self.expositionn = [[-1, -1], [-1, -1], [-1, -1], [-1, -1]]
                self.fitness += curr_reward
                self.count = conf.MAX_LIFE_WITHOUT_FOOD

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
        # # map field's rewards
        if conf.FIELD_AS_INPUT:
            for i in range(1, field.Field.N):
                for j in range(self.field.N):
                    if [i,j] == food:
                        input.append(1)
                    elif [i,j] in snake_body:
                        input.append(-1)
                    elif [i,j] == -1 or [i,j] == field.Field.N:
                        input.append(-2)
                    else:
                        input.append(0)
        else:
            #food as input
            input.append(food[0] / field.Field.N)
            input.append(food[1] / field.Field.N)
            #tale as imput
            input.append(snake_body[-1][0]/ field.Field.N)
            input.append(snake_body[-1][1]/ field.Field.N)
            # what snake sees in his 3 cross directions
            views = self.getViews()
            for view in views:
                input.append(view)
        #length as input -> TODO normalize
        #input.append(self.snake.score)
        # head coord
        input.append(norm_snake_head[0])
        input.append(norm_snake_head[1])
        # currend dir
        input.append(curr_dir)
        # current angle between food and head
        input.append(angle)



        return input
    
    def getViews(self):

        # UP
        if self.snake.curr_dir == 0:
            left_rew = self.get_abs_left_view()
            go_on_rew = self.get_abs_up_view()
            right_rew = self.get_abs_right_view()
        # RIGHT
        elif self.snake.curr_dir == 1:
            left_rew = self.get_abs_up_view()
            go_on_rew = self.get_abs_right_view()
            right_rew = self.get_abs_down_view()
        # DOWN
        elif self.snake.curr_dir == 2:
            left_rew = self.get_abs_right_view()
            go_on_rew = self.get_abs_down_view()
            right_rew = self.get_abs_left_view()
        # LEFT
        elif self.snake.curr_dir == 3:
            left_rew = self.get_abs_down_view()
            go_on_rew = self.get_abs_left_view()
            right_rew = self.get_abs_up_view()

        return left_rew, go_on_rew, right_rew

    def clear(self):
        visible = self.snake.visible
        color = self.snake.color
        self.snake.__init__(visible=visible, color=color)
        self.fitness = 0
        self.count = conf.MAX_LIFE_WITHOUT_FOOD
        self.is_dead = False
        self.exposition = [[-1, -1], [-1, -1], [-1, -1], [-1, -1]]

    def loop(self):
        head = self.snake.getBodyPosition()[0]
        if head == self.exposition[0]:
            #self.fitness -= 1
            return True
        else:
            self.exposition[:] = self.exposition[1:]
            self.exposition.append(head)
            return False

    def get_abs_up_view(self):
        snake_head = self.snake.getBodyPosition()[0]
        ret = 0
        for i in range(1, field.Field.N):
            if [snake_head[0], snake_head[1] - i] == self.snake.food:
                ret = 1
                return ret
            elif [snake_head[0], snake_head[1] - i] in self.snake.getBodyPosition():
                ret = -1
                return ret

        return ret

    def get_abs_down_view(self):
        snake_head = self.snake.getBodyPosition()[0]
        ret = 0
        for i in range(1, field.Field.N):
            if [snake_head[0], snake_head[1] + i] == self.snake.food:
                ret = 1
                return ret
            elif [snake_head[0], snake_head[1] + i] in self.snake.getBodyPosition():
                ret = -1
                return ret

        return ret

    def get_abs_left_view(self):
        snake_head = self.snake.getBodyPosition()[0]
        ret = 0
        for i in range(1, field.Field.N):
            if [snake_head[0] - i, snake_head[1]] == self.snake.food:
                ret = 1
                return ret
            elif [snake_head[0] - i, snake_head[1]] in self.snake.getBodyPosition():
                ret = -1
                return ret

        return ret

    def get_abs_right_view(self):
        snake_head = self.snake.getBodyPosition()[0]
        ret = 0
        for i in range(1, field.Field.N):
            if [snake_head[0] + i, snake_head[1]] == self.snake.food:
                ret = 1
                return ret
            elif [snake_head[0] + i, snake_head[1]] in self.snake.getBodyPosition():
                ret = -1
                return ret

        return ret
