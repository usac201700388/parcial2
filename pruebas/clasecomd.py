class comandos(object):

    def __init__(self, FTR, ID, filesize):
        self.FTR = FTR
        self.ID = ID
        self.filesize = filesize

    def getintruccion(self):
        return self.FTR

    def getcarnet(self):
        return self.ID
    
    def gettamaño(self):
        return self.filesize

    def __str__(self):
        return str('Orden: '+str(self.getintruccion())+' \nUsuario: '+str(self.getcarnet())+' \nTamaño: '+str(self.gettamaño()))

    def __repr__(self):
        return self.__str__()

lista = ['06','201709400', '']

final = comandos(lista[0], lista[1], lista[2])

orden = final.getintruccion()
destino = final.getcarnet()
file = final.gettamaño()

if (orden == "b'\\x02")):
    inst = orden 
    user = destino 
    tam = file 

if (orden == "b'\\x05"):
    if (destino == usuario)
        #permite el recibo de informacion
        pass
    else:
        #niega la conexion
        pass

if (orden == "b'\\x06"):
    if (destino == usuarioenvio)
        #permite el envio de informacion
        print('El destinatario es valido')

    else:
        #niega la conexion 
        break

if (orden == "b'\\x07")
    if (destino == usuarioenvio)
        #permite el envio de informacion
        print('El destinatario no es valido')
    else:
        #niega la conexion
        break
