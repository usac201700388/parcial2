import socket
import binascii
import os
import logging
import time


SERVER_IP = '167.71.243.238'
SEVER_PORT = 9809
BUFFER_SIZE = 64 * 1024
DEFAULT_DELAY = 1

logging.basicConfig(level=logging.INFO, format='\n[%(levelname)s] (%(processName)-10s) %(message)s')
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_address = (SERVER_IP, SEVER_PORT)
#logging.info('Conectando a  {} en el puerto {}'.format(*server_address))
print('Conectando a  {} en el puerto {}'.format(*server_address))
sock.connect(server_address)

try:
    N = int(input('\nIngrese el comando para realizar alguna accion: '))
    if N == 1:
        sock.sendall(binascii.unhexlify("01"))
        info = sock.recv(BUFFER_SIZE)
        info = int(info.decode())
        print(info)
        with open('audior.wav', 'wb') as f:
            print('Archivo Creado y listo para leer...')
            while info:
                data = sock.recv(BUFFER_SIZE)
                # print('data=', data)
                if not data:
                    break
                else:
                    f.write(data)
            f.close()
        sock.close()
        os.system('aplay audior.wav')
    elif N == 2:
        sock.sendall(binascii.unhexlify("02"))
        print('Iniciando grabacion...')
        os.system('arecord -d 29 -f U8 -r 8000 audio.wav')
        print('Grabacion finalizada...')
        print(os.stat('audio.wav').st_size)
        size = os.stat('audio.wav').st_size
        size = str(size).encode()
        sock.sendall(size)
        time.sleep(DEFAULT_DELAY)
        with open('audio.wav', 'rb') as g:
            print('Enviando archivo...')
            sock.sendfile(g, 0)
            g.close()
        # sock.close()
        print('\n\nEnviado a  {} en el puerto {}'.format(*server_address))
finally:
    print('\n\nConexion finalizada con el servidor')
    sock.close()