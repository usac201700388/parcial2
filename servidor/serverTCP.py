import socket
import binascii
import os
import logging

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
IP_ADDR = ''
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
    while data:
        print('\nEsperando instrucciones')
        print('Recibido: {!r}'.format(data))
        if data == binascii.unhexlify("01"):
            print('Enviando Archivo...')
            print(os.stat('audior.wav').st_size)
            size = os.stat('audior.wav').st_size
            size = str(size).encode()
            connection.sendall(size)
            with open('audior.wav', 'rb') as f:
                connection.sendfile(f, 0)
                f.close()
            print("\n\nArchivo enviado a: ", clientAddress)
        elif data == binascii.unhexlify("02"):
            print('Recibir archivo...')
            info = connection.recv(BUFFER_SIZE)
            info = int(info.decode())
            print(info)
            bytesRecividos = 0
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
        elif data == binascii.unhexlify("03"):
            print('cerrar conexion...')
            break
except KeyboardInterrupt:
    sock.close()
finally:
    connection.close()
