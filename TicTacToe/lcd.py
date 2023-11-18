#Programa: Display LCD I2C com Raspberry Pi
#Autor: Arduino e Cia

import i2c_lcd_driver
import socket
import fcntl
import struct
import time

lcdi2c = i2c_lcd_driver.lcd()

#Exibe informacoes iniciais
lcdi2c.lcd_display_string("Fabio 50 braço", 1,1)
lcdi2c.lcd_display_string("Fuku mito", 2,1)
time.sleep(4)

#Apaga o display
lcdi2c.lcd_clear()

def get_ip_address(ifname):
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    return socket.inet_ntoa(fcntl.ioctl(
        s.fileno(),
        0x8915, 
        struct.pack('256s', ifname[:15])
    )[20:24])

#Mostra o endereco IP
lcdi2c.lcd_display_string("IP", 1)
lcdi2c.lcd_display_string(get_ip_address('wlan0'), 1,3)
 
while True:
#Mostra a data no display
    lcdi2c.lcd_display_string("Data: %s" %time.strftime("%d/%m/%y"), 2,1)