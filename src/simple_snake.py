import curses
from curses import KEY_RIGHT, KEY_LEFT, KEY_UP, KEY_DOWN
from random import randint

WALL = 0 
WALL = 1#int(input('Wanna play with walls? [1/0] '))
curses.initscr()
win = curses.newwin(20, 60, 0, 0)
win.keypad(1)
curses.noecho()
curses.curs_set(0)
win.border(0)
win.nodelay(1)

key = KEY_RIGHT                                                    # Initializing values
score = 0

snake = [[4,10], [4,9], [4,8]]                                     # Initial snake co-ordinates
food = [1,20]                                                       # First food co-ordinates

win.addch(food[0], food[1], '*')                                   # Prints the food

while key != 27:                                                   # While Esc key is not pressed
    win.border(0)
    win.addstr(0, 2, 'Score : ' + str(score) + ' ')                # Printing 'Score' and
    win.addstr(0, 27, ' SNAKE ')                                   # 'SNAKE' strings
    win.timeout(round(150 - (len(snake)/5 + len(snake)/10)%120))   # Increases the speed of Snake as its length increases
    
    prevKey = key                                                  # Previous key pressed
    event = win.getch()
    key = key if event == -1 else event 


    if key == ord(' '):                                            # If SPACE BAR is pressed, wait for another
        key = -1                                                   # one (Pause/Resume)
        while key != ord(' '):
            key = win.getch()
        key = prevKey
        continue

    if key not in [KEY_LEFT, KEY_RIGHT, KEY_UP, KEY_DOWN, 27]:     # If an invalid key is pressed
        key = prevKey

    if (key == KEY_LEFT and prevKey == KEY_RIGHT) or (key == KEY_RIGHT and prevKey == KEY_LEFT) or (key == KEY_UP and prevKey == KEY_DOWN) or (key == KEY_DOWN and prevKey == KEY_UP):
        key = prevKey

    # Calculates the new coordinates of the head of the snake. NOTE: len(snake) increases.
    # This is taken care of later at [1].
    snake.insert(0, [snake[0][0] + (key == KEY_DOWN and 1) + (key == KEY_UP and -1), snake[0][1] + (key == KEY_LEFT and -1) + (key == KEY_RIGHT and 1)])

    # If snake crosses the boundaries, make it enter from the other side
    if WALL:
        if snake[0][0] == 0 or snake[0][0] == 19 or snake[0][1] == 0 or snake[0][1] == 59: break
    else:
        if snake[0][0] == 0: snake[0][0] = 18
        if snake[0][1] == 0: snake[0][1] = 58
        if snake[0][0] == 19: snake[0][0] = 1
        if snake[0][1] == 59: snake[0][1] = 1

    # If snake runs over itself
    if snake[0] in snake[1:]: break
    
    if snake[0] == food:                                            # When snake eats the food
        food = []
        score += 1
        while food == []:
            food = [randint(1, 18), randint(1, 58)]                 # Calculating next food's coordinates
            if food in snake: food = []
        win.addch(food[0], food[1], '*')
    else:    
        last = snake.pop()                                          # [1] If it does not eat the food, length decreases
        win.addch(last[0], last[1], ' ')
    win.addch(snake[0][0], snake[0][1], '#')
    
curses.endwin()
print("Score - " + str(score))
