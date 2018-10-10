import matplotlib
import matplotlib.pyplot as plt
from matplotlib import animation
import os
import numpy as np

# -- trick ----

def _blit_draw(self, artists, bg_cache):
    # Handles blitted drawing, which renders only the artists given instead
    # of the entire figure.
    updated_ax = []
    for a in artists:
        # If we haven't cached the background for this axes object, do
        # so now. This might not always be reliable, but it's an attempt
        # to automate the process.
        if a.axes not in bg_cache:
            # bg_cache[a.axes] = a.figure.canvas.copy_from_bbox(a.axes.bbox)
            # change here
            bg_cache[a.axes] = a.figure.canvas.copy_from_bbox(a.axes.figure.bbox)
        a.axes.draw_artist(a)
        updated_ax.append(a.axes)

    # After rendering all the needed artists, blit each axes individually.
    for ax in set(updated_ax):
        # and here
        # ax.figure.canvas.blit(ax.bbox)
        ax.figure.canvas.blit(ax.figure.bbox)

# MONKEY PATCH!!
animation.Animation._blit_draw = _blit_draw


def init():
	line.set_data([], [])
	ttl.set_text('')
	return line, ttl

def animate(i):
	filename = 'Dropbox/Coding/Python/snakeANN/data/max_fitness.csv'
	n_lines = (8 + 1) * 50
	with open(filename, 'r') as f:
		f.seek(0, os.SEEK_END)
		fsize = f.tell()
		f.seek(max(fsize - n_lines, 0), 0)
		data = f.readlines()
	data = [float(i.split('\n')[0]) for i in data]
	line.set_data(range(len(data)), data)

	return line, ttl

if __name__ == '__main__':
	matplotlib.rcParams.update({'font.size': 8})
	fig = plt.figure(figsize=(8,3))
	ax = plt.axes(xlim=(0, 2e2), ylim=(-1, 30))
	#ax.set_xlabel()
	ax.set_ylabel('max_fitness')
	ttl = ax.text(.5, 1.05, '', transform = ax.transAxes, va='center', ha='center', fontsize=10)
	line, = ax.plot([], [], lw=1, color='b')
	anim = animation.FuncAnimation(fig, animate, init_func=init, frames=100, interval=20, blit=True)
	plt.show()

