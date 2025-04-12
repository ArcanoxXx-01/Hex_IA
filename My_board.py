import random
from base import HexBoard
from copy import deepcopy
import numpy as np

class My_HexBoard(HexBoard):
    def __init__(self, size):
        super().__init__(size)
        # self.terminal = 1 if self.check_connection(1) else 2 if self.check_connection(2) else 0

    def clone(self) -> 'My_HexBoard':
        new_board= deepcopy(self)
        return new_board

    def place_piece(self, row: int, col: int, player_id: int) -> bool:
        if self.board[row][col] == 0:
            self.board[row][col] = player_id
            self.player_positions[player_id].add((row,col))
            return True
        return False

    def get_possible_moves(self) -> list:
        result = [(row, col) for row in range(self.size) for col in range(self.size) if self.board[row][col] == 0]
        random.shuffle(result)
        return result

    def check_connection(self, player_id: int) -> bool:
        visited = set()
        target = self.size - 1
        
        def dfs(row, col):
            if (row, col) in visited:
                return False
            visited.add((row, col))
            
            if player_id == 1 and row == target:
                return True
            if player_id == 2 and col == target:
                return True
            
            directions = [(-1,0), (-1,1), (0,-1), (0,1), (1,-1), (1,0)]
            for dr, dc in directions:
                nr, nc = row + dr, col + dc
                if 0 <= nr < self.size and 0 <= nc < self.size:
                    if self.board[nr][nc] == player_id and (nr, nc) not in visited:
                        if dfs(nr, nc):
                            return True
            return False
        
        if player_id == 1:
            return any(dfs(0, j) for j in range(self.size) if self.board[0][j] == 1)
        else:
            return any(dfs(i, 0) for i in range(self.size) if self.board[i][0] == 2)

    def __str__(self) -> str:
        """ Representacion del tablero para debuguear """
        symbols = {0: '. ', 1: '⬡ ', 2: '⬢ '}
        output = []     
        for i in range(self.size):
            output.append(" "*i)
            for j in range(self.size):
                output.append(symbols[self.board[i][j]])
            output.append("\n")
        return "".join(output)