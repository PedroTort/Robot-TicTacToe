import time
from funcoes_aux import *

class Player:
    def __init__(self,symbol = 'x'):
        self.player_class = 'player'
        self.symbol = symbol

    def set_board(self,board):
        self.board = board
        
    def cria_quadrados(self):
        self.imagem_tabuleiro_vazio = tira_foto_tabuleiro_vazio()
        cv2.imwrite("imagem_tabuleiro_vazio_processado.jpg", self.imagem_tabuleiro_vazio)
        try:
            self.lista_quadrados = encontra_quadrados(self.imagem_tabuleiro_vazio)
        except:
            return False
        return True
    
    def testa_qualidade_tabuleiro(self):
        if(testa_qualidade_tabuleiro(self.lista_quadrados)):
            return True
        return False

    def testa_enquadramento_tabuleiro(self):
        if(testa_posicionamento_tabuleiro(self.imagem_tabuleiro_vazio,self.lista_quadrados)):
            return True
        return False
    
    def play(self):
        
        posicao = detecta_jogada(self.imagem_tabuleiro_vazio,self.lista_quadrados,self.board.get_boolean_board(),self.symbol)
        while posicao is None:
            print("Faça uma jogada válida!!!")
            posicao = detecta_jogada(self.imagem_tabuleiro_vazio,self.lista_quadrados,self.board.get_boolean_board(),self.symbol)
        return posicao

    