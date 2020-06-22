#prueba Cliente
import paho.mqtt.client as mqtt
import logging
import time
import os
import threading
import sys 
from Data import * #Informacion de la conexion

LOG_FILENAME = 'mqtt.log'

DEFAULT_DELAY = 1 #1 minuto

#Configuracion inicial de logging
logging.basicConfig(
    level = logging.INFO, 
    format = '\n[%(levelname)s] (%(threadName)-10s) %(message)s'
    )

#Callback que se ejecuta cuando nos conectamos al broker
def on_connect_sub(client, userdata, rc):
    logging.info("Conectado al broker")


#Callback que se ejecuta cuando llega un mensaje al topic suscrito
def on_message(client, userdata, msg):
    #Se muestra en pantalla informacion que ha llegado
    logging.info("Ha llegado el mensaje al topic: " + str(msg.topic))
    logging.info("El contenido del mensaje es: " + str(msg.payload))
    
    #Y se almacena en el log 
    logCommand = 'echo "(' + str(msg.topic) + ') -> ' + str(msg.payload) + '" >> ' + LOG_FILENAME
    os.system(logCommand)


def on_connect_pub(client, userdata, flags, rc): 
    connectionText = "CONNACK recibido del broker con codigo: " + str(rc)
    logging.info(connectionText)

#Handler en caso se publique satisfactoriamente en el broker MQTT
def on_publish(client, userdata, mid): 
    publishText = "Publicacion satisfactoria"
    logging.debug(publishText)


client = mqtt.Client(clean_session=True) #Nueva instancia de cliente
clientp = mqtt.Client(clean_session=True) #Nueva instancia de cliente


client.on_connect_sub = on_connect_sub #Se configura la funcion "Handler" cuando suceda la conexion
client.on_message = on_message #Se configura la funcion "Handler" que se activa al llegar un mensaje a un topic subscrito
clientp.on_connect_pub = on_connect_pub #Se configura la funcion "Handler" cuando suceda la conexion
client.on_publish = on_publish #Se configura la funcion "Handler" que se activa al publicar algo


client.username_pw_set(MQTT_USER, MQTT_PASS) #Credenciales requeridas por el broker
client.connect(host=MQTT_HOST, port = MQTT_PORT) #Conectar al servidor remoto

#Nos conectaremos a distintos topics:
qos = 2

#Subscripcion simple con tupla (topic,qos)
#client.subscribe(("sensores/6/hum", qos))

client.subscribe([("usuarios/201700388", qos),("salas/09/S01", qos),("salas/09/S02", qos)])#<----implementar archivo----------------
#client.subscribe(("usuarios/#", qos))

#Subscripcion multiple con lista de tuplas
#client.subscribe([("sensores/8/#", qos), ("sensores/+/atm", qos), ("sensores/0/temp", qos)])

#pub----------------------------------------
def publishData(topicRoot, topicName, value, qos = 0, retain = False):
    topics = topicRoot + "/" + topicName
    client.publish(topics, value, qos, retain)


def tramaAlive(topic_c = 'comandos', grupo = '09'):
   
    logging.info('enviando alives')
    al = '\x04'
    separador = '-'
    carne = '201700388'
    while True:
        publishData(topic_c, grupo, al+separador+carne)
        time.sleep(2)
        


hiloTA = threading.Thread(name = 'Trama ALIVE',
                        target = tramaAlive,
                        args = (()),
                        daemon = True
                        )

hiloTA.start()

    
print('\n')
print(' ========================================================')
print(' |                                                      |')
print(' |                   Hola mi pana XD                    |')
print(' |                                                      |')
print(' ========================================================')
print('\n')




#Iniciamos el thread (implementado en paho-mqtt) para estar atentos a mensajes en los topics subscritos
client.loop_start()
#client.loop_forever()

#El thread de MQTT queda en el fondo, mientras en el main loop hacemos otra cosa

try:
    while True:
        try:
            
            print('\n==> 1. Enviar mensaje')
            print('==> 2. Enviar voz')
            print('==> 3. Adios')
            opcion = int(input('Escoge una opcion (solo funiona el 1 :v): '))


            if opcion == 1:

                print('\n==> 1. Usuario(privado)')
                print('==> 2. Sala')
                destino = int(input('Enviar a usuario o sala? '))

                if destino == 1:
                    carne = int(input('\nIngrese usuario(carne): '))    
                    mensaje_a_enviar = str(input('Escriba el mensaje:\n\n'))
                    publishData('usuarios', str(carne), mensaje_a_enviar)
                    logging.info("Los datos han sido enviados al broker")

                elif destino == 2:
                    opc_sala = int(input('Ingrese numero de sala[max 99](sin ceros a la izquierda >:v): '))
                    if len(str(opc_sala)) == 2:
                        sala = '09/S'+str(opc_sala)
                    elif len(str(opc_sala)) == 1:
                        sala = '09/S0'+str(opc_sala)
                    else:
                        print('no sea bobo >:v')
                        continue        
                    mensaje_a_enviar = str(input('Escriba el mensaje:\n\n'))
                    publishData('salas', sala, mensaje_a_enviar)
                    logging.info("Los datos han sido enviados al broker")

                else:
                    print('incorrecto pruebe de nuevo')    

            elif opcion == 2:
                print('no funciona :(, ingrese de nuevo')

            elif opcion == 3:
                break
            
            else:
                print('incorrecto pruebe de nuevo')

        except ValueError:
            print('Error: mal ingreso espere...')
            #pass  
                                     
        time.sleep(DEFAULT_DELAY)

        #logging.info("olakease")
        #time.sleep(10)


except KeyboardInterrupt:
    logging.warning("Desconectando del broker...")
    logging.info("Terminando hilos")
    
#    if hiloTA.is_alive():
#        hiloTA._stop()

finally:
    
    logging.info('no mas alives')
    client.loop_stop() #Se mata el hilo que verifica los topics en el fondo
    client.disconnect() #Se desconecta del broker
    clientp.disconnect()
    #logging.info("Desconectado del broker. Saliendo...")
    #sys.exit()



