#!/usr/bin/python
# -*- coding: utf-8 -*-

from rpi_libs.led import Led
from rpi_libs.relay import Relay
from rpi_libs.rfid_serial_mfrc522 import RfidSerialMFRC522
from common.mailsender import MailSender
from common.security import Security
from common.config import Config
import threading
import signal
import sys
import os
import logging


### handle ctrl-c ######################################

def signal_handler(signal, frame):
    logging.error("You pressed Ctrl+C!")
    sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)


### Configuration ######################################

CONFIG_FILE = "{0}/config.json".format(os.path.dirname(os.path.abspath(__file__)))
PID_FILE = "/var/log/rfid_door/rfid_door.pid"
LOG_FOLDER = "/var/log/rfid_door/"

### Classes ############################################
class RfidDoor:

    def __init__(self):
        """ Init the engine
        """
        logging.info("Starting RfidDoor")
        # Read the config
        logging.info("Read the configuration")
        config = Config(CONFIG_FILE)
        status_led_pin = int(config.get_value_for("status_led_pin"))
        door_relay_pin = int(config.get_value_for("door_relay_pin"))
        serial_rfid_device = config.get_value_for("serial_rfid_device")
        smtp_server = config.get_value_for("smtp_server")
        self.my_email = config.get_value_for("my_email")

        # Define the status led
        logging.info("Setup status led")
        self.status_led = Led("Status led", status_led_pin)

        # make the led blink 5 times quickly to say it is starting
        self.status_led.blink_n(5)

        # Define the rfid device
        logging.info("Setup rfid device")
        self.rfid = RfidSerialMFRC522(serial_rfid_device)

        # make the led blink 3 seconds to say the rfid has been successfully initiated
        self.status_led.blink(3000)

        # Define the relay 
        logging.info("Setup relay")
        self.door_relay = Relay("Door relay", door_relay_pin)

        # Create the mail sender
        logging.info("Setup email sender")
        self.mail_sender = MailSender(smtp_server)
        # send an email to tell the script is starting (will help to detect some unusual reboot)
        self.mail_sender.send("Rfid door : starts!", self.my_email, self.my_email, "Rfid door script has just started")
 
        # Init the security manager
        logging.info("Setup the security manager")
        self.security = Security(CONFIG_FILE)


    def listen_rfid(self):
        """ Listen to the rfid device
        """
        logging.info("Start listening to the rfid device (eternal loop)")
        rfid_thread = threading.Thread(None,
                                       self.rfid.read,
                                       "rfid_read",
                                       (self.cb_rfid_detected,),
                                       {})
        rfid_thread.start()

    def cb_rfid_detected(self, rfid_id):
        """ A rfid item has been detected : process it
            @param rfid_id : id of the rfid item
        """
        if self.security.is_granted(rfid_id):
            self.access_granted(rfid_id)
        else:
            self.access_denied(rfid_id)
 

    def access_granted(self, rfid_id):
        """ Access granted
        """
        self.status_led.blink(2000)
        logging.info("Access granted for '{0}'! Opening the door".format(rfid_id))
        self.mail_sender.send("Rfid door : access granted!", self.my_email, self.my_email, "Access granted for {0}".format(rfid_id))
        # for a hormann garage door motor, just do a pulse of 1s
        self.door_relay.pulse_no()

    def access_denied(self, rfid_id):
        """ Access denied
        """
        self.status_led.blink_n(5)
        logging.warning("Access denied for '{0}'!".format(rfid_id))
        self.mail_sender.send("Rfid door : access denied!", self.my_email, self.my_email, "Access denied for {0}".format(rfid_id))


if __name__ == "__main__":
    # logging
    logging.basicConfig(filename='{0}/rfid_door.log'.format(LOG_FOLDER), level=logging.DEBUG, format='%(asctime)s %(levelname)s %(message)s')
    logging.info('Starting!')

    # first, write the pid in a file 
    with open(PID_FILE, 'w') as pid_file:
        pid_file.write(str(os.getpid()))

    # then, start to play with rfid and the door :)
    rfid_door = RfidDoor()
    rfid_door.listen_rfid()
    logging.info('Finished')
    


