#!/usr/bin/env python3

'''
IBOOT - CONSOLA TEL 1.5M ENDPOINT MQTT TESTER
Version 0.1-dev          19/Oct/2022
Edgar Omar Cadena Zepeda
IA-UNAM-ENS
cadena@astro.unam.mx


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

# TELNET IP

TELNET_IP = "192.168.0.252"
USER = "admin"
PASSWORD = "admin"

# MQTT IP
MQTT_HOST = "192.168.0.243"

MQTT_JSON = "oan/control/1.5m/consola-ibb/json"



def estadojson():
    try:
        salida = {
            'SALIDA_1': 0,
            'SALIDA_2': 1,
            'SALIDA_3': 0,
            'SALIDA_4': 0,
            'SALIDA_5': 1,
            'SALIDA_6': 0,
            'SALIDA_7': 0,
            'SALIDA_8': 1
            }
        salida_json = json.dumps(salida, separators=(',', ':'), sort_keys=True) #data serialized
        client.publish(MQTT_JSON, salida_json, retain=False)
        print ("[+] ESTADO ENVIADO OK")

    except:
        print ("[-] PASO EL ERROR")
        pass


# Programa Principal
try:
    print ("[+] ENVIANDO UN MENSAJE MQTT EN JSON AL ENDPOINT IBOOT_CONSOLA_TEL1.5M")
    client = mqtt.Client()
    client.connect(MQTT_HOST, 1883, 60)
    estadojson()


except (KeyboardInterrupt, SystemExit): # If CTRL+C is pressed, exit cleanly:
    print("Adios Viajero")
    sys.exit()
