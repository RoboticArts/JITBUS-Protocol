
# JITBUS-Protocol

## Introducción

Implementación de un protocolo para la comunicación por puerto serie entre dispositivos que empleen esta comunicación de forma nativa o virtual (por ejemplo a través de un USB). El protocolo de este repositorio se ha escrito en Python y está pensado para ejecutarse en un ordenador. 

Cada una de las funciones viene acompañada de un ejemplo para comprender su utilidad. También se ha creado una interfaz para poder gestionar de forma visual la comunicación. Dicha GUI forma parte de otro proyecto más grande aún en construcción, sin embargo es completamente funcional para comprender el funcionamiento del protocolo.

## Motivación

Exiten pocos protocolos de comunicación orientados a transmisir datos de sensores o actuadores a través del bus USB. Uno de sus motivos se debe a que este bus es poco determinista y está sujeto a la latencia de un ordenador que no implementa un planificador de tiempo real. No obstante, hay aplicaciones donde no es importante cumplir plazos de tiempo en donde se requiere una transmisión de datos.

El USB tiene varios perfiles (almacenamineto masivo, audio HID), se ha elegido emular un puerto serie virtual para la transmisión de datos. Este método es elegido por la gran mayoria de fabricantes cuando quieren transmisitir información de sensores o actuadores en sus productos. Sin embargo, cada uno de los fabricantes termina creando su propio protocolo. Esto causa que no haya un protocolo general de comunicación y que cada persona tenga que crearse el suyo desde cero para transmitir datos. 

Existe el protocolo Modbus RTU sobre puerto serie el cual posee librerias para funcionar en un ordenador. El problema ocurre cuando se intenta migrar a un microcontrolador. Esto provoca que se tenga que volver a escribir la libreria desde cero en el uC ya que nunca hay librerias Modbus para todas las arquitecturas. Ante esta situación, como igualmente tenia que escribir un protocolo, decidí crearme el mio y lo llamé protocolo JITBUS. Este protocolo esta orientado principalmente a la robótica.

## Protocolo JITBUS

<div class="mxgraph" style="max-width:100%;border:1px solid transparent;" data-mxgraph="{&quot;highlight&quot;:&quot;#0000ff&quot;,&quot;nav&quot;:true,&quot;resize&quot;:true,&quot;toolbar&quot;:&quot;zoom layers lightbox&quot;,&quot;edit&quot;:&quot;_blank&quot;,&quot;xml&quot;:&quot;&lt;mxfile modified=\&quot;2019-07-12T17:26:18.575Z\&quot; host=\&quot;www.draw.io\&quot; agent=\&quot;Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36\&quot; etag=\&quot;6d2QC3Zr1Oj5j9IpM1Vd\&quot; version=\&quot;10.9.6\&quot; type=\&quot;device\&quot;&gt;&lt;diagram id=\&quot;5ufkOElNQOAtNcuxiQpk\&quot; name=\&quot;Page-1\&quot;&gt;3Ztdb5swFIZ/TS4rAQaHXLak29qpN02lXjvggFXAEXGWZL9+JnE+iKnKFgNntFLkHBtjP7w+xwfCCAXZ9ntBlskLj2g6cqxoO0LTkeP42JOfpWF3MLiuezDEBYsOJvtsmLHfVBktZV2ziK4qDQXnqWDLqjHkeU5DUbGRouCbarMFT6tnXZKYaoZZSFLd+s4ikahpOeOz/QdlcXI8s40nh5qMHBurmawSEvHNhQk9jlBQcC4OpWwb0LRkd+RyOO7bJ7WngRU0F00OyF6iV+z+TNav70+bzHvBz88fd6qXXyRdqwmrwYrdkUDB13lEy06sEXrYJEzQ2ZKEZe1GXnJpS0SWym+2LKruaCHo9tNx2qfZS9VQnlFR7GQTdcBYKUYJ5sRvc8aPLdUmuUCPVTuirnh86vkMRRYUl79g5GiMZoIUQpoemLgN14KlacBTXuyPRZFH/ciV9pUo+Ae9qPGdOcLYDGD8NWBkdcgXaXynRBBpSWkeyxH1LchJE0F2yMvVeL3tlnTk4FSe+WFeyFJclm5WpwF2qMFq7lRsnr6YWZzDhOdawODh+pWK7qXR30dm+YHKJnMmVkZd42JBcRjWucZoPJlbliHi6GvidqeLfawhD16DO/8uCJ7e3s7kb+dtgJ7XwFN2S8/X6Nn/f8BGltvIDaC2qE40qtZtVM0H6d4ZHfMXUJBsBxolPf+4kRJJy3COpqFEQouaFUuov6iNIzj06XxhCLT3NWinS9COvmZtGTQdTLISYD5fLfczb2KyLNu2rfL/Hzuo7dNYV9Ik/+xylOaGt5+wpWtTSkRUBVjVVc5zeiVCZdKEWgqOhSS9VxUZi6LyNLWKr64JE4q9cqBu3V7Tr5Gs05Zkke5BnyI5G7aQlATj+WH3U15l89vNftxE3Yap1k+0l4vryfgwHPIYmENGehZ/49YUCOgGG7FuQesZ/yBAS+cBDLR+d2AYoBE00Po9gUH4aAfaphkZv30ABDS4YGj8jgIQ0NCCoavvqQehaAQtGLoDvbGBoAVD1xkoaGjB0O08M+znkU//oPXMcBigwSlazwyHARra9s7tPDPsCDS47V3nmWE3oD1w2zs9MxwGaHDBsOa51SBAQwuGXueZYUegoQVDr/3M0AQ2aKHN0/M80/o0gA1DC1SenrVBxAYt7Hjt52AmsIELIu0/azOBDVxI0PMjiGoDFxLaz3YMYBuDCwnt5y4msIELCRB/9Xr9ekXvP+jEehrRP6Xr9yhapCS/nt/o29ddvBaJHv8A&lt;/diagram&gt;&lt;/mxfile&gt;&quot;}"></div>
<script type="text/javascript" src="https://www.draw.io/js/viewer.min.js"></script>

## ¡Comenzando!

Descarga este repositorio desde Github Web para poner en marcha todos los ejemplos. Asegurate que el directorio en tu ordenador debe quedar de la siguiente forma:
      
* MiProyecto
   * examples
   * GUI test
   * jitbus.py
           

       





 Implementation of a protocol for communication between USB devices through a virtual serial port
