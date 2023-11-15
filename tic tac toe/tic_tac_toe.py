import os
from player import Player
from bot import Bot
from copy import deepcopy

class Board:
    def __init__(self,board):
        self.board = board
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

        self.board_mapping_1D_to_2D = {
            0:'0,0',
            1:'0,1',
            2:'0,2',
            3:'1,0',
            4:'1,1',
            5:'1,2',
            6:'2,0',
            7:'2,1',
            8:'2,2',
        }
    def get_boolean_board(self):
        return [True if position != ' ' else False for position in self.board]
    
    def print_board(self):
        os.system('cls')
        print('-'*10)
        for i in range(3):
            print(self.board[3*i] + ' ' + self.board[3*i+1] + ' ' + self.board[3*i+2])
        print('-'*10)
    
    def get_symbol_at_position(self,position):
        if isinstance(position,str):
            if position not in self.board_mapping_2D_to_1D.keys():
                return None
            return self.board[self.board_mapping_2D_to_1D[position]]
        elif isinstance(position,int):
            if position < 0 or position > 8:
                return None
            return self.board[position]
    def set_symbol_at_position(self,position,symbol):
        if isinstance(position,str):
            if position not in self.board_mapping_2D_to_1D.keys():
                return None
            self.board[self.board_mapping_2D_to_1D[position]] = symbol
        elif isinstance(position,int):
            if position >= 0 and position <= 8:
                self.board[position] = symbol

    def check_draw(self):
        return ' ' not in self.board 
    
    def check_winner(self):
        for i in range(3):
            if self.board[i*3] != ' ' and self.board[i*3] == self.board[i*3+1] and self.board[i*3+1] == self.board[i*3+2]:
                return self.board[i*3]
            elif self.board[i+3*0] != ' ' and self.board[i+3*0] == self.board[i+3*1] and self.board[i+3*1] == self.board[i+3*2]:
                return self.board[i+3*0]
            
        if self.board[0] != ' ' and self.board[0] == self.board[4] and self.board[4] == self.board[8]:
            return self.board[0]
        elif self.board[2] != ' ' and self.board[2] == self.board[4] and self.board[4] == self.board[6]:
            return self.board[2]
        return ' '
    
    def check_valid_play(self,position):
        try:
            if self.get_symbol_at_position(position) == ' ':
                return True
            return False
        except:
            return False

    def count_empty_positions(self):
        return self.board.count(' ')
    
    def generate_possible_moves(self,symbol):
        boards = []
        for index,value in enumerate(self.board):
            if value == ' ':
                new_board = deepcopy(self.board)
                new_board[index] = symbol
                boards.append((Board(new_board),self.board_mapping_1D_to_2D[index]))
        return boards
    
class tic_tac_toe:
    def __init__(self,player1,player2):
        self.player1 = player1
        self.player2 = player2
        self.turn = 0 
        self.board = Board([' ' for _ in range(9)])
    
    def get_board(self):
        return self.board

    def play(self):
        while True:
            positionX = self.player1.play() 

            while not self.board.check_valid_play(positionX):
                positionX = self.player1.play()
            self.board.set_symbol_at_position(positionX,'x')
            self.board.print_board()

            if self.board.check_winner() == 'x':
                return 'x'
            
            elif self.board.check_draw():
                return 'draw'
            
            positionO = self.player2.play()

            while not self.board.check_valid_play(positionO):
                positionO = self.player2.play()
            self.board.set_symbol_at_position(positionO,'o')
            self.board.print_board()

            if self.board.check_winner() == 'o':
                return 'o'

if __name__ == '__main__':
    while True:
        _= input("Desenhe o tabuleiro")

        player1 = Player()
        player2 = Bot(symbol = 'o')

        ttc = tic_tac_toe(player1,player2)
        player1.set_board(ttc.get_board())
        player2.set_board(ttc.get_board())

        winner = ttc.play()

        if winner == 'draw':
            print("Draw")
        elif winner == 'x':
            print("X wins!")
        elif winner == 'o':
            print("O wins!")

        