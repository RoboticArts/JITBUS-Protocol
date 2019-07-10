from src import jitbus
import time


#atomRMS = jitbus.JitbusUSB("COM10", 2000000 , 0.00000001)

atomRMS = jitbus.JitbusUSB()
atomRMS.open("COM10", 3000000 , 0.00000001)

sendId = 0x3D4
#sendData = -256.872
sendData = 98

getId = 0
getData = 0
"""
Conclusiones
Hay una latencia de 2 ms. Sin embargo se pueden enviar hasta 256 bytes cada 2 ms
El numero de bytes máximos depende del buffer, el del ordenador es de 4096 bytes
pero como se usa un chip FTDI que convierte serie a USB, se depende de su buffer
maximo el cual es de 256 bytes. 

La latencia depende del ordenador e indica cuando se consultan los bytes almacenados
en el buffer. Como el ordenador debe atender a otros procesos no puede estar pendiente
del USB. El tiempo minimo de consulta que puede lograr es de 1 ms. Sin embargo se aconseja
enviar una rafaga de mensajes cada 2 ms para que funcione optimamente.

Aunque solo se pueda enviar datos cada 2ms, es posible enviar en cada viaje hasta 256 bytes.
Esto permitirá enviar los datos de todos los nodos de la red de un solo golpe. No obstante
si se quiere hacer un seguimiento en tiempo real de los datos hay que tener en cuenta que
como maximo se muestreará a 2 ms.

Los datos enviados, si no son atendidos por el UBS se almacenan en un buffer. Cuando se leen
los datos del buffer estos se eliminan para almacenar nuevos datos. De una lectura a otra del
buffer no deben aparecer datos corcenados. Sin embargo si es posible que aparecan datos 
incorrectos fruto interferencias. Esto significa que un buffer deberá contener un numero entero
de mensajes enviados. Esto simplica el algoritmo de busqueda del dato ya que no es necesario
conocer los datos del anterior buffer por si algun mensaje apareceria cortado.

"""

h,m,n,o,p,q = 0,0,0,0,0,0,

for x in range(20):
    h = h + 1
    m = h + 1
    n = m + 1
    o = n + 1
    p = o + 1
    q = p + 1

    print("Iteracion:", x )
    atomRMS.sendMsg(0x1D4, x)
    atomRMS.sendMsg(0x1D4, h)
    atomRMS.sendMsg(0x0FF, m)
    atomRMS.sendMsg(0x0FF, n)
    atomRMS.sendMsg(0x0FF, o)
    #atomRMS.sendMsg(0x1D4, p)
    #atomRMS.sendMsg(0x1D4, q)

    #atomRMS.sendMsg(0x1D4, sendData)
    time.sleep(0.002)

    if atomRMS.availableMsg() > 0:

        for w in range (atomRMS.isThereDataFromMaskId(0x1D4)):

            getId, getData = atomRMS.getDataFromMaskId(0x1D4)
            print("ID Recibido:   ", getId)
            print("Dato Recibido: ", getData)


        """
        if atomRMS.isThereDataFromMaskId(0x1D4) > 0:

            getId, getData = atomRMS.getLastDataFromMaskId(0x1D4)
            print("ID Recibido:   ", getId)
            print("Dato Recibido: ", getData)


        if atomRMS.isThereDataFromMaskId(0x0FF) > 0:

            getId, getData = atomRMS.getLastDataFromMaskId(0x0FF)
            print("ID Recibido:   ", getId)
            print("Dato Recibido: ", getData)
        """

        """
        numberOfMsgs = atomRMS.availableMsg()
        print("Mensajes en el buffer: ", numberOfMsgs)

        if atomRMS.isThereDataFromMaskId(0x1D4) > 0:

            getId, getData = atomRMS.getAllDataFromMaskId(0x1D4)
            print("ID Recibido:   ", getId)
            print("Dato Recibido: ", getData)

        if atomRMS.isThereDataFromMaskId(0x0FF) > 0:

            getId, getData = atomRMS.getAllDataFromMaskId(0x0FF)
            print("ID Recibido:   ", getId)
            print("Dato Recibido: ", getData)

        print("-----------------------------------------------------")
        """

        """
        getId, getData = atomRMS.getAllMsgs()
        print("ID Recibido:   ", getId)
        print("Dato Recibido: ", getData)
        print("-----------------------------------------------------")
        """

        """
        numberOfMsgs = atomRMS.availableMsg()
        print("Mensajes en el buffer: ", numberOfMsgs)

        for w in range (numberOfMsgs):

            getId, getData = atomRMS.getMsg()

            print("ID Recibido:   ",getId)
            print("Dato Recibido: ", getData)
            #print()

        print("-----------------------------------------------------")
        """

atomRMS.close()