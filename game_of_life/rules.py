import numpy as np



class BasicRules:
    
    def apply(self, grid: np.ndarray) -> np.ndarray:
        raise NotImplementedError
    


class ConwayRules(BasicRules):
    
    def apply(self, grid: np.ndarray) -> np.ndarray:
        neighbours = (
            np.roll(np.roll(grid, 1, 0), 1, 1) +  # верх-лево
            np.roll(np.roll(grid, 1, 0), -1, 1) + # верх-право
            np.roll(np.roll(grid, -1, 0), 1, 1) + # низ-лево
            np.roll(np.roll(grid, -1, 0), -1, 1) +# низ-право
            np.roll(grid, 1, 0) +                 # вверх
            np.roll(grid, -1, 0) +                # вниз
            np.roll(grid, 1, 1) +                 # влево
            np.roll(grid, -1, 1)                  # вправо
        )
        
        birth = neighbours == 3
        survive = (grid == 1) & ((neighbours == 2) | (neighbours == 3))
        new_grid = (birth | survive).astype(np.uint8)
        return new_grid
    


class RecuxcdRules(BasicRules):
    
    def apply(self, grid: np.ndarray) -> np.ndarray:
        neighbours = (
            np.roll(np.roll(grid, 1, 0), 1, 1) +  # верх-лево
            np.roll(np.roll(grid, 1, 0), -1, 1) + # верх-право
            np.roll(np.roll(grid, -1, 0), 1, 1) + # низ-лево
            np.roll(np.roll(grid, -1, 0), -1, 1) +# низ-право
            np.roll(grid, 1, 0) +                 # вверх
            np.roll(grid, -1, 0) +                # вниз
            np.roll(grid, 1, 1) +                 # влево
            np.roll(grid, -1, 1)                  # вправо
        )
        
        birth = neighbours == 2
        survive = (grid == 1) & ((neighbours == 1) | (neighbours == 4))
        new_grid = (birth | survive).astype(np.uint8)
        return new_grid
        


class HighLifeRules(BasicRules):
    
    def apply(self, grid: np.ndarray) -> np.ndarray:
        neighbours = (
            np.roll(np.roll(grid, 1, 0), 1, 1) +  # верх-лево
            np.roll(np.roll(grid, 1, 0), -1, 1) + # верх-право
            np.roll(np.roll(grid, -1, 0), 1, 1) + # низ-лево
            np.roll(np.roll(grid, -1, 0), -1, 1) +# низ-право
            np.roll(grid, 1, 0) +                 # вверх
            np.roll(grid, -1, 0) +                # вниз
            np.roll(grid, 1, 1) +                 # влево
            np.roll(grid, -1, 1)                  # вправо
        )
        
        birth = (neighbours == 3) | (neighbours == 6)
        survive = (grid == 1) & ((neighbours == 2) | (neighbours == 3))
        new_grid = (birth | survive).astype(np.uint8)
        return new_grid



class ImmortalRules(BasicRules):
    
    def apply(self, grid: np.ndarray) -> np.ndarray:
        neighbours = (
            np.roll(np.roll(grid, 1, 0), 1, 1) +  # верх-лево
            np.roll(np.roll(grid, 1, 0), -1, 1) + # верх-право
            np.roll(np.roll(grid, -1, 0), 1, 1) + # низ-лево
            np.roll(np.roll(grid, -1, 0), -1, 1) +# низ-право
            np.roll(grid, 1, 0) +                 # вверх
            np.roll(grid, -1, 0) +                # вниз
            np.roll(grid, 1, 1) +                 # влево
            np.roll(grid, -1, 1)                  # вправо
        )
        
        birth = (neighbours == 2)
        survive = (grid == 1)
        new_grid = (birth | survive).astype(np.uint8)
        return new_grid
    
    

class ThreeSpeciesSuperPredatorsRules(BasicRules):
    
    def apply(self, grid: np.ndarray) -> np.ndarray:
        plants_mask = (grid == 1).astype(int)
        herb_mask = (grid == 2).astype(int)
        pred_mask = (grid == 3).astype(int)
        
        plant_neighbours = (
            np.roll(np.roll(plants_mask, 1, 0), 1, 1) +  # верх-лево
            np.roll(np.roll(plants_mask, 1, 0), -1, 1) + # верх-право
            np.roll(np.roll(plants_mask, -1, 0), 1, 1) + # низ-лево
            np.roll(np.roll(plants_mask, -1, 0), -1, 1) +# низ-право
            np.roll(plants_mask, 1, 0) +                 # вверх
            np.roll(plants_mask, -1, 0) +                # вниз
            np.roll(plants_mask, 1, 1) +                 # влево
            np.roll(plants_mask, -1, 1)                  # вправо
        )
        herb_neighbours = (
            np.roll(np.roll(herb_mask, 1, 0), 1, 1) +  # верх-лево
            np.roll(np.roll(herb_mask, 1, 0), -1, 1) + # верх-право
            np.roll(np.roll(herb_mask, -1, 0), 1, 1) + # низ-лево
            np.roll(np.roll(herb_mask, -1, 0), -1, 1) +# низ-право
            np.roll(herb_mask, 1, 0) +                 # вверх
            np.roll(herb_mask, -1, 0) +                # вниз
            np.roll(herb_mask, 1, 1) +                 # влево
            np.roll(herb_mask, -1, 1)                  # вправо
        )
        pred_neighbours = (
            np.roll(np.roll(pred_mask, 1, 0), 1, 1) +  # верх-лево
            np.roll(np.roll(pred_mask, 1, 0), -1, 1) + # верх-право
            np.roll(np.roll(pred_mask, -1, 0), 1, 1) + # низ-лево
            np.roll(np.roll(pred_mask, -1, 0), -1, 1) +# низ-право
            np.roll(pred_mask, 1, 0) +                 # вверх
            np.roll(pred_mask, -1, 0) +                # вниз
            np.roll(pred_mask, 1, 1) +                 # влево
            np.roll(pred_mask, -1, 1)                  # вправо
        )
        
        plant_birth = (grid == 0) & (herb_neighbours <= 4) & (plant_neighbours > 0)
        herb_birth = (plant_neighbours >= 4) & (herb_neighbours >= 2)
        pred_birth = (pred_neighbours >= 2) & (herb_neighbours > 0)
        
        plant_survive = (grid == 1) & (herb_neighbours <= 4) 
        herb_survive = (grid == 2) & (pred_neighbours == 0) & (plant_neighbours > 0)
        pred_survive = (grid == 3) & (herb_neighbours > 0) & (pred_neighbours == 1)
        
        new_grid = np.zeros_like(grid)
        new_grid[plant_birth] = 1
        new_grid[plant_survive] = 1
        new_grid[herb_birth] = 2
        new_grid[herb_survive] = 2
        new_grid[pred_birth] = 3
        new_grid[pred_survive] = 3
        
        return new_grid



class ThreeSpeciesNormalRules(BasicRules):
    
    def apply(self, grid: np.ndarray) -> np.ndarray:
        plants_mask = (grid == 1).astype(int)
        herb_mask = (grid == 2).astype(int)
        pred_mask = (grid == 3).astype(int)
        
        plant_neighbours = (
            np.roll(np.roll(plants_mask, 1, 0), 1, 1) +  # верх-лево
            np.roll(np.roll(plants_mask, 1, 0), -1, 1) + # верх-право
            np.roll(np.roll(plants_mask, -1, 0), 1, 1) + # низ-лево
            np.roll(np.roll(plants_mask, -1, 0), -1, 1) +# низ-право
            np.roll(plants_mask, 1, 0) +                 # вверх
            np.roll(plants_mask, -1, 0) +                # вниз
            np.roll(plants_mask, 1, 1) +                 # влево
            np.roll(plants_mask, -1, 1)                  # вправо
        )
        herb_neighbours = (
            np.roll(np.roll(herb_mask, 1, 0), 1, 1) +  # верх-лево
            np.roll(np.roll(herb_mask, 1, 0), -1, 1) + # верх-право
            np.roll(np.roll(herb_mask, -1, 0), 1, 1) + # низ-лево
            np.roll(np.roll(herb_mask, -1, 0), -1, 1) +# низ-право
            np.roll(herb_mask, 1, 0) +                 # вверх
            np.roll(herb_mask, -1, 0) +                # вниз
            np.roll(herb_mask, 1, 1) +                 # влево
            np.roll(herb_mask, -1, 1)                  # вправо
        )
        pred_neighbours = (
            np.roll(np.roll(pred_mask, 1, 0), 1, 1) +  # верх-лево
            np.roll(np.roll(pred_mask, 1, 0), -1, 1) + # верх-право
            np.roll(np.roll(pred_mask, -1, 0), 1, 1) + # низ-лево
            np.roll(np.roll(pred_mask, -1, 0), -1, 1) +# низ-право
            np.roll(pred_mask, 1, 0) +                 # вверх
            np.roll(pred_mask, -1, 0) +                # вниз
            np.roll(pred_mask, 1, 1) +                 # влево
            np.roll(pred_mask, -1, 1)                  # вправо
        )
        
        plant_birth = (grid == 0) & (herb_neighbours <= 4) & (plant_neighbours > 0)
        herb_birth = (plant_neighbours >= 4) & (herb_neighbours >= 2)
        pred_birth = (pred_neighbours == 2) & (herb_neighbours > 0)
        
        plant_survive = (grid == 1) & (herb_neighbours <= 4) 
        herb_survive = (grid == 2) & (pred_neighbours == 0) & (plant_neighbours > 0)
        pred_survive = (grid == 3) & (herb_neighbours > 0) & (pred_neighbours == 1)
        
        new_grid = np.zeros_like(grid)
        new_grid[plant_birth] = 1
        new_grid[plant_survive] = 1
        new_grid[herb_birth] = 2
        new_grid[herb_survive] = 2
        new_grid[pred_birth] = 3
        new_grid[pred_survive] = 3
        
        return new_grid