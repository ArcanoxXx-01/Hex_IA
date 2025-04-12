import time
from base import HexBoard
from utils import *
from queue import Queue

# win # 
pesos ={
    'bridges': 100,         #Crear un puente
    'close_bridge':200,    #Cerrar un puente que el oponente intenta bloquear
    'center':5,           #Casillas centrales
    'complete_road':100,   #Completar camino
    'win': 100000,           #Movimiento ganador
    'block_enemy': 100,     #Bloquear jugada enemiga
    'close_border': 1,    #Acercar a los bordes que quiere unir
    "neighbor": 1000,       # Vecinos cerca
    "dsu": 2,
}

BRIDGE_PATTERNS = (
    ((-2,1),(-1,0),(-1,1)),
    ((-1,2),(-1,1),(0,1)),
    ((1,1),(0,1),(1,0)),
    ((2,-1),(1,0),(1,-1)),
    ((-1,-1),(0,-1),(-1,0)),
    ((1,-2),(1,-1),(0,-1)),
)

BRIDGE_CONECTED = [
    ((0,1),(-1,0)),
    ((1,0),(-1,1)),
    ((-1,1),(0,-1)),
    ((-1,0),(1,-1)),
    ((0,-1),(1,0)),
    ((1,-1),(0,1))
]


def h(state: HexBoard, move, id)->int:

    result = 1
    result+= pesos['bridges'] * bridges(state, move, id)
    result+= pesos['close_bridge'] if close_bridge(state.board, move, id) else 0
    result+= pesos['center'] * center(state, move)
    result+= pesos['complete_road'] if complete_road(state, move) else 0
    result+= pesos['win'] if state.check_connection(id) else 0
    result+= pesos['block_enemy'] if block_enemy_bridge(state, move, id) else 0
    result-= pesos['neighbor'] if neighbor(state, move, id)>=3 else 0
    result += pesos['dsu']*calculate(state, move, id)
    return result

def bridges(state: HexBoard, move, id: int) -> float:
    """
    Verifica si la posición (row, col) forma un puente con otra casilla del jugador.
    """
    #posibles patrones de puente
    x,y = move
    for (pr1, pc1), (vr1, vc1), (vr2, vc2) in BRIDGE_PATTERNS:
        if valid(len(state.board[0]),(x+pr1,y+pc1)) and state.board[x+pr1][y+pc1]==id and state.board[x+vr1][y+vc1]==0 and state.board[x+vr2][y+vc2]==0:
            return 1
    return 0   

def close_bridge(board, move, id)->bool:
    x, y = move
    for ((r1,c1),(r2,c2)) in BRIDGE_CONECTED:
        if valid(len(board[0]),(x+r1,y+c1)) and valid(len(board[0]),(x+r2,y+c2)) and board[x+r1][y+c1] == board[x+r2][y+c2] == id and board[x+r1+r2][y+c1+c2] == 3 - id:
            return True
    return False    

def complete_road(state:HexBoard, move)->bool:
    x, y = move
    for ((r1,c1),(r2,c2)) in BRIDGE_CONECTED:
        if valid(state.size,(x+r1,y+c1)) and valid(state.size,(x+r2,y+c2)) and state.board[x+r1][y+c1] == state.board[x+r2][y+c2] == id and state.board[x+r1+r2][y+c1+c2] == 0:
           return True
    return False

def center(state:HexBoard, move)->int:
    return state.size - abs(state.size//2 - move[0]) - abs(state.size//2 - move[1])

def close_border(state:HexBoard, move, id)->int:
    if id == 1:
        return max(move[0],state.size - move[0])
    return max(move[1],state.size - move[1])
        

def block_enemy_bridge(state:HexBoard, move, id)->bool:
    x, y = move
    for ((r1,c1),(r2,c2)) in BRIDGE_CONECTED:
        if valid(state.size,(x+r1,y+c1)) and valid(state.size,(x+r2,y+c2)) and state.board[x+r1][y+c1] == state.board[x+r2][y+c2] == 3-id and state.board[x+r1+r2][y+c1+c2] != 3 - id:
            return True
    return False    

def neighbor(state: HexBoard, move, id):
    x , y = move
    directions = [(-1,0), (-1,1), (0,-1), (0,1), (1,-1), (1,0)]
    count=0
    for (i, j) in directions:
        if valid(state.size, (x+i, y+j)) and state.board[x+i][y+j] == 3-id :
            count+=1
    return count   

    
def calculate(state: HexBoard, move, id):
    dsu= DSU(state.size)
    cells = state.player_positions[id]
    directions = [(-1,0), (-1,1), (0,-1), (0,1), (1,-1), (1,0)]        

    for cell in cells:
        if cell!= move:
            x , y = cell
            for (i, j) in directions:
                if (x+i, y+j)!= move and valid(state.size, (x+i, y+j)) and state.board[x+i][y+j] == id :
                    dsu.union(x*state.size+y, (x+i)*state.size + y+ j)
    val = 0
    x, y = move
    for (i, j) in directions:
        for (k, r) in directions:
            if valid(state.size, (x+i, y+j)) and valid(state.size, (x+k, y+r)) and state.board[x+i][y+j] == state.board[x+k][y+r]==id :  
                u, v = dsu.get((x+k)*state.size+y+r) , dsu.get((x+i)*state.size + y+ j)
                if u != v :
                    z = dsu.func(u,v) 
                    w = 0
                    if id == 1:
                        w = min(move[0],z[0]) + state.size - max(move[0], z[2])
                    else:
                        w = min(move[1],z[1]) + state.size - max(move[1], z[3])               
                    return (dsu.size[u] + dsu.size[v])*(state.size - w) + val
                else :val-= 20

    return val


def bfs(state: HexBoard, move, id, flag: bool):
    root = state.size*state.size
    adj = [[] for _ in range(state.size*state.size+1)]
    dp = [0 for _ in range (state.size*state.size+1)]
    dp[root] = 1
    visit= ["White" for _ in range(state.size*state.size+1)]
    directions = [(-1,0), (-1,1), (0,-1), (0,1), (1,-1), (1,0)]  
    for x in range(state.size):
        for y in range(state.size):
            k = x * state.size + y
            for (i,j) in directions:
                if valid(state.size, (x+i, y+j)) and state.board[x+i][y+j] != 3-id:
                    adj[k].append((x+i)*state.size+y+j)  

    que= Queue()
    que.put(root)

    if flag:
        if id==1:
            for i in range(state.size):
                adj[root].append(i)
        else:
            for i in range(state.size):
                adj[root].append(i * state.size)

    else:
        if id==1:
            for i in range(state.size):
                adj[root].append(state.size * (state.size-1) + i)
        else:
            for i in range(state.size):
                adj[root].append(i*state.size + state.size - 1)    

    while(not que.empty()):
        u = que.get()
        if u == move[0] * state.size + move[1]:
            break        
        for v in adj[u]:
            if visit[v] != 'Black':
                dp[v] += dp[u]
            if visit[v] == 'White':
                que.put(v)
                visit[v] = "Gray"
        visit[u] = "Black"   

    return dp[move[0] * state.size + move[1]]

