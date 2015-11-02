#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Clase (y programa principal) para un servidor de eco en UDP simple
"""

import socketserver
import sys
import json
import time


class SIPRegisterHandler(socketserver.DatagramRequestHandler):
    """
    Echo server class
    """
    Dicc = {}

    def handle(self):

        line = self.rfile.read()
        linea = line.decode('utf_8')
        ip = self.client_address[0]
        registro = linea.split()[0]
        direccionSIP = linea.split()[1]
        expires = int(linea.split()[4])
        tiempo = time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime(time.time()))
        # Escribe dirección y puerto del cliente (de tupla client_address)
        self.json2registered()
        print(self.Dicc)
        while 1:
            # Leyendo línea a línea lo que nos envía el cliente
            print("El cliente nos manda " + line.decode('utf-8'))
            if registro == "REGISTER":
                self.wfile.write(b"SIP/2.0 200 OK\r\n\r\n")
                self.Dicc[direccionSIP] = [ip, time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime(time.time() + expires))]
            if expires == 0:
                del self.Dicc[direccionSIP]
            # Si no hay más líneas salimos del bucle infinito
            if not line or len(linea):
                break
            #retirar los usuarios que ya han excedido su tiempo de expiracion
            caducados = []
            for usuario in self.Dicc:
                if tiempo >= time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime(time.time() + expires)):
                    caducados.append(usuario)
            for usuario in caducados:
                del self.Dicc[usuario]
            print(self.Dicc)
        self.register2json()

    def register2json(self):
        fich = open('register.json', 'w')
        json.dump(self.Dicc, fich, sort_keys=True, indent=4, separators=(',', ':'))
        fich.close()

    def json2registered(self):
        """
        Comprobar la existencia del fichero json
        """
        fich = open('registered.json', 'w')
        try:
            self.Dicc = json.loads(fich)
        except:
            pass
        fich.close()

if __name__ == "__main__":
    # Creamos servidor de eco y escuchamos
    PORT = int(sys.argv[1])
    serv = socketserver.UDPServer(('', PORT), SIPRegisterHandler)
    print("Lanzando servidor UDP de eco...")
    serv.serve_forever()
