# IBOOT CONSOLA TEL 1.5M - MQTT

Maneja 8 salidas de alimentación eléctrica del Iboot instalado en el gabinete de la
consola en el telescopio de 1.5m, recibe las instrucciones en JSON.

## Documentación del Programa

El programa esta en lenguaje Python3 se encarga de la comunicación entre
el Iboot de consola y el broker MQTT.

### Dependencias

Depende de:

+ pip3 install pexpect
+ pip3 install simplejson
+ pip3 install paho-mqtt

## Arranque

Se encuentra configurado el arranque automatico mediante el paquete supervisor.

Para reiniciar el proceso en una terminal de comandos ejecute la siguiente instrucción:

> - sudo supervisorctl restart iboot_consola

También es posible accesar a la interfaz web de supervisor en el siguiente enlace:

> - [supervisor webpage](http://192.168.0.242:9001/)


## TÓPICOS MQTT

En esta sección se describen los tópicos a los que se suscribe y a los que publica el programa.


### Tópico JSON
En esté tópico se controlan las salidas del Iboot:

```
oan/control/1.5m/consola-ibb/json
```

El contenido del mensaje a enviar (payload) es un objeto json con los siguientes campos.

Diccionario JSON:

```
    {
    'SALIDA_1': 1,
    'SALIDA_2': 0,
    'SALIDA_3': 0,
    'SALIDA_4': 0,
    'SALIDA_5': 0,
    'SALIDA_6': 0,
    'SALIDA_7': 0,
    'SALIDA_8': 0
    }
```

Con el uso del diccionario anterior se envia la instrucción de encendido de la SALIDA_1:

```
mosquitto_pub -h 192.168.0.243 -t oan/control/1.5m/consola-ibb/json -m (Diccionario JSON)
```


### Tópico PIDEESTADO
En este tópico se realiza la petición de publicar el estado actual de las salidas del Iboot:

```
oan/control/1.5m/consola-ibb/pideestado
```

El contenido del mensaje a enviar (payload) es cualquier mensaje y automaticamente se publicara el estado
actual de las salidas del Iboot en el Tópico ESTADO.

Ejemplo:

```
mosquitto_pub -h 192.168.0.243 -t oan/control/1.5m/consola-ibb/pideestado -n
```


### Tópico ESTADO
En este tópico se publica el estado actual de las salidas del Iboot:

```
oan/control/1.5m/consola-ibb/estado
```

El programa automaticamente publica el estado cada 5 minutos,
aunque se puede forzar la publicación del estado con el uso del topico anterior.

El contenido del mensaje publicado (payload) es un objeto json con los siguientes campos.

Ejemplo:

```
    {
    'SALIDA_1': 'ON',
    'SALIDA_2': 'OFF',
    'SALIDA_3': 'OFF',
    'SALIDA_4': 'OFF',
    'SALIDA_5': 'ON',
    'SALIDA_6': 'OFF',
    'SALIDA_7': 'OFF',
    'SALIDA_8': 'ON',
    'AMPERAJE': '0.5'
    }
```
