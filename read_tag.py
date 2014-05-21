#!/usr/bin/python
# -*- coding: utf-8 -*-


from rpi_libs.rfid_serial_mfrc522 import RfidSerialMFRC522
from common.config import Config

### Configuration ######################################

CONFIG_FILE = "config.json"

### Classes ############################################
class RfidDoorHelper:

    def __init__(self):
        """ Init the engine
        """
        # Read the config
        config = Config(CONFIG_FILE)
        serial_rfid_device = config.get_value_for("serial_rfid_device")

        # Define the rfid device
        self.rfid = RfidSerialMFRC522(serial_rfid_device)

    def listen_rfid(self):
        """ Listen to the rfid device
        """
        self.rfid.read(self.cb_rfid_detected)

    def cb_rfid_detected(self, rfid_id):
        """ A rfid item has been detected : process it
            @param rfid_id : id of the rfid item
        """
        pass


if __name__ == "__main__":
    rfid_door_helper = RfidDoorHelper()
    rfid_door_helper.listen_rfid()
    


