import socket
import binascii
import os
import logging

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
IP_ADDR = '167.71.243.238'
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

    while True:
        print('\nEsperando instrucciones')
        data = connection.recv(BUFFER_SIZE)
        print('Recibido: {!r}'.format(data))
        if data == binascii.unhexlify("01"):
            print('Enviando Archivo...')
            print(os.stat('text.txt').st_size)
            size = os.stat('text.txt').st_size
            size = str(size).encode()
            connection.sendall(size)
            with open('text.txt', 'rb') as f:
                connection.sendfile(f, 0)
                f.close()
            print("\n\nArchivo enviado a: ", clientAddress)
        elif data == binascii.unhexlify("02"):
            print('Recibir archivo...')
            info = connection.recv(BUFFER_SIZE)
            info = int(info.decode())
            print(info)
            with open('nuevo.txt', 'wb') as g:
                print('Archivo Creado y listo para recibir...')
                while info:
                    sound = connection.recv(BUFFER_SIZE)
                    print('data =', sound)
                    g.write(sound)
                    info -= info
                g.close()
        elif data == binascii.unhexlify("03"):
            print('cerrar conexion...')
            break
except KeyboardInterrupt:
    sock.close()
finally:
    connection.close()