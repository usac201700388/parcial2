import paho.mqtt.client as mqtt
import logging
import time
import os 


MQTT_HOST = '167.71.243.238'
MQTT_PORT = 1883

MQTT_USER = "proyectos"
MQTT_PASS = "proyectos980"

LOG_FILENAME = 'mqtt.log'

#Configuracion inicial de logging
logging.basicConfig(
    level = logging.INFO, 
    format = '[%(levelname)s] (%(threadName)-10s) %(message)s'
    )

#Callback que se ejecuta cuando nos conectamos al broker
def on_connect(client, userdata, flags, rc):
    logging.info("Conectado al broker")
    logging.info("Resultado de la conexcion: " + str(rc))
    # print("Connection returned result: " + connack_string(rc))


#Callback que se ejecuta cuando llega un mensaje al topic suscrito
def on_message(client, userdata, msg):
    #Se muestra en pantalla informacion que ha llegado
    # muesta de donde viene la informacion. 
    logging.info("Ha llegado el mensaje al topic: " + str(msg.topic))
    # muestra la info que llego
    logging.info("El contenido del mensaje es: " + str(msg.payload))
    
    #Y se almacena en el log 
    logCommand = 'echo "(' + str(msg.topic) + ') -> ' + str(msg.payload) + '" >> ' + LOG_FILENAME
    os.system(logCommand)



client = mqtt.Client(clean_session=True) #Nueva instancia de cliente
client.on_connect = on_connect #Se configura la funcion "Handler" cuando suceda la conexion
client.on_message = on_message #Se configura la funcion "Handler" que se activa al llegar un mensaje a un topic subscrito
client.username_pw_set(MQTT_USER, MQTT_PASS) #Credenciales requeridas por el broker
client.connect(host=MQTT_HOST, port = MQTT_PORT) #Conectar al servidor remoto


#Nos conectaremos a distintos topics:
qos = 2

#Subscripcion simple con tupla (topic,qos)
client.subscribe(("hola/09/201700796", qos))

#Subscripcion multiple con lista de tuplas
# client.subscribe([("sensores/8/#", qos), ("sensores/+/atm", qos), ("sensores/0/temp", qos)])


#Iniciamos el thread (implementado en paho-mqtt) para estar atentos a mensajes en los topics subscritos
client.loop_start()
# client.loop_forever()

#El thread de MQTT queda en el fondo, mientras en el main loop hacemos otra cosa

try:
    while True:
        logging.info("olakease")
        time.sleep(5)


except KeyboardInterrupt:
    logging.warning("Desconectando del broker...")

finally:
    client.loop_stop() #Se mata el hilo que verifica los topics en el fondo
    client.disconnect() #Se desconecta del broker
    logging.info("Desconectado del broker. Saliendo...")
