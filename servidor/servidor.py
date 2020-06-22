import paho.mqtt.client as mqtt
import logging
import time
import os 

MQTT_HOST = '167.71.243.238'
MQTT_PORT = 1883

MQTT_USER = "proyectos"
MQTT_PASS = "proyectos980"

LOG_FILENAME = 'mqtt.log'
DEFAULT_DELAY = 1  

#Configuracion inicial de logging
logging.basicConfig(
    level = logging.INFO, 
    format = '[%(levelname)s] (%(threadName)-10s) %(message)s'
    )

#Callback que se ejecuta cuando nos conectamos al broker
def on_connect(client, userdata, rc):
    logging.info("Conectado al broker")

#Callback que se ejecuta cuando llega un mensaje al topic suscrito
def on_message(client, userdata, msg):
    #Se muestra en pantalla informacion que ha llegado
    # muesta de donde viene la informacion. 
    logging.info("Ha llegado el mensaje al topic: " + str(msg.topic))
    # muestra la info que llego
    logging.info("El contenido del mensaje es: " + str(msg.payload)+ '\n')
    
    #Y se almacena en el log 
    logCommand = 'echo "(' + str(msg.topic) + ') -> ' + str(msg.payload) + '" >> ' + LOG_FILENAME
    os.system(logCommand)

def on_connect_pub(client, userdata, flags, rc):
    connectionText = "CONNACK recibido del broker con codigo: " + str(rc)
    logging.info(connectionText)

def on_publish(client, userdata, mid):
    publishText = "Publicacion satisfactoria"
    logging.debug(publishText)



client = mqtt.Client(clean_session=True) #Nueva instancia de cliente
clientp  = mqtt.Client(clean_session=True)


client.on_connect = on_connect #Se configura la funcion "Handler" cuando suceda la conexion
client.on_message = on_message #Se configura la funcion "Handler" que se activa al llegar un mensaje a un topic subscrito
clientp.on_connect_pub = on_connect_pub
clientp.on_publish = on_publish

client.username_pw_set(MQTT_USER, MQTT_PASS) #Credenciales requeridas por el broker
client.connect(host=MQTT_HOST, port = MQTT_PORT) #Conectar al servidor remoto


#Nos conectaremos a distintos topics:
qos = 2

#Subscripcion simple con tupla (topic,qos)
client.subscribe(("comandos/201700796", qos))

def publishData(topicRoot, topicName, value, qos=0, retain=False):
    topics = topicRoot + "/" + topicName
    client.publish(topics, value, qos, retain)

#Subscripcion multiple con lista de tuplas
# client.subscribe([("sensores/8/#", qos), ("sensores/+/atm", qos), ("sensores/0/temp", qos)])


#Iniciamos el thread (implementado en paho-mqtt) para estar atentos a mensajes en los topics subscritos
client.loop_start()
# client.loop_forever()

#El thread de MQTT queda en el fondo, mientras en el main loop hacemos otra cosa

try:
    while True:
        if ve == 'h':
            logging.info('si llego')
        else:
            logging.info('no llego')
        time.sleep(DEFAULT_DELAY)
except KeyboardInterrupt:
    logging.warning("Desconectando del broker...")

finally:
    client.loop_stop() #Se mata el hilo que verifica los topics en el fondo
    client.disconnect() #Se desconecta del broker
    clientp.disconnect()
    logging.info("Desconectado del broker. Saliendo...")
