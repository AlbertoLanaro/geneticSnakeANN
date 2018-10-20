from random import randint

WHITE = (255,255,255)

BLACK = (0,0,0)
RED = (255,0,0)
GREEN = (0, 255,0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
CYAN = (0, 255, 255)
MAGENTA = (255, 0, 255)

all_colors = [BLACK, RED, GREEN, BLUE, YELLOW, CYAN, MAGENTA]

# return a random color
def random():
    # avoid to bright colors
    max_bright = 240
    c = [randint(0,max_bright), randint(0,max_bright), randint(0,max_bright)]
    
    return c