#!/usr/bin/python3

"""
    Program: LCD1602 Demo (lcd-hello.py)
    Author:  M. Heidenreich, (c) 2020

    Description:

    This code is provided in support of the following YouTube tutorial:
    https://youtu.be/DHbLBTRpTWM

    This example shows how to use the LCD1602 I2C display with Raspberry Pi.

    THIS SOFTWARE AND LINKED VIDEO TOTORIAL ARE PROVIDED "AS IS" AND THE
    AUTHOR DISCLAIMS ALL WARRANTIES INCLUDING ALL IMPLIED WARRANTIES OF
    MERCHANTABILITY AND FITNESS. IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR
    ANY SPECIAL, DIRECT, INDIRECT, OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES
    WHATSOEVER RESULTING FROM LOSS OF USE, DATA OR PROFITS, WHETHER IN AN
    ACTION OF CONTRACT, NEGLIGENCE OR OTHER TORTIOUS ACTION, ARISING OUT OF
    OR IN CONNECTION WITH THE USE OR PERFORMANCE OF THIS SOFTWARE.
"""

from signal import signal, SIGTERM, SIGHUP, pause
from rpi_lcd import LCD
import RPi.GPIO as GPIO
from time import sleep

class LCDRasp:
    def __init__(self):
            self.BUTTON_PIN_SELEC = 24
            self.BUTTON_PIN_CHANGE = 23
            self.lcd = LCD()
            GPIO.setmode(GPIO.BCM)
            GPIO.setup(self.BUTTON_PIN_SELEC, GPIO.IN, pull_up_down=GPIO.PUD_UP)
            GPIO.setup(self.BUTTON_PIN_CHANGE, GPIO.IN, pull_up_down=GPIO.PUD_UP)

    def safe_exit(signum, frame):
        exit(1)

    def escolhe_simbolo(self):
        signal(SIGTERM, LCDRasp.safe_exit)
        signal(SIGHUP, LCDRasp.safe_exit)

        self.lcd.clear()
        self.lcd.text("Change    Select", 2)
        self.lcd.text("->X    O", 1)
        escolha = 'X'
        confirma = True

        while confirma:
            while escolha == 'X' and confirma:
                self.lcd.text("->X    O", 1)
                entrada = GPIO.input(self.BUTTON_PIN_CHANGE)
                entrada_2 = GPIO.input(self.BUTTON_PIN_SELEC)
                if entrada == GPIO.LOW:
                    escolha = 'O'
                    sleep(0.1)
                if entrada_2 == GPIO.LOW:
                    confirma = False

            while escolha == 'O' and confirma:
                self.lcd.text("  X  ->O", 1)
                entrada = GPIO.input(self.BUTTON_PIN_CHANGE)
                entrada_2 = GPIO.input(self.BUTTON_PIN_SELEC)
                if entrada == GPIO.LOW:
                    escolha = 'X'
                    sleep(0.1)
                if entrada_2 == GPIO.LOW:
                    confirma = False

        #self.lcd.text("Jogador escolheu:",1)
        #self.lcd.text(f"{escolha}",2)
        ##pause()
        return escolha

    def espera_apertar_botao(self):
        while True:
            if GPIO.input(self.BUTTON_PIN_SELEC) == GPIO.LOW or GPIO.input(self.BUTTON_PIN_CHANGE) == GPIO.LOW:
                sleep(0.1)
                break



    def escolhe_dificuldade(self):
        signal(SIGTERM, LCDRasp.safe_exit)
        signal(SIGHUP, LCDRasp.safe_exit)
        self.lcd.clear()
        self.lcd.text(">FAC  MED  DIF", 1)
        self.lcd.text("Change    Select", 2)
        escolha = "Facil"
        confirma = True

        while confirma:
            while escolha == "Facil" and confirma:
                self.lcd.text(">FAC  MED  DIF", 1)
                #sleep(0.25)
                #lcd.text("     O", 2)
                entrada = GPIO.input(self.BUTTON_PIN_CHANGE)
                entrada_2 = GPIO.input(self.BUTTON_PIN_SELEC)
                if entrada == GPIO.LOW:
                    escolha = 'Medio'
                if entrada_2 == GPIO.LOW:
                    confirma = False
                #if input() == 's':
                #    valor += 1
                #if input() == 'c':
                #    confirma = False

            while escolha == 'Medio' and confirma:
                self.lcd.text(" FAC >MED  DIF", 1)
                #sleep(0.25)
                #lcd.text("X     ", 2)
                entrada = GPIO.input(self.BUTTON_PIN_CHANGE)
                entrada_2 = GPIO.input(self.BUTTON_PIN_SELEC)
                if entrada == GPIO.LOW:
                    escolha = 'Dificil'
                if entrada_2 == GPIO.LOW:
                    confirma = False

            while escolha == 'Dificil' and confirma:
                self.lcd.text(" FAC  MED >DIF", 1)
                entrada = GPIO.input(self.BUTTON_PIN_CHANGE)
                entrada_2 = GPIO.input(self.BUTTON_PIN_SELEC)
                if entrada == GPIO.LOW:
                    escolha = 'Facil'
                if entrada_2 == GPIO.LOW:
                    confirma = False

       # self.lcd.text("Jogador escolheu:",1)
        #self.lcd.text(f"{escolha}",2)
        #pause()
        return escolha

    def mensagem_desenhando_tabuleiro(self):
        signal(SIGTERM, LCDRasp.safe_exit)
        signal(SIGHUP, LCDRasp.safe_exit)
        self.lcd.clear()
        self.lcd.text("Desenhando", 1)
        self.lcd.text("Tabuleiro...", 2)
        #pause()

    def mensagem_vez_jogador(self):
        signal(SIGTERM, LCDRasp.safe_exit)
        signal(SIGHUP, LCDRasp.safe_exit)
        self.lcd.clear()
        self.lcd.text("Vez do Jogador", 1)
        self.lcd.text("", 2)
        #pause()

    def mensagem_vez_robo(self):
        signal(SIGTERM, LCDRasp.safe_exit)
        signal(SIGHUP, LCDRasp.safe_exit)
        self.lcd.clear()
        self.lcd.text("Vez do Robo", 1)
        self.lcd.text("", 2)
        #pause()

    def calculando_jogada_robo(self):
        signal(SIGTERM, LCDRasp.safe_exit)
        signal(SIGHUP, LCDRasp.safe_exit)
        self.lcd.clear()
        self.lcd.text("Calculando prox", 1)
        self.lcd.text("Jogada", 2)
        #pause()

    def mensagem_jogar_novamente(self):
        self.lcd.clear()
        self.lcd.text("Apague tudo", 1)
        self.lcd.text("e aperte algo!",2)
        while True:
            if GPIO.input(self.BUTTON_PIN_CHANGE) == GPIO.LOW or GPIO.input(self.BUTTON_PIN_SELEC) == GPIO.LOW:
                self.lcd.text("Jogar novamente?", 1)
                self.lcd.text(" Sim        Nao ", 2) # change = sim  selec = nao
                while True:
                    if GPIO.input(self.BUTTON_PIN_CHANGE) == GPIO.LOW: #Sim
                        return True
                    if GPIO.input(self.BUTTON_PIN_SELEC) == GPIO.LOW: #Nao
                        self.lcd.clear()
                        self.lcd.text("Jah eh", 1)
                        sleep(3)
                        self.lcd.clear()
                        return False

    def mensagem_vencedor(self, vencedor):
        signal(SIGTERM, LCDRasp.safe_exit)
        signal(SIGHUP, LCDRasp.safe_exit)
        self.lcd.clear()
        self.lcd.text("Vencedor: ", 1 )
        if vencedor ==1:
            self.lcd.text("Jogador", 2)
        elif vencedor ==2:
            self.lcd.text("Robo", 2)
        else:
            self.lcd.text("Deu velha", 1)
        sleep(6) #6
        return self.mensagem_jogar_novamente()



    def mensagem_redesenha_tabuleiro(self):
        signal(SIGTERM, LCDRasp.safe_exit)
        signal(SIGHUP, LCDRasp.safe_exit)
        self.lcd.clear()
        self.lcd.text("Aperte para", 1 )
        self.lcd.text("Redesenhar", 2)
        while True:
            if GPIO.input(self.BUTTON_PIN_SELEC) == GPIO.LOW or GPIO.input(self.BUTTON_PIN_CHANGE) == GPIO.LOW:
                sleep(0.1)
                break

    def mensagem_enquadramento_tabuleiro(self):
        signal(SIGTERM, LCDRasp.safe_exit)
        signal(SIGHUP, LCDRasp.safe_exit)
        self.lcd.clear()
        self.lcd.text("Enquadra melhor", 1 )
        while True:
            entrada = GPIO.input(self.BUTTON_PIN_SELEC)
            if entrada == GPIO.LOW:
                sleep(0.1)
                break

    def mensagem_jogada_invalida(self):
        signal(SIGTERM, LCDRasp.safe_exit)
        signal(SIGHUP, LCDRasp.safe_exit)
        self.lcd.text("Jogada invalida", 1 )
        self.lcd.text("Desenhe dnv", 2)
#obj = LCDRasp()
#obj.escolhe_dificuldade()