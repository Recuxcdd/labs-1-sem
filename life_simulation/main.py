import matplotlib.pyplot as plt
import numpy as np
import sys
from rules import *



class World:
    
    def __init__(self, size_x: int = 100, size_y: int = 100, random_init: bool = True):
        self.size_x = size_x
        self.size_y = size_y
        if random_init:
            self.grid = np.random.randint(0, 2, (size_x, size_y), dtype=np.int8)
        else:
            self.grid = np.zeros((size_x, size_y), dtype=np.int8)
            
    
    def get_neighbours(self) -> np.ndarray:
        g = self.grid
        neighbours = (
            np.roll(np.roll(g, 1, 0), 1, 1) +  # верх-лево
            np.roll(np.roll(g, 1, 0), -1, 1) + # верх-право
            np.roll(np.roll(g, -1, 0), 1, 1) + # низ-лево
            np.roll(np.roll(g, -1, 0), -1, 1) +# низ-право
            np.roll(g, 1, 0) +                 # вверх
            np.roll(g, -1, 0) +                # вниз
            np.roll(g, 1, 1) +                 # влево
            np.roll(g, -1, 1)                  # вправо
        )
        return neighbours
    
    
    def update(self, new_grid: np.ndarray):
        self.grid = new_grid
        
        
    def toggle_cell(self, x: int, y: int):
        self.grid[x, y] = 1 - self.grid[x, y]



class Visualizer:
    
    def __init__(self, world):
        self.world = world
        self.fig, self.ax = plt.subplots()
        self.im = self.ax.imshow(world.grid, cmap='binary', interpolation='nearest')
        self.fig.canvas.mpl_connect('close_event', self.on_close)
        self.fig.canvas.mpl_connect('button_press_event', self.on_button_click)
    
    
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
            self.world.toggle_cell(y, x)
            self.im.set_data(self.world.grid)
            self.fig.canvas.draw_idle()



class Simulation:
    
    def __init__(self, size_x: int = 100, size_y: int = 100, rules=None, delay: float = 0.05):
        self.world = World(size_x, size_y)
        self.rules = rules or ConwayRules()
        self.visualizer = Visualizer(self.world)
        self.delay = delay
        self.step_count = 0
        
    
    def step(self):
        neighbours = self.world.get_neighbours()
        new_grid = self.rules.apply(self.world.grid, neighbours)
        self.world.update(new_grid)
        self.step_count += 1
    
    
    def run(self, steps: int = 1000):
        for _ in range(steps):
            print(f'Шаг {self.step_count}; Количество живых клеток: {self.world.grid.sum()};')
            self.step()
            self.visualizer.draw(self.delay)



sim = Simulation(size_x=50, size_y=50, rules=ConwayRules(), delay=0.1)
sim.run(steps=1000)