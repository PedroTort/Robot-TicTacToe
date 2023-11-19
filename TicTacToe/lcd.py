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

BUTTON_PIN = 12
lcd = LCD()
GPIO.setmode(GPIO.BCM)
GPIO.setup(BUTTON_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)

def safe_exit(signum, frame):
    exit(1)

def escolhe_simbolo():
    signal(SIGTERM, safe_exit)
    signal(SIGHUP, safe_exit)
     
    lcd.clear()
    lcd.text("Escolha:", 1)
    lcd.text("->X    O", 2) 
    escolha = 'X'
    confirma = True
    
    while confirma: 
        while escolha == 'X' and confirma:
            lcd.text("->X    O", 2) 
            entrada = GPIO.input(BUTTON_PIN)
            if entrada == GPIO.LOW:
                escolha = 'O'
                sleep(0.1)
            elif entrada == 'c':
                confirma = False

        while escolha == 'O' and confirma:
            lcd.text("  X  ->O", 2) 
            entrada = GPIO.input(BUTTON_PIN)
            if entrada == GPIO.LOW:
                escolha = 'X'
                sleep(0.1)
            elif entrada == 'c':
                confirma = False
        
    #lcd.text("Jogador escolheu:",1)
    #lcd.text(f"{escolha}",2)
    pause()
    return escolha

def escolhe_dificuldade():
    signal(SIGTERM, safe_exit)
    signal(SIGHUP, safe_exit)
    lcd.clear()    
    lcd.text("Escolha:", 1)
    lcd.text(">FAC  MED  DIF", 2) 
    escolha = "Facil"
    confirma = True
    
    while confirma: 
        while escolha == "Facil" and confirma:
            lcd.text(">FAC  MED  DIF", 2) 
            #sleep(0.25)
            #lcd.text("     O", 2)
            entrada = input()
            if entrada == 's':
                escolha = 'Medio'
            elif entrada == 'c':
                confirma = False
            #if input() == 's':
            #    valor += 1
            #if input() == 'c':
            #    confirma = False

        while escolha == 'Medio' and confirma:
            lcd.text(" FAC >MED  DIF", 2) 
            #sleep(0.25)
            #lcd.text("X     ", 2)
            entrada = input()
            if entrada == 's':
                escolha = 'Dificil'
            elif entrada == 'c':
                confirma = False
                
        while escolha == 'Dificil' and confirma:
            lcd.text(" FAC  MED >DIF", 2) 
            #sleep(0.25)
            #lcd.text("X     ", 2)
            entrada = input()
            if entrada == 's':
                escolha = 'Facil'
            elif entrada == 'c':
                confirma = False
        
    #lcd.text("Jogador escolheu:",1)
    #lcd.text(f"{escolha}",2)
    pause()
    return escolha
    
def mensagem_desenhando_tabuleiro():
    signal(SIGTERM, safe_exit)
    signal(SIGHUP, safe_exit)
    lcd.clear()    
    lcd.text("Desenhando", 1)
    lcd.text("Tabuleiro...", 2) 
    pause()

def mensagem_vez_jogador():
    signal(SIGTERM, safe_exit)
    signal(SIGHUP, safe_exit)
    lcd.clear()    
    lcd.text("Vez do Jogador", 1)
    lcd.text("", 2) 
    pause()

def mensagem_vez_robo():
    signal(SIGTERM, safe_exit)
    signal(SIGHUP, safe_exit)
    lcd.clear()
    lcd.text("Vez do Robo", 1)
    lcd.text("", 2) 
    pause()

def mensagem_vencedor(vencedor):
    signal(SIGTERM, safe_exit)
    signal(SIGHUP, safe_exit)        
    lcd.clear()    
    lcd.text("Vencedor: ", 1 )
    if vencedor ==1:
        lcd.text("Jogador", 2)
    elif vencedor ==2:
        lcd.text("Robo", 2)
    else:
        lcd.text("Deu velha", 1)
    pause()


escolhe_simbolo()
