# Secundario_endpoint (mqtt)

Programa intermediario entre en control del secundario del eje Z, el cual publuica su posicion y acepta mandos via mqtt.

Solo se pueden accesar los datos desde IP de la UNAM

## Hardware
Desarollado por F. Quiros, tiene un Rabitt con Ip 192.168.0.152 y puerto 3333, solo acepta un cliente
, este endpoint, ya no permite mas accesos.

## Documentacion del programa
El programa esta en python3 con las librerias Endpointlib que corren en un ambiente virtual.

### Dependencias
Depende de:

+ pip3 install paho-mqtt
+ pip3 install endpointlib


## Arranque
Se corre automaticamente mediante el programa supervisor de la pc 192.168.0.242 (control@endpoint-server):

 ``` 
 sudo supervisorctl status
 
iboot_consola                    RUNNING   pid 73272, uptime 0:04:58
mqtt                             RUNNING   pid 73273, uptime 0:04:58
secundario                       RUNNING   pid 73274, uptime 0:04:58
```

## TÓPICOS

En esta sección se describen los tópicos que publica el programa.

### Topico info
El unico topico que se publica peridicamente es:
```
'oan/control/1.5m/secundario/status/response'
```
El contenido del mensaje publicado (payload) es un objeto json con los siguientes campos.

Ejemplo:
```
{'posicion': 49.0, 'sw_down': 0, 'sw_up': 0, 'is_init': False}
```
Donde:
* posicion: Es la posicion actual del eje z del secundario
* sw_down: Estado del interruptor inferior
* sw_up: Estado del interruptor superior
* is_init: Es una bandera de software (no del harware) que indica si ya se a inicializado el secundario.

### TÓPICOS QUE ATIENDE LA CONSOLA
El programa atiende los siguientes tópicos.
* oan/control/1.5m/secundario/incializa
* oan/control/1.5m/secundario/incrementa
* oan/control/1.5m/secundario/decrementa
* oan/control/1.5m/secundario/mueve

### TÓPICOS inicializa
Inicializa el eje de foco del secundario.
No importa el payload que se mande.

### TÓPICOS incrementa
Mueve el foco del secundario hacia arriba de forma relativa a la posicion actual. 
El payload es la cantidad del incremento que se movera.

### TÓPICOS decrementa
Mueve el foco del secundario hacia abajo de forma relativa a la posicion actual. 
El payload es la cantidad del decremento que se movera.

### TÓPICOS mueve

Mueve el foco del secundario hacia una posicion absoluta, definida por el payload recibido.
