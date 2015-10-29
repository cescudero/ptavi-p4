#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Programa cliente que abre un socket a un servidor
"""

import socket
import sys

try:
    # Cliente UDP simple.

    # Dirección IP del servidor.
    SERVER = sys.argv[1]
    PORT = int(sys.argv[2])
    # Contenido que vamos a enviar
#LINE = sys.argv[3]
    #peticion SIP del cliente
    REGISTER = sys.argv[3].upper()
    #usuario
    USER = sys.argv[4]
    #tiempo de expiracion
    EXPIRES = sys.argv[5]
except IndexError:
    sys.exit('Usage: client.py ip puerto register sip_address expires_value')

# Creamos el socket, lo configuramos y lo atamos a un servidor/puerto
my_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
my_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
my_socket.connect((SERVER, PORT))

if REGISTER == 'REGISTER':
    EXPIRES = ("Expires: " + EXPIRES + '\r\n\r\n') 
    print("Enviando: " + REGISTER + ' ' + USER + '\r\n' + EXPIRES) 
    my_socket.send(bytes(REGISTER + ' ' + USER + ' ', 'utf-8') + b'SIP/2.0\r\n' + bytes(EXPIRES, 'utf-8'))
    data = my_socket.recv(1024)

print('Recibido -- ', data.decode('utf-8'))
print("Terminando socket...")

# Cerramos todo
my_socket.close()
print("Fin.")
