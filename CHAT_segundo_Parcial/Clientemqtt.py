import paho.mqtt.client as mqtt
import logging
import time
import os 
import threading
from Globales import*
from datetime import datetime


def client_instance():
    client = mqtt.Client(clean_session=True)
    return client

def banner1():
    print('\n')
    print(' ========================================================')
    print(' |                                                      |')
    print(' |               Bienvenido al chat de Voz!             |')
    print(' |                       Parcial 2                      |')
    print(' |                                                      |')
    print(' ========================================================')
    print('\n')

def banner2():
    print('\n==> 1. Enviar mensaje de texto')
    print('==> 2. Enviar mensaje de voz')
    print('==> 3. Salir')

def banner3():
    print('\n==> 1. Usuario(privado)')
    print('==> 2. Sala')    



class ClientManagement:
    
    def __init__(self, ip_address, user_mqtt, password, port_mqtt, port_tcp=None, user=FILE_USERS, rooms=FILE_ROOMS, group=GROUP_NUMBER):
        self.ip = ip_address
        self.user = user_mqtt
        self.password = password
        self.portM = port_mqtt
        self.portT = port_tcp
        self.participants = user
        self.Room = rooms
        self.Groups = group
        self.instance = client_instance()
        self.Quality = 2
    
    def server_mqtt(self):
        client = self.instance
        pub = self.instance
        logging.basicConfig(level=logging.INFO, format='\n[%(levelname)s] (%(threadName)-10s) %(message)s')
        logging.basicConfig(level=logging.ERROR, format='\n[%(levelname)s] (%(threadName)-10s) %(message)s')

        def on_connect_sub(client, userdata, rc):
            logging.info("Conectado al broker")
            
        def on_message(client, userdata, msg):
            logging.info("Ha llegado el mensaje al topic: " + str(msg.topic))

            if (str(msg.topic) == 'audio/09/201700796' or str(msg.topic) == 'audio/09/09S01'):
                fecha = datetime.now().strftime("%d-%m-%Y_%H:%M:%S")
                with open(str(fecha)+'.wav', 'wb') as recibido:
                    data = msg.payload
                    recibido.write(data)
                    recibido.close()

                hilorep = threading.Thread(name = 'reproduccion',
                        target = self.play_audio,
                        args = (str(fecha)+'.wav',),
                        daemon = False
                        )
                hilorep.start()
            else:
                logging.info("El contenido del mensaje es: " + str(msg.payload, 'utf-8'))

            
            
        def on_connect_pub(client, userdata, flags, rc):
            connection_text = "CONNACK recibido del broker con codigo: " + str(rc)
            logging.info(connection_text)
            
        def on_publish(client, userdata, mid):
            publish_text = "Publicacion satisfactoria"
            logging.debug(publish_text)

        client.on_connect_sub = on_connect_sub
        client.on_message = on_message
        pub.on_connect_pub = on_connect_pub
        client.on_publish = on_publish
        client.username_pw_set(self.user, self.password)
    
    
    def connect(self):
        client = self.instance
        pub = self.instance
        client.connect(host=self.ip, port=self.portM)

    def disconnect(self):
        client = self.instance
        client.disconnect()
    
    def subscribers(self):
        topic = []
        with open('usuarios.txt', 'r') as users:
            for i in users:
                split_users = i.split(',')
                tuple_users = ('usuarios' + '/' + split_users[0], self.Quality)
                topic.append(tuple_users)
            users.close()
        with open('salas.txt', 'r') as rooms:
            for i in rooms:
                split_rooms = i.split('\n')
                tuple_rooms = ('salas' + '/' + self.Groups + '/' + split_rooms[0][2:], self.Quality)
                topic.append(tuple_rooms)
            rooms.close()
        topic.append(('audio/' + self.Groups + '/#', self.Quality))
        # topic.append(('comandos/' + self.Groups + '/#', self.Quality))
        return topic
    
    def subscription(self):
        client = self.instance
        client_p = self.instance
        list_topics = self.subscribers()
        client.subscribe(list_topics[:])
        client.loop_start()
    
    def publish_data(self, topic_root, topic_name, value):
        client = self.instance
        topics = topic_root + "/" + topic_name
        client.publish(topics, value, self.Quality, retain=False)
    
    def play_audio(self, fileName):
        logging.info('Audio guardado')
        cont = 'aplay '+ str(fileName)
        os.system(cont)

    
chat = ClientManagement(MQTT_HOST, MQTT_USER, MQTT_PASS, MQTT_PORT)
chat.server_mqtt()
chat.connect()
chat.subscription()
print(chat.subscribers())
banner1()

try:
    while True:
        try:
            banner2()
            opcion = int(input('Escoja una opcion: '))

            if opcion == 1 :
                banner3()
                destino = int(input('Enviar a usuario o sala? '))

                if destino == 1:
                    carne = int(input('\nIngrese usuario(carne): '))    
                    mensaje_a_enviar = str(input('Escriba el mensaje:\n\n'))
                    chat.publish_data('usuarios', str(carne), mensaje_a_enviar)
                    logging.info("El mensaje ha sido enviado")
                
                elif destino == 2:
                    opc_sala = int(input('Ingrese el numero de sala[max 99](sin ceros a la izquierda): '))
                    if len(str(opc_sala)) == 2:
                        sala = '09/S'+str(opc_sala)
                    elif len(str(opc_sala)) == 1:
                        sala = '09/S0'+str(opc_sala)
                    else:
                        logging.warning('Numero incorrecto. Intente de nuevo')
                        continue        
                    mensaje_a_enviar = str(input('Escriba el mensaje:\n\n'))
                    chat.publish_data('salas', sala, mensaje_a_enviar)
                    logging.info("El mensaje ha sido enviado")
                
                else:
                    logging.warning('Opcion incorrecta. Intente de nuevo')
            
            elif opcion == 2:
                duracion = int(input('Ingrese la duracion en segundos(max 30): '))
                if duracion <= 30:

                    banner3()
                    destino2 = int(input('Enviar a usuario o sala? '))

                    if destino2 == 1:
                        carne2 = int(input('\nIngrese usuario(carne): '))
                        logging.info('Grabe su mensaje')
                        os.system('arecord -d '+str(duracion)+' -f U8 -r 8000 audioparaenviar.wav')
                        logging.info('Mensaje grabado')

                        file = open('audioparaenviar.wav', 'rb')
                        audiostring = file.read()
                        bytesArray = bytes(audiostring)
                        chat.publish_data('audio/09', str(carne2), bytesArray)
                        logging.info('Mensaje enviado')

                    elif destino2 == 2:
                        opc_sala2 = int(input('Ingrese numero de sala[max 99](sin ceros a la izquierda): '))
                        if len(str(opc_sala2)) == 2:
                            sala = '09S'+str(opc_sala2)
                        elif len(str(opc_sala2)) == 1:
                            sala = '09S0'+str(opc_sala2)
                        else:
                            logging.warning('Numero incorrecto. Intente de nuevo')
                            continue        
                        logging.info('Grabe su mensaje')
                        os.system('arecord -d '+str(duracion)+' -f U8 -r 8000 audioparaenviar.wav')
                        logging.info('Mensaje grabado')

                        file = open('audioparaenviar.wav', 'rb')
                        audiostring = file.read()
                        bytesArray = bytes(audiostring)
                        chat.publish_data('audio/09', sala, bytesArray)
                        logging.info('mensaje enviado')

                    else:
                        logging.warning('Opcion incorrecta. Intente de nuevo')                   
                else:
                    logging.warning('Valor incorrecto. Intente de nuevo')
            elif opcion == 3:
                break

            else:
                logging.warning('Opcion incorrecta. Intente de nuevo')
        except ValueError:
            logging.error('Error: Respuesta invalida')
        
        time.sleep(DEFAULT_DELAY)
except KeyboardInterrupt:
    pass

finally:
    logging.warning("Saliendo del programa...")
    chat.disconnect()







