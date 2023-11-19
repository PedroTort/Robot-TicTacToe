from time import sleep
import os

class LCDRasp_sim:                        
    
    def safe_exit(signum, frame):
        exit(1)

    def escolhe_simbolo(self):
        os.system('cls')
        simbolo = input('Escolha:')
        while simbolo != 'X' and simbolo != 'O': 
            os.system('cls')
            simbolo = input('Escolha:')
        return simbolo
    
    def espera_apertar_botao(self):
        _ = input()
           
    def escolhe_dificuldade(self):
        os.system('cls')
        escolha = input('Dificuldade:')
        while escolha != 'Facil' and escolha != 'Medio' and escolha != 'Dificil': 
            os.system('cls')
            escolha = input('Dificuldade:')
        return escolha
        
    def mensagem_desenhando_tabuleiro(self):
        os.system('cls')
        print("Desenhando Tabuleiro\n")

    def mensagem_vez_jogador(self):
        os.system('cls')
        print("Vez do Jogador")
      
    def mensagem_vez_robo(self):
        os.system('cls')
        print("Vez do Robo")

    def mensagem_vencedor(self, vencedor):
        os.system('cls')
        print("Vencedor:\n")
        if vencedor ==1:
            print("Jogador")
        elif vencedor ==2:
            print("Robo")
        else:
            print("Deu velha")

    #TODOOOOOOO
    def mensagem_redesenha_tabuleiro(self):
        os.system('cls')
        print("Redesenhar o Quadro!!!")
        _ = input()
    
    #TODOOOOOOO
    def mensagem_enquadramento_tabuleiro(self):
        os.system('cls')
        print("Melhore o enquadramento!!!")
        _ = input()