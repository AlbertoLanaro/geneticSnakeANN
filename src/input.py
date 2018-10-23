import conf
import math

class FieldAsInput:
    def __init__(self):
        self.size = conf.BORDER ** 2 + 3
        conf.INPUT_SIZE = conf.BORDER ** 2 + 3
    
    def getInput(self, snake):
        input = []
        snake_body = snake.getBodyPosition()
        food = snake.getFoodPosition()
        snake_head = snake_body[0]
        norm_snake_head = [snake_head[0] /
                           conf.BORDER, snake_head[1] / conf.BORDER]
        curr_dir = (snake.getCurrDir() % 4) - 1
        for i in range(1, conf.BORDER):
            for j in range(conf.BORDER):
                if [i, j] == food:
                    input.append(1)
                elif [i, j] in snake_body:
                    input.append(-1)
                elif [i, j] == -1 or [i, j] == conf.BORDER:
                    input.append(-2)
                else:
                    input.append(0)
        input.append(norm_snake_head[0])
        input.append(norm_snake_head[1])
        # currend dir
        input.append(curr_dir)
        return input
    
class HybridInput:
    def __init__(self):
        self.size = 11
        conf.INPUT_SIZE = 11
    
    def getInput(self, snake):
        # get info from snake
        snake_body = snake.getBodyPosition()
        food = snake.getFoodPosition()
        snake_head = snake_body[0]
        norm_snake_head = [snake_head[0] /
                           conf.BORDER, snake_head[1] / conf.BORDER]
        angle = math.atan2((food[1] - snake_head[1]),
                           (food[0] - snake_head[0]))  # y / x [rad]
        curr_dir = (snake.getCurrDir() % 4) - 1
        input = []
        #food coord
        input.append(food[0] / conf.BORDER)
        input.append(food[1] / conf.BORDER)
        #tail coord
        input.append(snake_body[-1][0] / conf.BORDER)
        input.append(snake_body[-1][1] / conf.BORDER)
        # what snake sees in his 3 cross directions
        views = self.getViews(snake)
        for view in views:
            input.append(view)
        #length as input -> TODO normalize
        #input.append(snake.score)
        # head coord
        input.append(norm_snake_head[0])
        input.append(norm_snake_head[1])
        # currend dir
        input.append(curr_dir)
        # current angle between food and head
        input.append(angle)

        return input

    '''
    Returns what the snake sees respectively in his left, up and right view
        1 if food
        -1 if himself (or border if conf.BORDER_BOOL is True)
        0 otherwise
    '''

    def getViews(self, snake):
        # UP
        if snake.curr_dir == 0:
            left_rew = self.get_abs_left_view(snake)
            go_on_rew = self.get_abs_up_view(snake)
            right_rew = self.get_abs_right_view(snake)
        # RIGHT
        elif snake.curr_dir == 1:
            left_rew = self.get_abs_up_view(snake)
            go_on_rew = self.get_abs_right_view(snake)
            right_rew = self.get_abs_down_view(snake)
        # DOWN
        elif snake.curr_dir == 2:
            left_rew = self.get_abs_right_view(snake)
            go_on_rew = self.get_abs_down_view(snake)
            right_rew = self.get_abs_left_view(snake)
        # LEFT
        elif snake.curr_dir == 3:
            left_rew = self.get_abs_down_view(snake)
            go_on_rew = self.get_abs_left_view(snake)
            right_rew = self.get_abs_up_view(snake)

        return left_rew, go_on_rew, right_rew

    def get_abs_up_view(self, snake):
        snake_head = snake.getBodyPosition()[0]
        for i in range(1, conf.BORDER - 1):
            if [snake_head[0], (snake_head[1] - i)%conf.BORDER] == snake.food:
                return 1
            elif conf.BORDER_BOOL == True:
                if [snake_head[0], (snake_head[1] - i)%conf.BORDER] in snake.getBodyPosition() or [snake_head[0], (snake_head[1] - i)] == -1:
                    return -1
            elif [snake_head[0], (snake_head[1] - i)%conf.BORDER] in snake.getBodyPosition():
                return -1

        return 0

    def get_abs_down_view(self, snake):
        snake_head = snake.getBodyPosition()[0]
        for i in range(1, conf.BORDER - 1):
            if [snake_head[0], (snake_head[1] + i) % conf.BORDER] == snake.food:
                return 1
            elif conf.BORDER_BOOL == True:
                if [snake_head[0], (snake_head[1] + i) % conf.BORDER] in snake.getBodyPosition() or [snake_head[0], (snake_head[1] + i)] == conf.BORDER:
                    return -1
            elif [snake_head[0], (snake_head[1] + i) % conf.BORDER] in snake.getBodyPosition():
                return -1

        return 0

    def get_abs_left_view(self, snake):
        snake_head = snake.getBodyPosition()[0]
        for i in range(1, conf.BORDER -1):
            if [(snake_head[0] - i)%conf.BORDER, snake_head[1]] == snake.food:
                return 1
            elif conf.BORDER:
                if [(snake_head[0] - i)%conf.BORDER, snake_head[1]] in snake.getBodyPosition() or [(snake_head[0] - i), snake_head[1]] == -1:
                    return -1
            elif [(snake_head[0] - i)%conf.BORDER, snake_head[1]] in snake.getBodyPosition():
                return -1

        return 0

    def get_abs_right_view(self, snake):
        snake_head = snake.getBodyPosition()[0]
        for i in range(1, conf.BORDER -1 ):
            if [(snake_head[0] + i)%conf.BORDER, snake_head[1]] == snake.food:
                return 1
            elif conf.BORDER:
                if [(snake_head[0] + i)%conf.BORDER, snake_head[1]] in snake.getBodyPosition() or [(snake_head[0] + i), snake_head[1]] == conf.BORDER:
                    return -1
            elif [(snake_head[0] + i)%conf.BORDER, snake_head[1]] in snake.getBodyPosition():
                return-1

        return 0
    

