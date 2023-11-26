import serial
import time

serial_port = '/dev/ttyACM0'
#serial_port = 'COM3'
baud_rate = 9600 

class Arduino:
    def __init__(self):
        self.serial = serial.Serial(serial_port, baud_rate)
        self.recebe_ack()

    def desenha_jogo_da_velha(self):
        self.serial.write('v'.encode())
        self.recebe_ack()

    def movimenta(self,posicao):
        self.serial.write(posicao.encode())
        self.recebe_ack()

    def desenha_simbolo(self,simbolo):
        self.serial.write(simbolo.encode())
        self.recebe_ack()
      
    def volta_posicao_inicial(self):
        self.serial.write('i'.encode())
        self.recebe_ack()

    def desenhar_linha_vencedor(self,eixo):
        self.serial.write('d'.encode())
        self.recebe_ack()

        self.serial.write(eixo.encode())
        self.recebe_ack()

    def recebe_ack(self):
        while True:
            received_data = self.serial.read(1).decode('utf-8')
            if received_data == 'a':
                break

