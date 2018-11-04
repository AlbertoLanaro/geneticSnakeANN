import conf
import math

class FieldAsInput:
    def __init__(self):
        self.size = (conf.BORDER) **2 + 3
        conf.INPUT_SIZE = conf.BORDER ** 2 + 3
    
    def getInput(self, snake):
        input = []
        snake_body = snake.getBodyPosition()
        food = snake.getFoodPosition()
        snake_head = snake_body[0]
        norm_snake_head = [snake_head[0] /
                           conf.BORDER, snake_head[1] / conf.BORDER]
        curr_dir = (snake.getCurrDir() % 4) - 1
        for i in range(conf.BORDER):
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
        views = getViews(snake)
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


#this input type is very simple. 
# 3 input which map the content of the future cells if he turn right, left, go streight
#4 input that map where is the food
class PointOfView:
    def __init__(self):
        self.size = 7
        conf.INPUT_SIZE = 7

    def getInput(self, snake):
        possible_direction = snake.getNextPossibleDir()
        input = []
        # what snake sees in his 3 cross directions
        head = snake.body[0]
        next_left = [head[0] + (possible_direction[0] == 1 and 1) +(possible_direction[0] == 3 and -1), head[1] +(possible_direction[0] == 2 and 1) + (possible_direction[0] == 0 and -1)]
        next_right = [head[0] + (possible_direction[2] == 1 and 1) +(possible_direction[2] == 3 and -1), head[1] +(possible_direction[2] == 2 and 1) + (possible_direction[2] == 0 and -1)]
        next_straight = [head[0] + (possible_direction[1] == 1 and 1) +
                        (possible_direction[1] == 3 and -1), head[1] +
                        (possible_direction[1] == 2 and 1) + (possible_direction[1] == 0 and -1)]
        input.append(snake.mapPoint(next_left))
        input.append(snake.mapPoint(next_right))
        input.append(snake.mapPoint(next_straight))
        wherefood = findFood(snake.food, head, snake.curr_dir)
        input.append(wherefood[0])
        input.append(wherefood[1])
        input.append(wherefood[2])
        input.append(wherefood[3])
        return input

#1) We add the last three direction changes and improove the field viewed
#turn right 1, left -1
class PointOfViewUpgraded:
    def __init__(self):
        self.size = 13
        conf.INPUT_SIZE = 13

    def getInput(self, snake):
        possible_direction = snake.getNextPossibleDir()
        input = []
        # what snake sees in his 3 cross directions
        head = snake.body[0]
        next_left = [head[0] + (possible_direction[0] == 1 and 1) + (possible_direction[0] == 3 and -1),
                     head[1] + (possible_direction[0] == 2 and 1) + (possible_direction[0] == 0 and -1)]
        nextnext_left = [next_left[0] + (possible_direction[0] == 1 and 1) + (possible_direction[0] == 3 and -1),
                         next_left[1] + (possible_direction[0] == 2 and 1) + (possible_direction[0] == 0 and -1)]
        next_right = [head[0] + (possible_direction[2] == 1 and 1) + (possible_direction[2] == 3 and -1),
                      head[1] + (possible_direction[2] == 2 and 1) + (possible_direction[2] == 0 and -1)]
        nextnext_right = [next_right[0] + (possible_direction[2] == 1 and 1) + (possible_direction[2] == 3 and -1),
                          next_right[1] + (possible_direction[2] == 2 and 1) + (possible_direction[2] == 0 and -1)]
        next_straight = [head[0] + (possible_direction[1] == 1 and 1) +
                         (possible_direction[1] == 3 and -1), head[1] +
                         (possible_direction[1] == 2 and 1) + (possible_direction[1] == 0 and -1)]
        nextnext_straight = [next_straight[0] + (possible_direction[1] == 1 and 1) +
                             (possible_direction[1] == 3 and -1), next_straight[1] +
                         (possible_direction[1] == 2 and 1) + (possible_direction[1] == 0 and -1)]
        
        input.append(snake.mapPoint(next_left))
        input.append(snake.mapPoint(next_right))
        input.append(snake.mapPoint(next_straight))
        input.append(snake.mapPoint(nextnext_left))
        input.append(snake.mapPoint(nextnext_right))
        input.append(snake.mapPoint(nextnext_straight))
        input.append(snake.lastturn[0])
        input.append(snake.lastturn[1])
        input.append(snake.lastturn[2])
        wherefood = findFood(snake.food, head, snake.curr_dir)
        input.append(wherefood[0])
        input.append(wherefood[1])
        input.append(wherefood[2])
        input.append(wherefood[3])
        return input



#map the food position for the snake. It changes for each direction.
# if food is up -> food_y < head_y if down >
# if food is left -> food_x < head_x id down >
left_front = [-1, -1, -1, 1]
right_front = [1,-1,-1,-1]
right_bottom = [-1,1,-1,-1]
left_bottom = [-1,-1,1,-1]
front = [1,0,0,0]
right = [0,1,0,0]
bottom = [0,0,1,0]
left = [0,0,0,1]
map = {
    "--0": left_front,
    "--1": left_bottom,
    "--2": right_bottom,
    "--3": right_front,

    "+-0": right_front,
    "+-1": left_front,
    "+-2": left_bottom,
    "+-3": right_bottom,

    "++0": right_bottom,
    "++1": right_front,
    "++2": left_front,
    "++3": left_bottom,

    "-+0": left_bottom,
    "-+1": right_bottom,
    "-+2": right_front,
    "-+3": left_front,

    "=-0": front,
    "=-1": left,
    "=-2": bottom,
    "=-3": right,

    "+=0": right,
    "+=1": front,
    "+=2": left,
    "+=3": bottom,

    "=+0": bottom,
    "=+1": right,
    "=+2": front,
    "=+3": left,

    "-=0": right,
    "-=1": front,
    "-=2": left,
    "-=3": bottom,

    "==0" : [0,0,0,0],
    "==1" : [0, 0, 0, 0],
    "==2" : [0, 0, 0, 0],
    "==3" : [0, 0, 0, 0]
}

def findFood(food, head, direction):
    string = ""
    if(head[0] > food[0]):
        string += "-"
    elif(head[0] < food[0]):
        string += "+"
    else:
        string += "="
    if(head[1] > food[1]):
        string += "-"
    elif(head[1] < food[1]):
        string += "+"
    else:
        string += "="
    string += str(direction)
    return map[string]
    
    
        
    '''
    Returns what the snake sees respectively in his left, up and right view
        1 if food
        -1 if himself (or border if conf.BORDER_BOOL is True)
        0 otherwise
    '''
def getViews(snake):
    # UP
    if snake.curr_dir == 0:
        left_rew = get_abs_left_view(snake, half = True)
        go_on_rew = get_abs_up_view(snake)
        right_rew = get_abs_right_view(snake, half = True)
    # RIGHT
    elif snake.curr_dir == 1:
        left_rew = get_abs_up_view(snake, half=True)
        go_on_rew = get_abs_right_view(snake)
        right_rew = get_abs_down_view(snake, half=True)
    # DOWN
    elif snake.curr_dir == 2:
        left_rew = get_abs_right_view(snake, half=True)
        go_on_rew = get_abs_down_view(snake)
        right_rew = get_abs_left_view(snake, half=True)
    # LEFT
    elif snake.curr_dir == 3:
        left_rew = get_abs_down_view(snake, half=True)
        go_on_rew = get_abs_left_view(snake)
        right_rew = get_abs_up_view(snake, half=True)

    return left_rew, go_on_rew, right_rew

def get_abs_up_view( snake, half= False):
    snake_head = snake.getBodyPosition()[0]
    if half:
        limit = int(conf.BORDER/2)
    else:
        limit = conf.BORDER
    for i in range(1, limit - 1):
        if [snake_head[0], (snake_head[1] - i)%conf.BORDER] == snake.food:
            return 1
        elif conf.BORDER_BOOL == True:
            if [snake_head[0], (snake_head[1] - i)%conf.BORDER] in snake.getBodyPosition() or [snake_head[0], (snake_head[1] - i)] == -1:
                return -1
        elif [snake_head[0], (snake_head[1] - i)%conf.BORDER] in snake.getBodyPosition():
            return -1

    return 0

def get_abs_down_view( snake, half = False):
    snake_head = snake.getBodyPosition()[0]
    if half:
        limit = int(conf.BORDER/2)
    else:
        limit = conf.BORDER
    for i in range(1, limit - 1):
        if [snake_head[0], (snake_head[1] + i) % conf.BORDER] == snake.food:
            return 1
        elif conf.BORDER_BOOL == True:
            if [snake_head[0], (snake_head[1] + i) % conf.BORDER] in snake.getBodyPosition() or [snake_head[0], (snake_head[1] + i)] == conf.BORDER:
                return -1
        elif [snake_head[0], (snake_head[1] + i) % conf.BORDER] in snake.getBodyPosition():
            return -1

    return 0

def get_abs_left_view( snake, half = False):
    snake_head = snake.getBodyPosition()[0]
    if half:
        limit = int(conf.BORDER/2)
    else:
        limit = conf.BORDER
    for i in range(1, limit -1):
        if [(snake_head[0] - i)%conf.BORDER, snake_head[1]] == snake.food:
            return 1
        elif conf.BORDER:
            if [(snake_head[0] - i)%conf.BORDER, snake_head[1]] in snake.getBodyPosition() or [(snake_head[0] - i), snake_head[1]] == -1:
                return -1
        elif [(snake_head[0] - i)%conf.BORDER, snake_head[1]] in snake.getBodyPosition():
            return -1

    return 0

def get_abs_right_view( snake, half = False):
    snake_head = snake.getBodyPosition()[0]
    if half:
        limit = int(conf.BORDER/2)
    else:
        limit = conf.BORDER
    for i in range(1, limit -1 ):
        if [(snake_head[0] + i)%conf.BORDER, snake_head[1]] == snake.food:
            return 1
        elif conf.BORDER:
            if [(snake_head[0] + i)%conf.BORDER, snake_head[1]] in snake.getBodyPosition() or [(snake_head[0] + i), snake_head[1]] == conf.BORDER:
                return -1
        elif [(snake_head[0] + i)%conf.BORDER, snake_head[1]] in snake.getBodyPosition():
            return-1

    return 0



    

