import numpy as np



class World:
    
    def __init__(self, size_x: int = 100, size_y: int = 100, n_species: int = 1, random_init: bool = True):
        self.size_x = size_x
        self.size_y = size_y
        if random_init:
            self.grid = np.random.randint(0, n_species + 1, (size_y, size_x), dtype=np.int8)
        else:
            self.grid = np.zeros((size_y, size_x), dtype=np.int8)
            
    
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
        self.grid[y, x] = (self.grid[y, x] + 1) % 4