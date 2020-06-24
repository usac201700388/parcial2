# JDCR Importamos las librerias que se utilizaran en esta clase.
import paho.mqtt.client as mqtt
import logging
import time
import os 
import threading
from datetime import datetime


# JDCR funcion para crear una instancia de cliente mqtt
def client_instance():
    client = mqtt.Client(clean_session=True)
    return client

# JDCR Creacion de la Clase que manejara el Cliente
class ClientManagement:
    ''' JDCR Creacion del constructor en donde se le dice cuales sera los atributos del objeto servidor.
      Entre los cuales estan la direcion IP, el Usuario de MQTT con su password
     y los datos de nuestro grupo.''' 
    def __init__(self, ip_address, user_mqtt, password, port_mqtt, port_tcp=None, user=None, rooms=None, group=None):
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
    
    # JDCR Funcion para configurar el objeto como un suscriptor/ publicador en el MQTT
    def server_mqtt(self):
        # Nueva instancia de cliente
        client = self.instance
        pub = self.instance
        # JDCR Configuracion Inicial de logging en los niveles Info y Error
        logging.basicConfig(level=logging.INFO, format='\n[%(levelname)s] (%(threadName)-10s) %(message)s')
        logging.basicConfig(level=logging.ERROR, format='\n[%(levelname)s] (%(threadName)-10s) %(message)s')

        # JDCR Callback que se ejecuta cuando nos conectamos al broker.
        def on_connect_sub(client, userdata, rc):
            logging.info("Conectado al broker")
        # JDCR  Callback que se ejecuta cuando llega un mensaje al topic suscrito
        def on_message(client, userdata, msg):
            logging.info("Ha llegado el mensaje al topic: " + str(msg.topic))
            # JDCR Funcion para determinar los mensajes de texto o audio que llegan a los topics que esta suscrito el usuario.
            # JDCR Condicion de que si el topic que recibio la publicacion contiene la palabra audio se 
            # JDCR llama a la funcion audio.
            if 'audio' in str(msg.topic):
                x = self.audio()
                # Se recorre la lista x la cual contiene los topics a los cuales esta suscrito el usuario
                for i in range(0, len(x)):
                    # JDCR si el topic que llego es igual a algun elemento de la lista entonces se recibe y se reproduce el archivo.
                    if str(msg.topic) == x[i]:
                        #EMVB Se guarda la fecha y hora exacta en la que ingresa un mensaje de audio, con un formato definido
                        fecha = datetime.now().strftime("%d-%m-%Y_%H:%M:%S")
                        with open(str(fecha)+'.wav', 'wb') as recibido:
                            data = msg.payload
                            recibido.write(data)
                            recibido.close()

                        hilorep = threading.Thread(name = 'reproduccion',target = self.play_audio, args = (str(fecha)+'.wav',),daemon = False)
                        hilorep.start()
            # JDCR si el Topic que se recibio no contiene la palabra audio, significa que es texto lo cual se muestra al usuario.
            else:
                logging.info("El contenido del mensaje es: " + str(msg.payload, 'utf-8'))
        # JDCR Handler en caso suceda la conexion con el broker MQTT
        def on_connect_pub(client, userdata, flags, rc):
            connection_text = "CONNACK recibido del broker con codigo: " + str(rc)
            logging.info(connection_text)
        # JDCR Handler en caso se publique satisfactoriamente en el broker MQTT    
        def on_publish(client, userdata, mid):
            publish_text = "Publicacion satisfactoria"
            logging.debug(publish_text)

        client.on_connect_sub = on_connect_sub # JDCR Se configura la funcion "Handler" cuando suceda la conexion
        client.on_message = on_message # JDCR Se configura la funcion "Handler" que se activa al llegar un mensaje a un topic subscrito
        pub.on_connect_pub = on_connect_pub # JDCR Se configura la funcion "Handler" cuando suceda la conexion
        client.on_publish = on_publish #JDCR Se configura la funcion "Handler" que se activa al publicar algo
        client.username_pw_set(self.user, self.password) # JDCR Credenciales requeridas por el broker
    
    
    def connect(self):
        # JDCR se llama al atributo que  hace la instancia del cliente 
        client = self.instance
        # JDCR Conectar al servidor remoto
        client.connect(host=self.ip, port=self.portM) 

    def disconnect(self):
        # JDCR se llama al atributo que  hace la instancia del cliente 
        client = self.instance
        # JDCR  Se desconecta del broker
        client.disconnect()
    # JDCR 
    def subscribers(self):
        topic = []
        # JDCR leemos el archivo en donde se encuentran los datos del ususario
        with open(self.participants, 'r') as users:
            for i in users:
                # JDCR Se separa el contenido del archivo 
                split_users = i.split(',')
                # JDCR SE ingresa en la tupla con el siguiente formato, tanto para el topic usuarios como para audio
                tuple_users = ('usuarios' + '/' + split_users[0], self.Quality)
                tuple_audio = ('audio' + '/' + self.Groups + '/'+ split_users[0], self.Quality)
                # JDCR Se adjunta las tuplas a la lista creando una lista de tuplas
                topic.append(tuple_audio)
                topic.append(tuple_users)
            users.close()
        # JDCR leemos el archivo en donde se encuentra las salas a las que esta suscrito el usuario.
        with open(self.Room, 'r') as rooms:
            for i in rooms:
                # JDCR Se separa el contenido del archivo 
                split_rooms = i.split('\n')
                # JDCR Se ingresa en la tupla con el siguiente formato, tanto para el topic salas como para  salas de audio
                tuple_rooms = ('salas' + '/' + self.Groups + '/' + split_rooms[0][2:], self.Quality)
                tuple_rooms_audio = ('audio' + '/' + self.Groups + '/' + self.Groups + split_rooms[0][2:], self.Quality)
                # JDCR Se adjunta las tuplas a la lista creando una lista de tuplas
                topic.append(tuple_rooms_audio)
                topic.append(tuple_rooms)
            rooms.close()
        return topic
    # JDCR Funcion para sacar de la tupla de topics, los topics en donde se publicaran los archivos de audio
    def audio(self):
        # JDCR Se llama a la funcion que nos da la tupla de topics 
        topics_audio = self.subscribers()
        Tip_audio = []
        # JDCR Si algun elemento de la tupla contiene la palabra audio entonces se almacena en la lista.
        for i in topics_audio:
            if 'audio' in i[0]:
                # JDCR Lista en donde se adjunta los valores de la tupla que cumplen con la condicion.
                Tip_audio.append(i[0])
        # JDCR SE devuelve el valor de la lista.
        return Tip_audio   

    
    def subscription(self):
        # JDCR Instancia del cliente
        client = self.instance
        # JDCR lista de topics a los cuales esta suscrito el usuario
        # JDCR Estos deben ser en formato de tupla
        list_topics = self.subscribers()
        # JDCR se le asigna la tupla a la funcion de suscrbibirse en la libreria paho
        client.subscribe(list_topics[:])
        # JDCR Iniciamos el thread (implementado en paho-mqtt) para estar atentos a mensajes en los topics subscritos
        client.loop_start()
    # JDCR Funcion para publicar un mensaje de texto o de audio en el Broker 
    def publish_data(self, topic_root, topic_name, value):
        # JDCR Instancia del cliente
        client = self.instance
        # JDCR Concatenacion de los parametro requierido, que seran el topic al que se publique el mensaje.
        topics = topic_root + "/" + topic_name
        # JDCR Funcio de la libreria paho para publicar por medio de MQTT en el topic  deseado por el usuario.
        client.publish(topics, value, self.Quality, retain=False)
    # JDCR Funcion que Reproduce el archivo de audio recibido
    def play_audio(self, fileName):
        logging.info('Audio guardado') # JDCR Mensaje en consola.
        cont = 'aplay '+ str(fileName) # JDCR Concatenacion de todos las partes que requiere el comando.
        os.system(cont) # JDCR Ejecicion del comando de reproduccion 