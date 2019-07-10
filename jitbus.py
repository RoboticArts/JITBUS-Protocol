import serial
import math
import crcmod
import struct

class JitbusUSB:


    _idMsg = []
    _dataMsg = []
    _sizeBuffer = 256

    port = serial.Serial()

    def open(self, portCOM, baudrate=9600, timeout = 0.001  ):

        #Inicializa el constructor y abre el puerto COM
        self.port = serial.Serial(port = portCOM,
                                  baudrate = baudrate,
                                  timeout = timeout,
                                  bytesize = serial.EIGHTBITS,
                                  parity=serial.PARITY_NONE,
                                  stopbits= serial.STOPBITS_ONE
                                  #parity = serial.PARITY_ODD,
                                  #stopbits= serial.STOPBITS_TWO
                                  )

    def isOpen(self):

        #return self.port.isOpen()
        return self.port.isOpen()
    """
    def __init__(self, port, baudrate=9600, timeout = 0.001  ):

        #Inicializa el constructor y abre el puerto COM
        self.port = serial.Serial(port = port,
                                  baudrate = baudrate,
                                  timeout = timeout,
                                  bytesize = serial.EIGHTBITS,
                                  parity = serial.PARITY_ODD,
                                  stopbits= serial.STOPBITS_TWO
                                  )
    """

    def __buildMsg(self, id, data):

        print("Send:  ", data)

        # Si la variable es mayor de 32 bits, se evita el desbordamiento
        if data >= pow(2, 32):
            data = pow(2, 32) - 1
        elif data <= -pow(2, 32):
            data = -(pow(2, 32) - 1)

        # Se halla el signo del dato a enviar
        if data < 0:
            signBit = 0x1
            data = abs(data)
        else:
            signBit = 0x0

        # Se determina si es de tipo entero o decimal
        if isinstance(data, float):

            typeBit = 0x1
            # Representacion binaria del dato decimal
            data = (struct.unpack('!i', struct.pack('!f', data))[0])

        else:
            typeBit = 0x0

        initBit = 0x1  # 1 bit
        typeBit = typeBit  # 1 bit, 0x0 indica tipo entero, 0x01 indica tipo decimal
        signBit = signBit  # 1 bit, 0x0 indica signo positivo, 0x1 indica signo negativo
        id = id  # 11 bits, tamaño fijo
        data = data  # 32 bits máximos, tamaño variable, en este caso se usan 14 bits
        lengthDataBytes = self.__numberOfBytes(data)  # 2 bits fijos, tamaño en bytes de data

        # Se asigna un valor en binario para un numero determinado de bytes
        switcher = {
            1: 0b00,
            2: 0b01,
            3: 0b10,
            4: 0b11
        }
        lengthBit = switcher.get(lengthDataBytes, 0b00)

        message = initBit << (2 + 1 + 1 + 11 + lengthDataBytes * 8)
        message = message | (lengthBit << (1 + 1 + 11 + lengthDataBytes * 8))
        message = message | (id << (1 + 1 + lengthDataBytes * 8))
        message = message | (typeBit << (1 + lengthDataBytes * 8))
        message = message | (signBit << (lengthDataBytes * 8))
        message = message | data

        #print(bin(initBit))
        #print(bin(lengthBit))
        #print(bin(id))
        #print(bin(typeBit))
        #print(bin(signBit))
        #print(bin(data))
        #print(bin(message))

        # Inicializacion del CRC, polinomio generador CRC-8-CCITT
        crc8_func = crcmod.predefined.mkCrcFun('crc-8')

        # Calculo del CRC
        crc_send = crc8_func(message.to_bytes(self.__numberOfBytes(message), byteorder="big"))

        # print("CRC: ", bin(crc_send))


        sendMsg = (message << 8) | crc_send

        #print("Send: ", bin(sendMsg))

        # Conversion a cadena de bytes
        sendMsg = sendMsg.to_bytes(self.__numberOfBytes(sendMsg), byteorder="big")

        #print("Send: ", sendMsg)

        """
        #fakeSendMsg = ((message << 8) | crc_send) | (0x80 << (self.__numberOfBits(message)+8) )
        #fakeSendMsg = (((message << 8) | crc_send) << 8) | 0xFF
        #fakeSendMsg = (((message << 8) | 0xAB) << 8) | crc_send
        fakeSendMsg = 0x8080808080808080
        print("Send1: ", bin((message << 8) | crc_send))
        print("Send:  ", bin(fakeSendMsg))
        fakeSendMsg = fakeSendMsg.to_bytes(self.__numberOfBytes(fakeSendMsg), byteorder="big")
        """

        # Comprobacion del CRC
        # crc_check = crc8_func(sendMsg.to_bytes(numberOfBytes(sendMsg),byteorder="big"))
        # if crc_check == 0:
        #    print("CRC = ", bin(crc_check), " CRC calculado correctamente")
        # else:
        #   print("CRC = ", bin(crc_check), "CRC incorrecto")

        return sendMsg


    def sendMsg(self, id, data):
        msg = self.__buildMsg(id, data)
        self.port.write(msg)
    """
    def availableMsg(self):

        if self.port.inWaiting() > 0:
            return self.port.inWaiting()
        else:
            return 0
    """

    def getAllDataFromMaskId(self, maskId): #Lee todos los mensajes del buffer que tengan el ID indicado

        idx = []
        datax = []
        x = 0

        #Barrido hasta el numero de elementos del buffer
        while x < (len(self._dataMsg)):

            if self._idMsg[x] == str(maskId):

                datax.append(self._dataMsg.pop(x))
                idx.append(self._idMsg.pop(x))
                x = x - 1

            x = x + 1

        return idx, datax

    def getLastDataFromMaskId (self, maskId): #Lee el ultimo valor del buffer con el ID indicado

        idx, datax = self.getAllDataFromMaskId(maskId)

        return  idx[len(idx)-1], datax[len(datax)-1]


    #Devuelve el numero de mensajes que se han recibido hasta el momento con el ID indicado
    def isThereDataFromMaskId(self, maskId):

        numberOfMsgs = 0

        for x in range (len(self._dataMsg)):

            if self._idMsg[x] == str(maskId):
                numberOfMsgs = numberOfMsgs + 1

        return  numberOfMsgs


    def getDataFromMaskId(self, maskId):

        idx = 0
        datax = 0

        for x in range (len (self._dataMsg)):

            if self._idMsg[x] == str(maskId):
                datax = self._dataMsg.pop(x)
                idx = self._idMsg.pop(x)
                break

        return idx, datax

    def availableMsg(self):

        if self.port.inWaiting() > 0:

            #Se halla el numero de bytes en el buffer
            n = self.port.inWaiting()
            print("Hay ", n, " bytes en el buffer")

            rawBytes = [0 for v in range (n)]

            #Se lee del puerto y se guarda en un vector, una posicion ocupa 8 bits
            for i in range (n):
                rawBytes[i] = int.from_bytes(self.port.read(1), byteorder='big')


            #Desde 0 hasta que queden al menos 4 bytes (tamaño minimo del mensaje) en el buffer
            i = 0
            while i < (n-3):

                #Se busca el bit de inicio
                ib = rawBytes[i] >> 7

                # Si se encuentra un supuesto bit de inicio, se continua
                if ib == 1:

                    #Se obtiene la longitud de los datos: 8,16,24 o 32 bits
                    rawLengthDataBytes = ((rawBytes[i] << 1) & 0xFF) >> 6

                    switcher = {
                        0b00: 1,
                        0b01: 2,
                        0b10: 3,
                        0b11: 4
                    }

                    lengthDataBytes = switcher.get(rawLengthDataBytes, 0b00)

                    # Se suman los bytes de los datos mas los bytes resultado de: ib+tb+sb+id+crc
                    lengthBytes = lengthDataBytes + 3

                    #El numero de bytes del supuesto mensaje debe ser menor que el numero de bytes
                    #que QUEDAN por comprobar en el buffer
                    if lengthBytes <= (n-i):
                        # n-(i+1)
                        checkMessage = 0

                        # Con la informacion anterior, se reconstruye el supuesto mensaje
                        for k in range (i, lengthBytes+i): #De 0 a 3

                            checkMessage = checkMessage << 8
                            checkMessage = checkMessage | rawBytes[k]

                        # Inicializacion del CRC, polinomio generador CRC-8-CCITT
                        crc8_func = crcmod.predefined.mkCrcFun('crc-8')

                        # Se comprueba el CRC del supuesto mensaje
                        crc_check = crc8_func(
                            checkMessage.to_bytes(
                                self.__numberOfBytes(checkMessage), byteorder="big"))

                        if crc_check == 0:
                            #print("CRC = ", bin(crc_check), " CRC calculado correctamente")

                            nb = lengthBytes

                            #Se obtiene el ID y el dato del mensaje
                            verifiedMessage = checkMessage

                            windowMessage = pow(2, nb * 8) - 1

                            receiveId = ((verifiedMessage << 3) & windowMessage) >> (8 * nb - 11)  # 11bits ID
                            receiveType = (((verifiedMessage << 14) & windowMessage) >> ((8 * nb) - 1))
                            receiveSign = (((verifiedMessage << 15) & windowMessage) >> ((8 * nb) - 1))
                            receiveData = ((verifiedMessage << 16) & windowMessage) >> (8 * nb - (8 * (nb - 3)))

                            if receiveType == 1:
                                receiveData = (struct.unpack('!f', struct.pack('!i', receiveData))[0])
                                receiveData = round(receiveData, 7)

                            if receiveSign == 1:
                                receiveData = -receiveData

                            #print("ID recibido: ", hex(receiveId))
                            #print("Dato recibido: ", receiveData)

                            #Como el dato es correcto, se saltan el numero de bytes del mensaje correcto
                            i = (i + lengthBytes)-1

                            if len(self._idMsg) < self._sizeBuffer and len(self._dataMsg) < self._sizeBuffer :

                                self._idMsg.append(str(receiveId))
                                self._dataMsg.append(str(receiveData))

                            else:
                                self._idMsg.pop(0)
                                self._dataMsg.pop(0)
                                self._idMsg.append(str(receiveId))
                                self._dataMsg.append(str(receiveData))


                        else:
                            print("CRC incorrecto")
                            self._idMsg = self._idMsg
                            self._dataMsg = self._dataMsg

                i = i + 1

        return len(self._dataMsg)

    def getAllMsgs(self): #Lectura de todos los mensajes del buffer de golpe

        idx = self._idMsg.copy()
        datax = self._dataMsg.copy()
        self._idMsg.clear()
        self._dataMsg.clear()

        return  idx, datax

    def getMsg(self): #Lectura mensaje a mensaje del buffer

        idx = self._idMsg.pop()
        datax = self._dataMsg.pop()

        return idx, datax

    def close(self):
        #Cierra el puerto
        self.port.close()



    def __numberOfBits(self, value):

        return int(math.log(value, 2) + 1)

    def __numberOfBytes(self, value):

        if value != 0:
            valueBits = int(math.log(value, 2) + 1)

            if valueBits % 8 != 0:
                valueBits = (valueBits / 8) + 1
            else:
                valueBits = valueBits / 8
        else:
            valueBits = 1

        return int(valueBits)

