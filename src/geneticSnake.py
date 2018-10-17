import snake
import brain
import fitness
import field

class GeneticSnake:
    def __init__(self, field): # TODO passa DNA a BRAIN
        self.field = field
        self.snake = snake.Snake()
        self.brain = brain.Brain(field.Field.N ** 2)
        self.fitness = fitness.Fitness()
    
    def update(self):
        # get body + food + old direction 
        curr_input = self.getCurrentInput()
        # get new direction from brain 
        # outputs:
        #   0: go on
        #   1: left
        #   2: right
        next_possible_dirs = self.getNextPossibleDir()
        tmp_dir = self.brain.predictOutput(curr_input)
        new_dir = next_possible_dirs[tmp_dir]
        # update snake body
        curr_reward = self.snake.update(self.field, new_dir)
        # update fitness
        self.fitness.update(curr_reward)

    def getNextPossibleDir(self):
        prev_dir = self.snake.getPrevDir()
        # left
        rel_left = (prev_dir - 1) % 4
        # go on
        rel_go_on = prev_dir
        # right
        rel_right = (prev_dir + 1) % 4

        return [rel_left, rel_go_on, rel_right]

    def getCurrentInput(self):
        # get info from snake
        snake_body = self.snake.getBodyPosition()
        food = self.snake.getFoodPosition()
        norm_snake_head = [ snake_body[0][1] / field.Field.N , snake_body[0][1] / field.Field.N ]
        prev_dir = self.snake.getPrevDir()
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
        input.append(norm_snake_head)
        input.append(prev_dir)

        return input

        
        
