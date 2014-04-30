#!/usr/bin/python

from rpi_libs.led import Led
from rpi_libs.relay import Relay
from rpi_libs.rfid_serial_mfrc522 import RfidSerialMFRC522
from common.mailsender import MailSender
from common.security import Security
from common.config import Config
import threading
import signal
import sys

### handle ctrl-c ######################################

def signal_handler(signal, frame):
    print("You pressed Ctrl+C!")
    sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)


### Configuration ######################################

CONFIG_FILE = "config.json"

#STATUS_LED_PIN = 7
#DOOR_RELAY_PIN = 11
#SERIAL_RFID_DEVICE = "/dev/ttyAMA0"
#SMTP_SERVER = "smtp.free.fr"
#MY_EMAIL = "frederic.le.roy@free.fr"


### Classes ############################################
class RfidDoor:

    def __init__(self):
        """ Init the engine
        """
        # Read the config
        config = Config(CONFIG_FILE)
        status_led_pin = int(config.get_value_for("status_led_pin"))
        door_relay_pin = int(config.get_value_for("door_relay_pin"))
        serial_rfid_device = config.get_value_for("serial_rfid_device")
        smtp_server = config.get_value_for("smtp_server")
        self.my_email = config.get_value_for("my_email")

        # Define the status led
        self.status_led = Led("Status led", status_led_pin)

        # make the led blink 5 times quickly to say it is starting
        self.status_led.blink_n(5)

        # Define the rfid device
        self.rfid = RfidSerialMFRC522(serial_rfid_device)

        # make the led blink 3 seconds to say the rfid has been successfully initiated
        self.status_led.blink(3000)

        # Define the relay 
        self.door_relay = Relay("Door relay", door_relay_pin)

        # Create the mail sender
        self.mail_sender = MailSender(smtp_server)
        # send an email to tell the script is starting (will help to detect some unusual reboot)
        self.mail_sender.send("Rfid door : starts!", self.my_email, self.my_email, "Rfid door script has just started")
 
        # Init the security manager
        self.security = Security(CONFIG_FILE)


    def listen_rfid(self):
        """ Listen to the rfid device
        """
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
        print("Rfid item detected. Id is '{0}'".format(rfid_id))
        # TODO :this is just some test right now
        #if rfid_id == "1761ab7a":
        if self.security.is_granted(rfid_id):
            self.access_granted(rfid_id)
        else:
            self.access_denied(rfid_id)
 

    def access_granted(self, rfid_id):
        """ Access granted
        """
        self.status_led.blink(2000)
        print("Access granted! Opening the door")
        self.mail_sender.send("Rfid door : access granted!", self.my_email, self.my_email, "Access granted for {0}".format(rfid_id))
        # for a hormann garage door motor, just do a pulse of 1s
        self.door_relay.pulse()

    def access_denied(self, rfid_id):
        """ Access denied
        """
        self.status_led.blink_n(5)
        print("Access denied!")
        self.mail_sender.send("Rfid door : access denied!", self.my_email, self.my_email, "Access denied for {0}".format(rfid_id))


if __name__ == "__main__":
    rfid_door = RfidDoor()
    rfid_door.listen_rfid()
    


