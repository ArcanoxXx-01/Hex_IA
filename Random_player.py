from base import *
from typing import Tuple
import random

class Random_Player(Player):
    """ Jugador Random :) """
    def play(self, board: HexBoard) -> Tuple[int, int]:
        return random.choice(list(board.get_possible_moves()))