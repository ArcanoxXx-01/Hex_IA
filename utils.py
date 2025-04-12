from typing import Tuple
from base import *
import numpy as np

def valid(size: int, cell: tuple[int, int]) -> bool:
  """ 
  Devuelve si la celda es una pocision valida del tablero
  """
  return 0 <= cell[0] < size and 0 <= cell[1] < size


def get_move(original_state, current_state) -> Tuple[int, int]:
    """ 
    Encuentra la diferencia entre dos estados del tablero y devuelve la posición cambiada. 
    """
    size = len(original_state)

    for row in range(size):
        original_row = original_state[row]
        current_row = current_state[row]
        for col in range(size):
            if original_row[col] != current_row[col]:
                return (row, col)
    return (-1, -1)

def oponent(id):
    return 3 - id

def terminal(state:HexBoard) -> bool:
    return True if state.check_connection(1) else True if state.check_connection(2) else False

class DSU:
    def __init__(self, n:int):
        self.s = n*n
        self.parent = list(range(self.s))
        self.size= [1 for _ in range(self.s)]
        self.borders= [[i / n, i % n, i / n, i % n] for i in range(self.s)]

    def get(self, u: int):
        return u if self.parent[u]==u else self.get(self.parent[u])   
    
    def union(self, u: int, v: int):
        u = self.get(u)
        v = self.get(v)
        if self.size[u]>self.size[v]:
            u, v = v, u
        self.parent[u] = v
        self.size[v]+= self.size[u]     
        x1, y1, z1, w1 = self.borders[v]
        x2, y2, z2, w2 = self.borders[u]
        self.borders[v]= [min(x1,x2), min(y1,y2), max(z1,z2), max(w1,w2)]

    def func(self, u: int, v: int):
        u = self.get(u)
        v = self.get(v)
        if self.size[u] > self.size[v]:
            u, v = v, u
        x1, y1, z1, w1 = self.borders[v]
        x2, y2, z2, w2 = self.borders[u]
        return [min(x1,x2), min(y1,y2), max(z1,z2), max(w1,w2)]