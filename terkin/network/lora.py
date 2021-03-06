# -*- coding: utf-8 -*-
# (c) 2019 Richard Pobering <richard@hiveeyes.org>
# (c) 2019 Andreas Motl <andreas@hiveeyes.org>
# License: GNU General Public License, Version 3
import time
import binascii
from terkin import logging

log = logging.getLogger(__name__)


class LoRaManager:

    def __init__(self, manager, settings):
        self.manager = manager
        self.settings = settings

        # LoRa settings.
        self.otaa_settings = self.settings.get('networking.lora.otaa')
        #self.generated_device_eui = binascii.hexlify(LoRa().mac())

    def start(self):
        self.start_lora_join()
        self.wait_for_lora_join(42)

        time.sleep(2.5)

        if self.lora_joined:
            self.create_lora_socket()
        else:
            log.error("[LoRa] Could not join network")

    def start_lora_join(self):

        from network import LoRa

        #pycom.rgbled(0x0f0000) # red
        #self.lora = LoRa(mode=LoRa.LORAWAN, region=self.otaa_settings['region'])
        self.lora = LoRa(mode=LoRa.LORAWAN, region=LoRa.EU868)

        # Create LoRaWAN OTAA connection to TTN.
        app_eui = binascii.unhexlify(self.otaa_settings['application_eui'])
        app_key = binascii.unhexlify(self.otaa_settings['application_key'])

        # Remark: For Pycom Nanogateway.
        # Set the 3 default channels to the same frequency (must be before sending the otaa join request)
        #self.lora.add_channel(0, frequency=self.otaa_settings['frequency'], dr_min=0, dr_max=5)
        #self.lora.add_channel(1, frequency=self.otaa_settings['frequency'], dr_min=0, dr_max=5)
        #self.lora.add_channel(2, frequency=self.otaa_settings['frequency'], dr_min=0, dr_max=5)

        if self.otaa_settings.get('device_eui') is None:
            self.lora.join(activation=LoRa.OTAA, auth=(app_eui, app_key), timeout=0)
        else:
            dev_eui = binascii.unhexlify(self.otaa_settings['device_eui'])
            self.lora.join(activation=LoRa.OTAA, auth=(dev_eui, app_eui, app_key), timeout=0)

    def wait_for_lora_join(self, attempts):
        self.lora_joined = None
        for i in range(0, attempts):
            while not self.lora.has_joined():
                time.sleep(2.5)
                #pycom.rgbled(0x0f0f00) # yellow
                time.sleep(0.1)
                log.info('[LoRA] Not joined yet...')
                #pycom.rgbled(0x000000) # off

        self.lora_joined = self.lora.has_joined()

        if self.lora_joined:
            log.info('[LoRA] joined...')
        else:
            log.info('[LoRa] did not join in %s attempts', attempts)

        #for i in range(3, 16):
        #    self.lora.remove_channel(i)

        return self.lora_joined

    def create_lora_socket(self):
        # create a lora socket

        self.lora_socket = None
        self.socket = socket.socket(socket.AF_LORA, socket.SOCK_RAW)

        # set the LoRaWAN data rate
        #self.socket.setsockopt(socket.SOL_LORA, socket.SO_DR, self.otaa_settings['datarate'])
        self.socket.setsockopt(socket.SOL_LORA, socket.SO_DR, self.otaa_settings['datarate'])
        # make the socket non-blocking
        self.socket.setblocking(False)

        self.lora_socket = True
        log.info('[LoRa] socket created')

        for i in range(0,2):
            #pycom.rgbled(0x000f00) # green
            time.sleep(0.1)
            #pycom.rgbled(0x000000) # off

        time.sleep(4.0)
        return self.lora_socket

    def lora_send(self, payload):
        success = self.socket.send(payload)
        for i in range(0,2):
            #pycom.rgbled(0x00000f) # green
            time.sleep(0.1)
            #pycom.rgbled(0x000000) # off

        return success

    def lora_receive(self):
        rx, port = self.socket.recvfrom(256)
        if rx:
            #pycom.rgbled(0x000f00) # green
            log.info('[LoRa] Received: {}, on port: {}'.format(rx, port))
            #pycom.rgbled(0x000f00) # green
        time.sleep(6)

        return rx, port
