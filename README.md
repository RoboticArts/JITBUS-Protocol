
# JITBUS-Protocol

## Introducción 📑

Implementación de un protocolo para la comunicación por puerto serie entre dispositivos que empleen esta comunicación de forma nativa o virtual (por ejemplo a través de un USB). El protocolo de este repositorio se ha escrito en Python y está pensado para ejecutarse en un ordenador. 

Cada una de las funciones viene acompañada de un ejemplo para comprender su utilidad. También se ha creado una interfaz para poder gestionar de forma visual la comunicación. Dicha GUI forma parte de otro proyecto más grande aún en construcción, sin embargo es completamente funcional para comprender el funcionamiento del protocolo.

## Motivación 💪

Exiten pocos protocolos de comunicación orientados a transmisir datos de sensores o actuadores a través del bus USB. Uno de sus motivos se debe a que este bus es poco determinista y está sujeto a la latencia de un ordenador que no implementa un planificador de tiempo real. No obstante, hay aplicaciones donde no es importante cumplir plazos de tiempo en donde se requiere una transmisión de datos.

El USB tiene varios perfiles (almacenamineto masivo, audio HID), se ha elegido emular un puerto serie virtual para la transmisión de datos. Este método es elegido por la gran mayoria de fabricantes cuando quieren transmisitir información de sensores o actuadores en sus productos. Sin embargo, cada uno de los fabricantes termina creando su propio protocolo. Esto causa que no haya un protocolo general de comunicación y que cada persona tenga que crearse el suyo desde cero para transmitir datos. 

Existe el protocolo Modbus RTU sobre puerto serie el cual posee librerias para funcionar en un ordenador. El problema ocurre cuando se intenta migrar a un microcontrolador. Esto provoca que se tenga que volver a escribir la libreria desde cero en el uC ya que nunca hay librerias Modbus para todas las arquitecturas. Ante esta situación, como igualmente tenia que escribir un protocolo, decidí crearme el mio y lo llamé protocolo JITBUS. Este protocolo esta orientado principalmente a la robótica.

## Protocolo JITBUS 🔨

Ejemplo del protocolo JITBUS cuando se envia el identificador 0x1D4 y el dato 19

![protocol](images/jitbus-protocol.png)

JITBUS significa Just In Time Bus y es un protocolo en el que se envian unicamente los datos necesarios justo a tiempo. Esta basado en la estructura del protocolo CAN estándar. Dada su similitud es muy sencillo transmitir mediante JITBUS los datos recibidos de un dispositivo CAN a traves de un microcontrolador para que los datos puedan ser adquiridos por el USB de un ordenador. 

Los componentes que el usuario debe tener en cuenta son la ID y el DATO. El ID representa la identificación del dispositivo al que se debe acceder. Por ejemplo un controlador de motor que se comunique por puerto serie (nativo o virtual) puede tener asignada la direccion 0x1D4 y un controlador de leds la direccion 0xFF. Esta asigación debe ser establecidad por el programador y según el dispositivo que se trate él debe considerar el DATO de una forma u otra. Por ejemplo, si el ID es del motor, el DATO se puede tratar de la velocidad (si asi lo ha establecido el programador). 

### Partes del protocolo

Las partes del protocolo son las siguientes
* *Start bit:* bit que detecta el inicio de la trama
* *Data lenght:* dos bits que indican la longitud máxima del DATO en bytes (1-4 bytes)
* *Identification:* once bits que indican la identificacion del dispositivo
* *Type bit:* indica si el DATO es de tipo float o entero 
* *Sign bit:* indica el signo del DATO
* *Data:* dato que se envia, su tamaño puede ser de 1,2,3 o 4 bytes
* *CRC:* verificación de redundancia cíclica de tipo CCITT

### Tipos de DATO a enviar

El dato a enviar puede ser de tipo *float* o de tipo *int*, en ambos casos el valor no será nunca superior a 32 bits. Las variables de tipo *float* son de precision simple y ocupan siempre 4 bytes en el protocolo. Las variable de tipo *int* ocuparán 1, 2, 3 o 4 bytes en función del valor que se pretenda transmitir. No es necesario indicar de qué tipo será el dato a enviar y tampoco hay que indicar la longitud que va a ocupar, el módulo JITBUS se encarga de hacerlo automaticamente por el programador.

Por otro lado, el protocolo JITBUS tiene dedicado un bit para saber el signo del DATO. Esto significa que las variables de tipo entero pueden adquirir ![](http://latex.codecogs.com/gif.latex?2%5E%7B32%7D) valores tanto en positivo como en negativo. Los valores máximos y mínimos de las variables float se rigen por la norma IEE 754 con precision simple.

### Mejoras futuras

* Los once bits de indentificacion pueden partirse en 7 bits para la identificacion del dipositivo y otros 4 bits para poder indicar alguna caracteristica del dispositivo. Por ejemplo, en el controlador de un motor, con un ID de 7 bits, se podrían señalar 16 caracteristicas diferentes: velocidad, posicion inicial, valores del PI, etc.

* Implementar una capa de aplicación en este protocolo que permita crear un diccionario de objetos. De esta forma cada actuador tendrá un identificador fijo que facilite la portabilidad del codigo.


## ¡Comenzando! :rocket:

Descarga este repositorio desde Github Web para poner en marcha todos los ejemplos. Asegurate que el directorio en tu ordenador debe quedar de la siguiente forma:
      
* JITBUS-Protocol
   * examples
   * GUI test
   * jitbus.py
 
Abre uno de los ejemplos de la carpeta *examples*. Estos ejemplos envian la trama JITBUS, esperan la respuesta y reciben la trama en el mismo código. Por este motivo es necesario que conectes por USB un disposivo que implemente el protocolo JITBUS para que pueda contestar. Sino dispones de ese recurso puedes emplear un chip FTDI en modo eco (loopback mode). Para ello hay que conectar el pin TX al pin RX. De este forma la trama enviada al chip FTDI sera devuelta al ordenador como si fuera un eco.
 
 ![schematic](http://buyhere22.com/components/usb-ttl-ft232rl-pinout.png)

### Mejorando la latencia

Por defecto, la latencia en Windows es de 16 ms, esto hace un cuello de botella si se desean tramisitir datos a gran velocidad. Para camibar la latencia hay que ir a:

```
  * Administrador de Dispositivos -> Puerto COM (el nuestro) -> Propiedades -> Configuración del puerto -> Opciones Avanzadas 
```

⚠️ Es importante que si quieres conseguir la máxima velocidad emplees el FTDI 232RL o alguno similar del mismo fabricante. Los chips como el CH340 son mas lentos ya que no se les puede modificar la latencia.

![latencia](images/latenciaW10.png)


Una vez con todos los recursos necesarios ¡ejecuta el programa! Por ejemplo, el resultado para el ejemplo *example_getAllMsgs* es el siguiente:

![example1](images/result-getAllMsgs.png)


# Funciones del módulo JITBUS

El módulo JITBUS para Python implementa las funciones necesarias para enviar y recibir los mensajes. Las funciones son:

```python
  myJitbus.open(COMport, baudrate , timeout)
  myJitbus.close()
  myJitbus.sendMsg(id, data)
  myJitbus.availableMsg()
  myJitbus.getAllMsgs()
  myJitbus.getMsg()
  myJitbus.isThereDataFromMaskId(id)
  myJitbus.getAllDataFromMaskId(id)
  myJitbus.getDataFromMaskId(id)
  myJitbus.getLastDataFromMaskId(id)
```

## Inicialización 

Ejemplo de inicialización 

```python
myJitbus = jitbus.JitbusUSB()
myJitbus.open("COM10", 3000000 , 0.00000001)
```

Se crea un objeto llamado *myJitbus* y se abre el puerto COM10 a 3 Mbits/s con un timeout pequeño

## Envio de mensajes

Mediante la siguiente función se envia la trama JITBUS. Es necesario indicar el identificacdor (máximo 0x7FF) y el dato que puede ser un valor entero o decimal positivo o negativo (máximo ![](http://latex.codecogs.com/gif.latex?2%5E%7B32%7D) )

```python
myJitbus.sendMsg(id, data)
```

Ejemplo de envio de un mensaje

```python
id = 0x1D4
data = 19
myJitbus.sendMsg(id, data)
time.sleep(0.002)
```

Se envia un mensaje con identificador 0x1D4 y dato 19. Es recomendable realizar una espera de 2 ms para evitar problemas con la latencia del ordenador. Si no se realiza la pausa, los bytes recibidos por el puerto serie que no hayan sido recogidos por el USB se almacenarán en un buffer para su posterior comprobación. 

## Recepcion de datos

Para recibir los datos hay que invocar la función de abajo. Esto permite leer desde el puerto serie y encontrar el mensaje entre los datos en raw recibidos desde otro dispositivo que ha enviado una trama JITBUS. Todos los mensajes correctamente recibidos se almacenarán en un buffer de 256 bytes a la espera de que sean consultados. La función devuelve el número de mensajes que existen en dicho buffer hasta el momento

```python
 if myJitbus.availableMsg() > 0:
      #Hacer cosas...
 ```
 
 Cuando hay datos disponibles en el buffer la función de abajo devuelve de golpe todos los mensajes almacenados hasta el momento. Una vez que la función ha terminado los mensajes del buffer son eliminados. Si hay mas de un mensaje almacenado, las variables *getId* y *getData* se convierten en vectores.
 
 ```python
 getId, getData = myJitbus.getAllMsgs()
 ```


 Implementation of a protocol for communication between USB devices through a virtual serial port
