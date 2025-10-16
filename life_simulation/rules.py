import numpy as np



class BasicRules:
    
    def apply(self, grid: np.ndarray, neighbours: np.ndarray) -> np.ndarray:
        raise NotImplementedError
    


class ConwayRules(BasicRules):
    
    def apply(self, grid: np.ndarray, neighbours: np.ndarray) -> np.ndarray:
        birth = neighbours == 3
        survive = (grid == 1) & ((neighbours == 2) | (neighbours == 3))
        new_grid = (birth | survive).astype(np.uint8)
        return new_grid
    


class RecuxcdRules(BasicRules):
    
    def apply(self, grid: np.ndarray, neighbours: np.ndarray) -> np.ndarray:
        birth = neighbours == 2
        survive = (grid == 1) & ((neighbours == 1) | (neighbours == 4))
        new_grid = (birth | survive).astype(np.uint8)
        return new_grid
        


class HighLifeRules(BasicRules):
    
    def apply(self, grid: np.ndarray, neighbours: np.ndarray) -> np.ndarray:
        birth = (neighbours == 3) | (neighbours == 6)
        survive = (grid == 1) & ((neighbours == 2) | (neighbours == 3))
        new_grid = (birth | survive).astype(np.uint8)
        return new_grid



class ImmortalRules(BasicRules):
    
    def apply(self, grid: np.ndarray, neighbours: np.ndarray) -> np.ndarray:
        birth = (neighbours == 2)
        survive = (grid == 1)
        new_grid = (birth | survive).astype(np.uint8)
        return new_grid