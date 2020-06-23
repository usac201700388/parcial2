#https://www.geeksforgeeks.org/arecord-command-in-linux-with-examples/

import os 
import logging
from datetime import datetime

logging.basicConfig(
    level = logging.DEBUG, 
    format = '%(message)s'
    )

now = datetime.now()
print(now)
dt_string = now.strftime("%d-%m-%Y_%H:%M:%S")
nombre = dt_string
print(nombre)

#timestamp = datetime.timestamp(now)
#print(timestamp)

logging.info('Comenzando grabacion')
os.system('arecord -d 5 -f U8 -r 8000 ' + str(nombre) +'.wav')

logging.info('Grabacion finalizada, inicia reproduccion')
os.system('aplay ' + str(nombre) + '.wav')
