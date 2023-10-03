#!/usr/bin/env python3

'''
IBOOT - CONSOLA TEL 1.5M ENDPOINT MQTT
Version 0.1-dev          28/Ene/2023
Edgar Omar Cadena Zepeda
IA-UNAM-ENS
cadena@astro.unam.mx

Ejemplos con Mosquitto:

mosquitto_sub -h 192.168.0.243 -t oan/control/1.5m/consola-ibb/# -d
mosquitto_sub -h 192.168.0.243 -t oan/control/1.5m/consola-ibb/estado

mosquitto_pub -h 192.168.0.243 -t oan/control/1.5m/consola-ibb/1 -m 1
mosquitto_pub -h 192.168.0.243 -t oan/control/1.5m/consola-ibb/1 -m 0
mosquitto_pub -h 192.168.0.243 -t oan/control/1.5m/consola-ibb/pideestado -n

Funciones Añadidas:

Ver. 0.1 - En Desarrollo
'''



# Modulos externos
import time, datetime
import os
import sys
import paho.mqtt.client as mqtt
import subprocess
from threading import Thread
import simplejson as json
import pexpect

# RASPBERRY PI IP
RPI_IP = "nc 192.168.0.252 5555"
LOCAL_IP = "nc localhost 5555"

# MQTT IP
MQTT_HOST = "192.168.0.243"
#MQTT_HOST = "localhost"

MQTT_TOPIC = "oan/control/1.5m/consola-ibb/#"

MQTT_OUT_1 = "oan/control/1.5m/consola-ibb/1"
MQTT_OUT_2 = "oan/control/1.5m/consola-ibb/2"
MQTT_OUT_3 = "oan/control/1.5m/consola-ibb/3"
MQTT_OUT_4 = "oan/control/1.5m/consola-ibb/4"
MQTT_OUT_5 = "oan/control/1.5m/consola-ibb/5"
MQTT_OUT_6 = "oan/control/1.5m/consola-ibb/6"
MQTT_OUT_7 = "oan/control/1.5m/consola-ibb/7"
MQTT_OUT_8 = "oan/control/1.5m/consola-ibb/8"
MQTT_PIDE_ESTADO = "oan/control/1.5m/consola-ibb/pideestado"
MQTT_ESTADO = "oan/control/1.5m/consola-ibb/estado"
MQTT_JSON = "oan/control/1.5m/consola-ibb/json"

# Global variable
salida = {
    'SALIDA_1': "OFF",
    'SALIDA_2': "OFF",
    'SALIDA_3': "OFF",
    'SALIDA_4': "OFF",
    'SALIDA_5': "OFF",
    'SALIDA_6': "OFF",
    'SALIDA_7': "OFF",
    'SALIDA_8': "OFF",
    'AMPERAJE': "0"
    }


# MQTT on_connect
def on_connect(client, user_data, flags, rc):
    print("Resultado de conexion: " + str(rc))
    client.subscribe(MQTT_TOPIC)
    print("Conectado a: " + MQTT_TOPIC)


# MQTT on_message
def on_message(client, user_data, msg):
    #status = str(msg.payload)
    #print("Received message '" + str(msg.payload.decode("utf-8")) + "' on topic '" + str(msg.topic) + "' with QoS " + str(msg.qos))
    topic = str(msg.topic)   # decodificar la string
    status = str(msg.payload.decode("utf-8"))   # decodificar la string
    status2 = status.upper() # convertir a mayusculas
    print("Topico MQTT: " + topic + " Mensaje MQTT: " + status)

    if topic == MQTT_OUT_1:
        iboot(1, status2)
        time.sleep(1)

    elif topic == MQTT_OUT_2:
        iboot(2, status2)
        time.sleep(1)

    elif topic == MQTT_OUT_3:
        iboot(3, status2)
        time.sleep(1)

    elif topic == MQTT_OUT_4:
        iboot(4, status2)
        time.sleep(1)

    elif topic == MQTT_OUT_5:
        iboot(5, status2)
        time.sleep(1)

    elif topic == MQTT_OUT_6:
        iboot(6, status2)
        time.sleep(1)

    elif topic == MQTT_OUT_7:
        iboot(7, status2)
        time.sleep(1)

    elif topic == MQTT_OUT_8:
        iboot(8, status2)
        time.sleep(1)

    elif topic == MQTT_PIDE_ESTADO:
        #estadojson()
        enviajson()
        time.sleep(1)

    elif topic == MQTT_JSON:
        statusjson = json.loads(status)
        print(statusjson)
        if 'SALIDA_1' in statusjson:                                     #1
            iboot(1, str(statusjson['SALIDA_1']))
            time.sleep(0.2)
        if 'SALIDA_2' in statusjson:                                     #2
            iboot(2, str(statusjson['SALIDA_2']))
            time.sleep(0.2)
        if 'SALIDA_3' in statusjson:                                     #3
            iboot(3, str(statusjson['SALIDA_3']))
            time.sleep(0.2)
        if 'SALIDA_4' in statusjson:                                     #4
            iboot(4, str(statusjson['SALIDA_4']))
            time.sleep(0.2)
        if 'SALIDA_5' in statusjson:                                     #5
            iboot(5, str(statusjson['SALIDA_5']))
            time.sleep(0.2)
        if 'SALIDA_6' in statusjson:                                     #6
            iboot(6, str(statusjson['SALIDA_6']))
            time.sleep(0.2)
        if 'SALIDA_7' in statusjson:                                     #7
            iboot(7, str(statusjson['SALIDA_7']))
            time.sleep(0.2)
        if 'SALIDA_8' in statusjson:                                     #8
            iboot(8, str(statusjson['SALIDA_8']))
            time.sleep(0.2)


#Loop que publica los datos de estado en el broker MQTT
class MQTTLOOP(Thread):
    def __init__(self):
        Thread.__init__(self)
        print ("[+] Inicia thread de monitoreo de estado y publicacion en MQTT")

    def run(self):
        while True :
            estadojson()
            #actualiza el estado en MQTT cada 5 segundos
            time.sleep(5)


def iboot(salida, accion):
    time.sleep(0.5)
    if accion == "1":
        try:
            out = subprocess.Popen(RPI_IP, shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr = subprocess.PIPE)
            print ("[+] ENCENDIENDO SALIDA " + str(salida))
            out1 = out.communicate(str.encode("ON " + str(salida)))
            out.kill()
            print ("[+] ENCENDIO SALIDA " + str(salida))
        except:
            print ("[-]ERROR ENCENDIENDO SALIDA " + str(salida))
            pass
    else:
        try:
            out = subprocess.Popen(RPI_IP, shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr = subprocess.PIPE)
            print ("[+] APAGANDO SALIDA " + str(salida))
            out1 = out.communicate(str.encode("OFF " + str(salida)))
            out.kill()
            print ("[+] APAGO SALIDA " + str(salida))
        except:
            print ("[-]ERROR APAGANDO SALIDA " + str(salida))
            pass


def estadojson():
    global salidas
    time.sleep(0.5)
    try:
        estado = subprocess.Popen(RPI_IP, shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr = subprocess.PIPE)
        estado1 = estado.communicate(str.encode("ESTADO"))[0]  #regresa un tuple [0,1]
        print ("[+] SOLICITANDO VARIABLES ACTUALES DE ESTADO")
        #print(estado1)
        estadojson = estado1.decode('utf-8')    #decodificar el mensaje
        #print(estadojson)
        estado.kill()
        estadojson1 = json.loads(estadojson) #viejos nombres
        print ("[+] PETICION DE ESTADO OK")
        if estadojson1['SALIDA_1'] == "1":
            estadojson1['SALIDA_1'] = "ON"
        else:
            estadojson1['SALIDA_1'] = "OFF"

        if estadojson1['SALIDA_2'] == "1":
            estadojson1['SALIDA_2'] = "ON"
        else:
            estadojson1['SALIDA_2'] = "OFF"

        if estadojson1['SALIDA_3'] == "1":
            estadojson1['SALIDA_3'] = "ON"
        else:
            estadojson1['SALIDA_3'] = "OFF"

        if estadojson1['SALIDA_4'] == "1":
            estadojson1['SALIDA_4'] = "ON"
        else:
            estadojson1['SALIDA_4'] = "OFF"

        if estadojson1['SALIDA_5'] == "1":
            estadojson1['SALIDA_5'] = "ON"
        else:
            estadojson1['SALIDA_5'] = "OFF"

        if estadojson1['SALIDA_6'] == "1":
            estadojson1['SALIDA_6'] = "ON"
        else:
            estadojson1['SALIDA_6'] = "OFF"

        if estadojson1['SALIDA_7'] == "1":
            estadojson1['SALIDA_7'] = "ON"
        else:
            estadojson1['SALIDA_7'] = "OFF"

        if estadojson1['SALIDA_8'] == "1":
            estadojson1['SALIDA_8'] = "ON"
        else:
            estadojson1['SALIDA_8'] = "OFF"

        salidas = {
            'SALIDA_1': estadojson1['SALIDA_1'],
            'SALIDA_2': estadojson1['SALIDA_2'],
            'SALIDA_3': estadojson1['SALIDA_3'],
            'SALIDA_4': estadojson1['SALIDA_4'],
            'SALIDA_5': estadojson1['SALIDA_5'],
            'SALIDA_6': estadojson1['SALIDA_6'],
            'SALIDA_7': estadojson1['SALIDA_7'],
            'SALIDA_8': estadojson1['SALIDA_8'],
            'AMPERAJE': estadojson1['AMPERAJE']
            }
        salida_json = json.dumps(salidas, separators=(',', ':'), sort_keys=True) #data serialized
        client.publish(MQTT_ESTADO, salida_json, retain=True)
        print ("[+] ESTADO ENVIADO OK")

    except:
        print ("[-] PASO EL ERROR PIDIENDO ESTADO")
        pass


def enviajson():
    global salidas
    time.sleep(0.20)
    try:
        salida_json = json.dumps(salidas, separators=(',', ':'), sort_keys=True) #data serialized
        client.publish(MQTT_ESTADO, salida_json, retain=True)
        print ("[+] ESTADO ALMACENADO ENVIADO OK")

    except:
        print ("[-] PASO EL ERROR ENVIANDO ESTADO POR MQTT")
        pass

# Programa Principal
try:
    print ("[+] INTERPRETE MQTT DEL IBOOT_CONSOLA_1.5M Iniciado! Presione CTRL+C para Salir")
    client = mqtt.Client()
    client.connect(MQTT_HOST, 1883, 60)
    client.on_connect = on_connect
    client.on_message = on_message
    #client.loop_start()

    MQTTloop = MQTTLOOP()
    MQTTloop.setDaemon(True)
    MQTTloop.start()

    client.loop_forever()


except (KeyboardInterrupt, SystemExit): # If CTRL+C is pressed, exit cleanly:
    print("Adios Viajero")
    client.loop_stop()
    sys.exit()
