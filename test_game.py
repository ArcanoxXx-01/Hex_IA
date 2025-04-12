from base import *
from Random_player import *
from player import *
from My_board import *
import time

board = My_HexBoard(11)
p1 = Random_Player(1)
p2 = MinMax_Player(2)
count = 0
game_over = False
is_p1 = True
games=34
wins=0
lose=0
while(games>=0):
    games-=1
    game_over=False
    board= My_HexBoard(11)
    while not game_over:
        # time.sleep(1.5)
        count += 1
        x , y = p1.play(board)
        board.place_piece(x, y, 1)

        if board.check_connection(1):
            print(f"Gana el jugador {1} en {count} jugadas")
            game_over = True
            lose+=1
            continue

        x , y= p2.play(board, 1)
        board.place_piece(x, y, 2)
        
        if board.check_connection(2):
            print(f"Gana el jugador {2} en {count} jugadas")
            wins+=1
            game_over = True     
        
        is_p1 = not is_p1
        # print(f'{id}, {x}, {y}')
        print(board)

print(f"Player:  {wins}, Random : {lose}")
print(count/35)