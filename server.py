#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Clase (y programa principal) para un servidor de eco en UDP simple
"""

import socketserver
import sys

class SIPRegisterHandler(socketserver.DatagramRequestHandler):
    """
    Echo server class
    """
    
    Dicc={}
    
    def handle(self):
        line = self.rfile.read()
        linea = line.decode('utf_8')
        ip = self.client_address[0]
        registro = linea.split()[0]
        direccionSIP = linea.split()[1]
        expires = int(linea.split()[4])
        # Escribe dirección y puerto del cliente (de tupla client_address)
        self.wfile.write(b"SIP/2.0 200 OK\r\n\r\n")
        while 1:
            # Leyendo línea a línea lo que nos envía el cliente
            print("El cliente nos manda " + line.decode('utf-8'))
            self.Dicc[direccionSIP]= ip
            if expires == 0:
                Dicc.pop(direccionSIP)

            # Si no hay más líneas salimos del bucle infinito
            if not line or len(linea):
                break
                

        print (self.dicc)
        print (expires)

if __name__ == "__main__":
    # Creamos servidor de eco y escuchamos
    PORT = int(sys.argv[1])
    serv = socketserver.UDPServer(('', PORT), SIPRegisterHandler)
    print("Lanzando servidor UDP de eco...")
    serv.serve_forever()
