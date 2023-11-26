import time
from funcoes_aux import *
from lcd import LCDRasp

class Player:
    def __init__(self,tabuleiro_vazio, quadro_vazio, cap, symbol = 'x'):
        self.player_class = 'player'
        self.symbol = symbol
        self.lista_quadrados = None
        self.cap = cap
        self.tabuleiro_vazio = tabuleiro_vazio
        self.quadro_vazio = quadro_vazio

    def set_board(self,board):
        self.board = board
        
    def cria_quadrados(self):
        self.imagem_tabuleiro_vazio = processa_tabuleiro_vazio(self.cap, self.tabuleiro_vazio, self.quadro_vazio)
        # cv2.imwrite("imagem_tabuleiro_vazio_processado.jpg", self.imagem_tabuleiro_vazio)
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
        lcd = LCDRasp() # modo feio de fazer
        lcd.mensagem_vez_jogador() # modo feio de fazer
        posicao = detecta_jogada(self.imagem_tabuleiro_vazio,self.lista_quadrados,self.board.get_boolean_board(),self.symbol, self.cap)
        while posicao is None:
            lcd.mensagem_jogada_invalida()
            posicao = detecta_jogada(self.imagem_tabuleiro_vazio,self.lista_quadrados,self.board.get_boolean_board(),self.symbol, self.cap)
        return posicao

    
