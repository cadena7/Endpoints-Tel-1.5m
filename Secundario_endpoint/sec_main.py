#!/usr/bin/env python3
# -*- coding: utf-8 -*-

'''
E. Colorado - Octubre-2022 V0.1 -inicio
'''
import asyncio
import sys
import json

# Hack for python paths, just for the demo utils
import inspect, os, sys
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(os.path.dirname(currentdir))
sys.path.insert(0, parentdir)
#from utils.demo_helper import DemoHelper
# End Hack

from endpointlib.devices.socket_device import SocketDevice
from endpointlib.endpoints.endpoint_monitor_device import EndpointMonitorDevice
from endpointlib.helpers.loggers.logger_level import LoggerLevel
from endpointlib.helpers.loggers.logger_manager import LoggerManager
from endpointlib.helpers.loggers.logger_settings import LoggerSettings

LoggerManager.create(LoggerSettings.get_debug_settings(level=LoggerLevel.INFO))
logger = LoggerManager.get_async_logger(name='demo_secundario')
###########################################################################
# Inherit from EndpointMonitorDevice that has a socket device to monitor
class DomeEndpoint(EndpointMonitorDevice):
    def __init__(self, host, port, socket_monitor, delay, command):
        super().__init__(host=host, port=port, device=SocketDevice(socket_monitor[0], socket_monitor[1]),
                            delay=delay, command=command)
        self.is_init=False
    ###########################################################################
    # Define callbacks
    def get_handlers(self):
        handlers = dict()
        handlers['oan/control/1.5m/secundario/alto'] = self.on_stop_operation
        handlers['oan/control/1.5m/secundario/incializa'] = self.on_init_operation
        handlers['oan/control/1.5m/secundario/incrementa'] = self.on_increment_operation
        handlers['oan/control/1.5m/secundario/decrementa'] = self.on_decrement_operation
        handlers['oan/control/1.5m/secundario/mueve'] = self.on_move_operation
        handlers['oan/control/1.5m/secundario/redefine'] = self.on_redefine_operation
        return handlers

    ###########################################################################
    # Callback defined to be executed every 10(monitor_interval) seconds
    async def on_monitor(self, status):
        d={}
        s=status.split()
        d['posicion']=float (s[0])
        d['sw_down'] = int(s[1])
        d['sw_up'] = int(s[2])
        d['is_init'] = self.is_init
        print (d)

        await self.publish('oan/control/1.5m/secundario/status/response', json.dumps(d))
        await logger.info('[on_dome_monitor]: ' + status)

    ###########################################################################
    # Callback executed when topic 'oan/control/dome/operation01' is received
    async def on_stop_operation(self, topic, payload):
        response = await self.send_to_device(':D01;')
        await logger.info('[on_stop_operation]Response from device: ' + response)

    ###########################################################################
    # Callback executed when topic 'oan/control/dome/operation02' is received
    async def on_init_operation(self, topic, payload):
        print('Vamos a inicializar');

        #response = await self.send_to_device('INICIALIZA;')
        response = await self.send_to_device(':D02;')
        await self.publish('oan/control/1.5/secundario/events/init', response)
        await logger.info('[on_init_operation]Response from device: ' + response)
        self.is_init=True

    ###########################################################################
    async def on_increment_operation(self, topic, payload):
        print("payload",payload)
        #cmd='INCREMENTO({});'.format(payload)
        cmd=":D055%04X;" % int(payload)
        print(cmd)
        response = await self.send_to_device(cmd)
        await self.publish('oan/control/1.5/secundario/events/increment', response)
        await logger.info('[on_increment_operation]Response from device: ' + response)

    ###########################################################################
    async def on_decrement_operation(self, topic, payload):
        print("payload", payload)
        # cmd='INCREMENTO({});'.format(payload)
        cmd = ":D065%04X;" % int(payload)
        print(cmd)
        response = await self.send_to_device(cmd)
        await self.publish('oan/control/1.5/secundario/events/decrement', response)
        await logger.info('[on_increment_operation]Response from device: ' + response)
###########################################################################
    async def on_move_operation(self, topic, payload):
        print("payload",payload)
        cmd='MUEVE({});'.format(payload)
        print(cmd)
        response = await self.send_to_device(cmd)
        await self.publish('oan/control/1.5/secundario/events/move', response)
        await logger.info('[on_move_operation]Response from device: ' + response)

    ###########################################################################
    async def on_redefine_operation(self, topic, payload):
        print("payload", payload)

        cmd = ":D03%04X;" % int(payload)
        print(cmd)
        response = await self.send_to_device(cmd)
        await self.publish('oan/control/1.5/secundario/events/redefine', response)
        await logger.info('[on_redefine_operation]Response from device: ' + response)


#################################################################################################
async def demo():
    # Creates the user defined class DomeEndpoint
    endpoint = DomeEndpoint(host='192.168.0.243', port=1883, socket_monitor=('192.168.0.152', 3333),
                            delay=5, command='POSICION;')

    # Gather loop_forever and socket server tasks
    #await DemoHelper.run(server_port=10001, endpoint=endpoint)
    await endpoint.run_forever()
    await logger.shutdown()

# In order to execute async loop you must start with this instruction 'asyncio.run(tasks...)'
asyncio.run(demo(), debug=True)