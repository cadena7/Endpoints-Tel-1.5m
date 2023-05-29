#!/usr/bin/env python3

'''
IBOOT - RACK TEL 1.5M ENDPOINT MQTT
Version 0.2-dev          12/Dic/2022
Edgar Omar Cadena Zepeda
IA-UNAM-ENS
cadena@astro.unam.mx

Ejemplos con Mosquitto:

mosquitto_sub -h 192.168.0.243 -t oan/control/1.5m/rack-ibb/# -d
mosquitto_sub -h 192.168.0.243 -t oan/control/1.5m/rack-ibb/estado

mosquitto_pub -h 192.168.0.243 -t oan/control/1.5m/rack-ibb/1 -m 1
mosquitto_pub -h 192.168.0.243 -t oan/control/1.5m/rack-ibb/1 -m 0
mosquitto_pub -h 192.168.0.243 -t oan/control/1.5m/rack-ibb/pideestado -n

Funciones Añadidas:

Ver. 0.2 - Peticiones de estado ahora envian datos almacendados en el programa
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

# TELNET IP
TELNET_IP = "192.168.0.251"
USER = "admin"
PASSWORD = "admin"

# MQTT IP
IBOOT_IP = "192.168.0.251"
MQTT_HOST = "192.168.0.243"
#MQTT_HOST = "localhost"

MQTT_TOPIC = "oan/control/1.5m/rack-ibb/#"

MQTT_OUT_1 = "oan/control/1.5m/rack-ibb/1"
MQTT_OUT_2 = "oan/control/1.5m/rack-ibb/2"
MQTT_OUT_3 = "oan/control/1.5m/rack-ibb/3"
MQTT_OUT_4 = "oan/control/1.5m/rack-ibb/4"
MQTT_OUT_5 = "oan/control/1.5m/rack-ibb/5"
MQTT_OUT_6 = "oan/control/1.5m/rack-ibb/6"
MQTT_OUT_7 = "oan/control/1.5m/rack-ibb/7"
MQTT_OUT_8 = "oan/control/1.5m/rack-ibb/8"
MQTT_PIDE_ESTADO = "oan/control/1.5m/rack-ibb/pideestado"
MQTT_ESTADO = "oan/control/1.5m/rack-ibb/estado"
MQTT_JSON = "oan/control/1.5m/rack-ibb/json"

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
            time.sleep(1)
        if 'SALIDA_2' in statusjson:                                     #2
            iboot(2, str(statusjson['SALIDA_2']))
            time.sleep(1)
        if 'SALIDA_3' in statusjson:                                     #3
            iboot(3, str(statusjson['SALIDA_3']))
            time.sleep(1)
        if 'SALIDA_4' in statusjson:                                     #4
            iboot(4, str(statusjson['SALIDA_4']))
            time.sleep(1)
        if 'SALIDA_5' in statusjson:                                     #5
            iboot(5, str(statusjson['SALIDA_5']))
            time.sleep(1)
        if 'SALIDA_6' in statusjson:                                     #6
            iboot(6, str(statusjson['SALIDA_6']))
            time.sleep(1)
        if 'SALIDA_7' in statusjson:                                     #7
            iboot(7, str(statusjson['SALIDA_7']))
            time.sleep(1)
        if 'SALIDA_8' in statusjson:                                     #8
            iboot(8, str(statusjson['SALIDA_8']))
            time.sleep(1)


#Loop que publica los datos de estado en el broker MQTT
class MQTTLOOP(Thread):
    def __init__(self):
        Thread.__init__(self)
        print ("[+] Inicia thread de monitoreo de estado y publicacion en MQTT")

    def run(self):
        while True :
            estadojson()
            #actualiza el estado en MQTT cada 30 segundos
            time.sleep(30)


def iboot(salida, accion):
    time.sleep(1)
    if accion == "1":
        try:
            child = pexpect.spawn("telnet " + TELNET_IP, timeout=5)
            child.expect("Name: ")
            child.sendline(USER)
            child.expect("Password: ")
            child.sendline(PASSWORD)
            child.expect("iBootBar >")
            child.sendline("set outlet " + str(salida) + " on \r")
            child.expect("OK")
            child.close()
            result = child.signalstatus
            if result == 1:
                print ("[+] ENCENDIO SALIDA " + str(salida))
            else:
                print ("[-] ERROR ENCENDIENDO SALIDA " + str(salida))
        except:
            print ("[-] PASO EL ERROR ENCENDIENDO SALIDA POR TELNET")
            pass
    else:
        try:
            child = pexpect.spawn("telnet " + TELNET_IP, timeout=5)
            child.expect("Name: ")
            child.sendline(USER)
            child.expect("Password: ")
            child.sendline(PASSWORD)
            child.expect("iBootBar >")
            child.sendline("set outlet " + str(salida) + " off \r")
            child.expect("OK")
            child.close()
            result = child.signalstatus
            if result == 1:
                print ("[+] APAGO SALIDA " + str(salida))
            else:
                print ("[-] ERROR APAGANDO SALIDA " + str(salida))
        except:
            print ("[-] PASO EL ERROR APAGANDO SALIDA POR TELNET")
            pass


def estadojson():
    global salida
    time.sleep(1)
    try:
        status = pexpect.spawn("telnet " + TELNET_IP, timeout=5)
        status.expect("Name: ")
        status.sendline(USER)
        status.expect("Password: ")
        status.sendline(PASSWORD)
        status.expect("iBootBar >")
        status.sendline("get outlets \r")
        status.expect("OK")
        a = status.before.decode('utf-8')
        #print (a)
        status.close()
        result = status.signalstatus
        if result == 1:
            print ("[+] PIDIO ESTADO")
        else:
            print ("[-] ERROR PIDIENDO ESTADO POR TELNET")
        a1 = a[a.find("ibb")+3:]
        a2 = " ".join( a1.split())
        a3 = a2.split()
        #print (a3)
        a4 = [("OFF", "ON")[i == 'N'] for i in a3]
        #print (a4)
        #print (a3[8])
        salida = {
            'SALIDA_1': a4[0],
            'SALIDA_2': a4[1],
            'SALIDA_3': a4[2],
            'SALIDA_4': a4[3],
            'SALIDA_5': a4[4],
            'SALIDA_6': a4[5],
            'SALIDA_7': a4[6],
            'SALIDA_8': a4[7],
            'AMPERAJE': a3[8]
            }
        salida_json = json.dumps(salida, separators=(',', ':'), sort_keys=True) #data serialized
        client.publish(MQTT_ESTADO, salida_json, retain=True)
        print ("[+] ESTADO POR TELNET ENVIADO OK")

    except:
        print ("[-] PASO EL ERROR PIDIENDO ESTADO POR TELNET")
        pass


def enviajson():
    global salida
    time.sleep(0.20)
    try:
        salida_json = json.dumps(salida, separators=(',', ':'), sort_keys=True) #data serialized
        client.publish(MQTT_ESTADO, salida_json, retain=True)
        print ("[+] ESTADO ALMACENADO ENVIADO OK")

    except:
        print ("[-] PASO EL ERROR ENVIANDO ESTADO POR MQTT")
        pass


# Programa Principal
try:
    print ("[+] INTERPRETE MQTT DEL IBOOT_RACK_1.5M Iniciado! Presione CTRL+C para Salir")
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

