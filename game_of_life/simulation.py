import matplotlib.pyplot as plt

from rules import *
from world import World
from visualizer import Visualizer



class Simulation:
    
    def __init__(self, size_x: int = 100, size_y: int = 100, rules=None, delay: float = 0.05, paused: bool = False, n_species: int = 1, random_init: bool = True):
        self.n_species = n_species
        self.random_init = random_init
        self.world = World(size_x, size_y, n_species, random_init)
        self.rules = rules or ConwayRules()
        self.visualizer = Visualizer(self.world, self)
        self.delay = delay
        self.step_count = 0
        self.paused = paused
        self.step_request = False
        self.reset_request = False
    
    
    def toggle_pause(self):
        self.paused = not self.paused


    def step(self):
        neighbours = self.world.get_neighbours()
        new_grid = self.rules.apply(self.world.grid)
        self.world.update(new_grid)
        self.step_count += 1
    
    
    def run(self, steps='inf'):
        step = 0
        infinite = True if steps == 'inf' else False
        while infinite or step < steps:
            
            if self.reset_request:
                self.reset_request = False
                self.world.update(World(self.world.size_x, self.world.size_y, self.n_species, self.random_init).grid)
                self.visualizer.draw(self.delay)
                
            if not self.paused:
                print(f'Шаг {self.step_count}; Количество живых клеток: {self.world.grid.sum()};')
                self.step()
                self.visualizer.draw(self.delay)
                if not infinite:
                    step += 1
            else:
                if self.step_request:
                    self.step_request = False
                    self.step()
                    self.visualizer.draw(self.delay)
                    if not infinite:
                        step += 1
                else:
                    plt.pause(0.05)