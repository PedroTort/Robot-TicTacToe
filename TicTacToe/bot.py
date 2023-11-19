import random
from arduino import Arduino

class Bot:
    def __init__(self,arduino:Arduino,symbol = 'o',level = 'hard'):
        self.board = 'o'
        self.symbol = symbol
        self.opponents_symbol = 'x' if symbol == 'o' else 'x'   
        self.arduino = arduino
        self.dict_level_depth = {
            'easy': None,
            'medium':1,
            'hard': 15
        }

        self.depth = self.dict_level_depth[level]
        self.board_mapping_2D_to_1D = {
            '0,0':0,
            '0,1':1,
            '0,2':2,
            '1,0':3,
            '1,1':4,
            '1,2':5,
            '2,0':6,
            '2,1':7,
            '2,2':8,
        }
        
    def set_board(self,board):
        self.board = board

    def play(self):
        position2D = self.min_max(self.board,0,self.depth)[1]

        position1D = self.board_mapping_2D_to_1D[position2D]
        self.arduino.movimenta(str(position1D))
    
        self.arduino.desenha_simbolo(self.symbol)
        self.arduino.volta_posicao_inicial()
        return position2D

    #turn = 0 -> bot`s turn
    #turn = 1 -> player`s turn
    def min_max(self,board,turn,depth):
        symbol = self.symbol if turn == 0 else self.opponents_symbol
        possible_boards = board.generate_possible_moves(symbol)
        weight = board.count_empty_positions() + 1
        multiplier = 1 if turn == 0 else -1
        evals = [[multiplier*weight,new_board[1]] if new_board[0].check_winner() == symbol else [0,new_board[1]] for new_board in possible_boards]
        
        if depth is not None:
            depth -= 1

        if depth is None or depth >=0:
            for index,tuple in enumerate(evals):
                if tuple[0] == 0 and possible_boards[index][0].count_empty_positions()>0:
                    tuple[0] = self.min_max(possible_boards[index][0],int(not turn),depth)[0]

        if turn == 0:
            if depth is None:
                value =  min(evals, key=lambda x: x[0])[0]
            value =  max(evals, key=lambda x: x[0])[0]
        else:
            if depth is None:
                value =  max(evals, key=lambda x: x[0])[0]
            value =  min(evals, key=lambda x: x[0])[0]
        
        values_tuples = [t for t in evals if t[0] == value]
        return random.choice(values_tuples)

        