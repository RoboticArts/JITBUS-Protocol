
# JITBUS-Protocol

## Introducción

Implementación de un protocolo para la comunicación por puerto serie entre dispositivos que empleen esta comunicación de forma nativa o virtual (por ejemplo a través de un USB). El protocolo de este repositorio se ha escrito en Python y está pensado para ejecutarse en un ordenador. 

Cada una de las funciones viene acompañada de un ejemplo para comprender su utilidad. También se ha creado una interfaz para poder gestionar de forma visual la comunicación. Dicha GUI forma parte de otro proyecto más grande aún en construcción, sin embargo es completamente funcional para comprender el funcionamiento del protocolo.

## Motivación

Exiten pocos protocolos de comunicación orientados a transmisir datos de sensores o actuadores a través del bus USB. Uno de sus motivos se debe a que este bus es poco determinista y está sujeto a la latencia de un ordenador que no implementa un planificador de tiempo real. No obstante, hay aplicaciones donde no es importante cumplir plazos de tiempo en donde se requiere una transmisión de datos.

El USB tiene varios perfiles (almacenamineto masivo, audio HID), se ha elegido emular un puerto serie virtual para la transmisión de datos. Este método es elegido por la gran mayoria de fabricantes cuando quieren transmisitir información de sensores o actuadores en sus productos. Sin embargo, cada uno de los fabricantes termina creando su propio protocolo. Esto causa que no haya un protocolo general de comunicación y que cada persona tenga que crearse el suyo desde cero para transmitir datos. 

Existe el protocolo Modbus RTU sobre puerto serie el cual posee librerias para funcionar en un ordenador. El problema ocurre cuando se intenta migrar a un microcontrolador. Esto provoca que se tenga que volver a escribir la libreria desde cero en el uC ya que nunca hay librerias Modbus para todas las arquitecturas. Ante esta situación, como igualmente tenia que escribir un protocolo, decidí crearme el mio y lo llamé protocolo JITBUS. Este protocolo esta orientado principalmente a la robótica.

## Protocolo JITBUS

https://www.draw.io/?lightbox=1&highlight=0000ff&edit=_blank&layers=1&nav=1&title=Untitled%20Diagram.drawio#R3Ztdb5swFIZ%2FTS4rAQaHXLak29qpN02lXjvggFXAEXGWZL9%2BJnE%2BiKnKFgNntFLkHBtjP7w%2BxwfCCAXZ9ntBlskLj2g6cqxoO0LTkeP42JOfpWF3MLiuezDEBYsOJvtsmLHfVBktZV2ziK4qDQXnqWDLqjHkeU5DUbGRouCbarMFT6tnXZKYaoZZSFLd%2Bs4ikahpOeOz%2FQdlcXI8s40nh5qMHBurmawSEvHNhQk9jlBQcC4OpWwb0LRkd%2BRyOO7bJ7WngRU0F00OyF6iV%2Bz%2BTNav70%2BbzHvBz88fd6qXXyRdqwmrwYrdkUDB13lEy06sEXrYJEzQ2ZKEZe1GXnJpS0SWym%2B2LKruaCHo9tNx2qfZS9VQnlFR7GQTdcBYKUYJ5sRvc8aPLdUmuUCPVTuirnh86vkMRRYUl79g5GiMZoIUQpoemLgN14KlacBTXuyPRZFH%2FciV9pUo%2BAe9qPGdOcLYDGD8NWBkdcgXaXynRBBpSWkeyxH1LchJE0F2yMvVeL3tlnTk4FSe%2BWFeyFJclm5WpwF2qMFq7lRsnr6YWZzDhOdawODh%2BpWK7qXR30dm%2BYHKJnMmVkZd42JBcRjWucZoPJlbliHi6GvidqeLfawhD16DO%2F8uCJ7e3s7kb%2BdtgJ7XwFN2S8%2FX6Nn%2Ff8BGltvIDaC2qE40qtZtVM0H6d4ZHfMXUJBsBxolPf%2B4kRJJy3COpqFEQouaFUuov6iNIzj06XxhCLT3NWinS9COvmZtGTQdTLISYD5fLfczb2KyLNu2rfL%2FHzuo7dNYV9Ik%2F%2BxylOaGt5%2BwpWtTSkRUBVjVVc5zeiVCZdKEWgqOhSS9VxUZi6LyNLWKr64JE4q9cqBu3V7Tr5Gs05Zkke5BnyI5G7aQlATj%2BWH3U15l89vNftxE3Yap1k%2B0l4vryfgwHPIYmENGehZ%2F49YUCOgGG7FuQesZ%2FyBAS%2BcBDLR%2Bd2AYoBE00Po9gUH4aAfaphkZv30ABDS4YGj8jgIQ0NCCoavvqQehaAQtGLoDvbGBoAVD1xkoaGjB0O08M%2BznkU%2F%2FoPXMcBigwSlazwyHARra9s7tPDPsCDS47V3nmWE3oD1w2zs9MxwGaHDBsOa51SBAQwuGXueZYUegoQVDr%2F3M0AQ2aKHN0%2FM80%2Fo0gA1DC1SenrVBxAYt7Hjt52AmsIELIu0%2FazOBDVxI0PMjiGoDFxLaz3YMYBuDCwnt5y4msIELCRB%2F9Xr9ekXvP%2BjEehrRP6Xr9yhapCS%2Fnt%2Fo29ddvBaJHv8A


## ¡Comenzando!

Descarga este repositorio desde Github Web para poner en marcha todos los ejemplos. Asegurate que el directorio en tu ordenador debe quedar de la siguiente forma:
      
* MiProyecto
   * examples
   * GUI test
   * jitbus.py
           

       





 Implementation of a protocol for communication between USB devices through a virtual serial port
