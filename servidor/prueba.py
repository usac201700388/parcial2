import socket
import binascii
import os
import logging
import time

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
IP_ADDR = '167.71.243.238'
IP_ADDR_ALL = ''
IP_PORT = 9809

BUFFER_SIZE = 64 * 1024

serverAddress = (IP_ADDR, IP_PORT)
print('Iniciando servidor en {}, puerto {}'.format(*serverAddress))
sock.bind(serverAddress)

sock.listen(10)

logging.basicConfig(level=logging.DEBUG, format='%(message)s')

# JDCR Esperando conexion
print('Esperando conexion remota')
connection, clientAddress = sock.accept()
try:
    print('Conexion establecida desde', clientAddress)
    data = connection.recv(BUFFER_SIZE)

    if data == binascii.unhexlify("01"):
            print('Enviando Archivo...')
            print(os.stat('audior.wav').st_size)
            size = os.stat('audior.wav').st_size
            size = str(size).encode()
            connection.sendall(size)
            time.sleep(1)
            with open('audior.wav', 'rb') as f:
                print('Enviando...')
                connection.sendfile(f, 0)
                f.close()
            print("\n\nArchivo enviado a: ", clientAddress)
            pass
    if data == binascii.unhexlify("02"):
            print('Recibir archivo...')
            info = connection.recv(BUFFER_SIZE)
            info = int(info.decode())
            print(info)
            with open('audior.wav', 'wb') as g:
                print('Archivo Creado y listo para recibir...')
                while info:
                    sound = connection.recv(BUFFER_SIZE)
                    # print('data =', sound)
                    if not sound:
                        break
                    else:
                        g.write(sound)
                g.close()
except KeyboardInterrupt:
    sock.close()
finally:
    connection.close()