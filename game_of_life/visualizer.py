import numpy as np
import matplotlib.pyplot as plt
import sys



class Visualizer:
    
    def __init__(self, world, simulation):
        self.world = world
        self.simulation = simulation
        self.fig, self.ax = plt.subplots()
        self.im = self.ax.imshow(world.grid, cmap='binary', interpolation='nearest')
        
        self.fig.canvas.mpl_connect('close_event', self.on_close)
        self.fig.canvas.mpl_connect('button_press_event', self.on_button_click)
        self.fig.canvas.mpl_connect('key_press_event', self.on_key_click)
        
    
    def draw(self, delay):
        self.im.set_data(self.world.grid)
        plt.pause(delay)
    
    
    def on_close(self, event):
        print('-' * 30)
        print('Симуляция досрочно завершена.')
        print('-' * 30)
        sys.exit(0)
    
    
    def on_button_click(self, event):
        if hasattr(event, 'inaxes') and event.inaxes is not None:
            x = round(event.xdata)
            y = round(event.ydata)
            self.world.toggle_cell(x, y)
            self.im.set_data(self.world.grid)
            self.fig.canvas.draw_idle()
    
    
    def on_key_click(self, event):
        key = event.key
        if key == ' ':
            self.simulation.toggle_pause()
        elif key == 'right':
            self.simulation.step_request = True