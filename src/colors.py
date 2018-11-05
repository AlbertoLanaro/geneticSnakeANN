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
    min_bright = 50
    c = [randint(min_bright, 255), randint(min_bright, 255), randint(min_bright, 255)]
    
    return c