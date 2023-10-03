# RUCA 2: RUEDA DE FILTROS - MQTT

Maneja la operación de la rueda de filtros RUCA 2.

## Documentación del Programa

El programa esta en lenguaje Python3 se encarga de la comunicación entre
la rueda de filtros la Ruca 2 y el broker MQTT.

### Dependencias

Depende de:

+ pip3 install simplejson
+ pip3 install paho-mqtt

## Arranque

Se encuentra configurado el arranque automatico mediante el paquete supervisor.

Para reiniciar el proceso en una terminal de comandos ejecute la siguiente instrucción:

> - sudo supervisorctl restart ruca2

También es posible accesar a la interfaz web de supervisor en el siguiente enlace:

> - [supervisor webpage](http://192.168.0.242:9001/)


## TÓPICOS MQTT

En esta sección se describen los tópicos a los que se suscribe y a los que publica el programa.


### Tópico CONTROL
En esté tópico realiza acciones de control general del instrumento:

```
oan/control/1.5m/ruca2/control
```

El contenido del mensaje a enviar (payload) es una string, cuenta con los  los siguientes comandos habilitados.

- INICIO: para enviar el comando de inicialización del instrumento, ejemplo:

```
mosquitto_pub -h 192.168.0.243 -t oan/control/1.5m/ruca2/control -m INICIO
```

- ESTADO: regresa las variables del estado actual del instrumento y los publica en el tópico ESTADO, ejemplo:

```
mosquitto_pub -h 192.168.0.243 -t oan/control/1.5m/ruca2/control -m ESTADO
```

- NOMBRES: regresa el nombre de los filtros, polarizados y reductores instalados en el instrumento y los publica en el tópico NOMBRES, ejemplo:

```
mosquitto_pub -h 192.168.0.243 -t oan/control/1.5m/ruca2/control -m NOMBRES
```


### Tópico ESTADO
En este tópico se publica el estado actual del instrumento:

```
oan/control/1.5m/ruca2/estado
```

El programa automaticamente publica el estado cada 60 segundos,
aunque se puede forzar la publicación instantánea con el uso del topico CONTROL.

El contenido del mensaje publicado (payload) es un objeto json con los siguientes campos.

Diccionario JSON:

```
        {
        'RUEDA_INICIO': 1,
        'RUEDA_INDICE': 1,
        'POLARIZA_INICIO': 0,
        'POLARIZA_INDICE': 0,
        'REDUCTOR_AZUL': 0,
        'REDUCTOR_ROJO': 1,
        'REDUCTOR_FUERA': 0,
        'REDUCTOR_INDICE': 2,
        'RUEDA_FRENO': 0,
        'POLARIZA_FRENO': 0,
        'REDUCTOR_FRENO': 0,
        'RUEDA_INDICE_SET': 1,
        'POLARIZA_INDICE_SET': 0,
        'REDUCTOR_SET': 2,
        'RUEDA_PASOS': 1,
        'POLARIZA_PASOS': 0,
        'REDUCTOR_PASOS': 20000,
        'FIRST_INIT_RUEDA': 1,
        'FIRST_INIT_POLARIZA': 0,
        'FIRST_INIT_REDUCTOR': 1,
        'RUEDA_FRENO_SENSOR': 1,
        'POLARIZA_FRENO_SENSOR': 0,
        'RUEDA_PARO_EMERGENCIA': 0
        }
```


### Tópico NOMBRES
En este tópico se publica el estado actual del nombre de los filtros, polarizados
y reductores instalados en el instrumento:

```
oan/control/1.5m/ruca2/nombres
```

El programa automaticamente publica los nombres cada 60 segundos,
aunque se puede forzar la publicación instantánea con el uso del topico CONTROL.

El contenido del mensaje publicado (payload) es un objeto json con los siguientes campos.

Diccionario JSON:

```
        {
        'Filtro01': FILTRO_01,
        'Filtro02': FILTRO_02,
        'Filtro03': FILTRO_03,
        'Filtro04': FILTRO_04,
        'Filtro05': FILTRO_05,
        'Filtro06': FILTRO_06,
        'Filtro07': FILTRO_07,
        'Filtro08': FILTRO_08,
        'Polariza01': POLARIZA_01,
        'Polariza02': POLARIZA_02,
        'Polariza03': POLARIZA_03,
        'Polariza04': POLARIZA_04,
        'Polariza05': POLARIZA_05,
        'Reductor01': REDUCTOR_01,
        'Reductor02': REDUCTOR_02,
        'Reductor03': REDUCTOR_03
        }
```


### Tópico RUEDA
En este tópico se realiza la petición de posicionar la rueda de filtros en uno de los 8 espacios:

```
oan/control/1.5m/consola-ibb/rueda
```

El contenido del mensaje a enviar (payload) es una string del 1 al 8 para elegir la posición deseada.

Ejemplo para solicitar el filtro en la posición número 5:

```
mosquitto_pub -h 192.168.0.243 -t oan/control/1.5m/ruca2/rueda -m 5
```


### Tópico POLARIZADOR
En este tópico se realiza la petición de posicionar la rueda de polarizadores en uno de los 5 espacios:
**Actualmente esta rueda se encuentra desmontada.**
```
oan/control/1.5m/consola-ibb/polarizador
```

El contenido del mensaje a enviar (payload) es una string del 1 al 5 para elegir la posición deseada.

Ejemplo para solicitar el polarizador en la posición número 3:

```
mosquitto_pub -h 192.168.0.243 -t oan/control/1.5m/ruca2/polarizador -m 3
```


### Tópico REDUCTOR
En este tópico se realiza la petición de posicionar el mecanismo de reductores en uno de los 3 espacios:

```
oan/control/1.5m/consola-ibb/reductor
```

El contenido del mensaje a enviar (payload) es una string del 1 al 3 para elegir la posición deseada.

Ejemplo para solicitar el reductor en la posición número 2:

```
mosquitto_pub -h 192.168.0.243 -t oan/control/1.5m/ruca2/reductor -m 2
```


### Tópico CAMBIANOMBRES
En este tópico se cambia el nombre de los filtros, polarizados
y reductores instalados en el instrumento:

```
oan/control/1.5m/ruca2/cambianombres
```

El contenido del mensaje a enviar (payload) es un objeto json con los siguientes campos.

Diccionario JSON:

```
        {
        'Filtro01': N_FILTRO_01,
        'Filtro02': N_FILTRO_02,
        'Filtro03': N_FILTRO_03,
        'Filtro04': N_FILTRO_04,
        'Filtro05': N_FILTRO_05,
        'Filtro06': N_FILTRO_06,
        'Filtro07': N_FILTRO_07,
        'Filtro08': N_FILTRO_08,
        'Polariza01': N_POLARIZA_01,
        'Polariza02': N_POLARIZA_02,
        'Polariza03': N_POLARIZA_03,
        'Polariza04': N_POLARIZA_04,
        'Polariza05': N_POLARIZA_05,
        'Reductor01': N_REDUCTOR_01,
        'Reductor02': N_REDUCTOR_02,
        'Reductor03': N_REDUCTOR_03
        }
```

Ejemplo para solicitar el cambio con nuevos nombres definidos en el diccionario anterior:

```
mosquitto_pub -h 192.168.0.243 -t oan/control/1.5m/ruca2/cambianombres -m (Diccionario JSON)
```

Para verificar la actualización de los nombres se puede esperar a la actualización automática en el Tópico NOMBRES
o si se desea una actualización instantánea mediante el uso del Tópico CONTROL.
