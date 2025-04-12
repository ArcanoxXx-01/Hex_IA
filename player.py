from base import *
from Heuristics import h
from typing import Tuple
from utils import *
import time

class MinMax_Player(Player):
    def __init__(self, player_id):
        super().__init__(player_id)
        self.heuristic_cache = {}
        self.time = time.time()
        # self.mM = MiniMax_AB(player_id)
        
    def play(self, board:HexBoard, time_limit=9.5):
        """  """

        self.time = time.time()
        level = 1

        _ , best_move = self.minMax(board, level, float('-inf'), float('inf'), True,  None)

        return best_move

    def minMax(self, state:HexBoard, current_level:int, alpha, beta, maximizzing, previus_move)-> Tuple[int,Tuple[int,int]]:
        if current_level == 0:
            return self.get_heuristic(state, previus_move)

        current_best_move = None
        current_best_value  = float('-inf') if maximizzing else float('inf')
        player = self.player_id if maximizzing else  3 - self.player_id

        moves = state.get_possible_moves()

        for move in moves:
            child_state = self.change_state(state, move, player)
            current_eval, _ = self.minMax(child_state, current_level-1, alpha, beta, not maximizzing, move)

            if ((beta <= alpha) and maximizzing) or ((beta >= alpha) and not maximizzing):
                break

            if ((current_eval > current_best_value) and maximizzing) or ((current_eval < current_best_value) and not maximizzing):
                current_best_value = current_eval
                current_best_move = move
                if maximizzing: alpha= max(alpha, current_best_value)
                else: beta= min(beta, current_best_value)

        return current_best_value, current_best_move


    def change_state(self, state:HexBoard, move, id):
        new_state = state.clone()
        new_state.place_piece(move[0], move[1], id)
        return new_state

    def get_heuristic(self, state:HexBoard, previus_move)-> Tuple[int,Tuple[int,int]]:
        """ Si esta guardado en memoria lo devuelve, sino lo calcula"""

        hashable_state = tuple(tuple(row) for row in state.board)

        if hashable_state in self.heuristic_cache:
            return self.heuristic_cache[hashable_state], previus_move
        
        value = h(state, previus_move, self.player_id)
        self.heuristic_cache[hashable_state] = value

        return value, previus_move
