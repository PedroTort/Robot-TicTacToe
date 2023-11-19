import time
from funcoes_aux import *

class Player:
    def set_board(self,board):
        self.board = board
        self.imagem_tabuleiro_vazio = tira_foto_tabuleiro_vazio()
        cv2.imwrite("imagem_tabuleiro_vazio_processado.jpg", self.imagem_tabuleiro_vazio)
        self.lista_quadrados = encontra_quadrados(self.imagem_tabuleiro_vazio)
    def play(self):
        
        posicao = detecta_jogada(self.imagem_tabuleiro_vazio,self.lista_quadrados,self.board.get_boolean_board(),'x')
        while posicao is None:
            print("Faça uma jogada válida!!!")
            posicao = detecta_jogada(self.imagem_tabuleiro_vazio,self.lista_quadrados,self.board.get_boolean_board(),'x')
        return posicao

    