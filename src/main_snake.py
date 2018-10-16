#!/Users/albertolanaro/venv3/bin/python3

import snake
import world
import snake_generation

import matplotlib.pyplot as plt
import curses
import time
import numpy as np
import debug

# General Parameters
MAX_X = 20
MAX_Y = 10
TIMEOUT = 2
N_SNAKE = 8 # number of snakes per generation [> 2]

def init():
	# windon + game initialization
	curses.initscr()
	curses.start_color()
	curses.init_pair(1, curses.COLOR_RED, curses.COLOR_BLACK)
	curses.init_pair(2, curses.COLOR_GREEN, curses.COLOR_BLACK)
	win = curses.newwin(MAX_Y, MAX_X, 0, 0)
	win.keypad(1)
	curses.noecho()
	curses.curs_set(0)
	win.border(0) # set window borders
	win.nodelay(1)
	win.timeout(TIMEOUT)

	return win

if __name__ == '__main__':
	# initialize game window
	win = init()
	snake_world = world.World(win, MAX_X, MAX_Y) # initialize the world
	snakes_gen = snake_generation.SnakeGeneration(N_SNAKE, snake_world, win) # create the 1st snakes generation
	key = None
	while key != 27: # press 'ESC' to quit

		win.border(0)
		# flush debug file
		debug.flush()

		snakes_gen.update(snake_world, win)
		snake_world.update(win, snakes_gen.snakes)
		debug.f_fitness.write(str(round(snakes_gen.max_fitness, 2)) + '\n')
		key = win.getch()

	debug.f_fitness.close()
	curses.endwin()
