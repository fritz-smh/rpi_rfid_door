#!/usr/bin/python

from rpi_libs.led import Led
from rpi_libs.rfid_serial_mfrc522 import RfidSerialMFRC522
import threading
import signal
import sys

### handle ctrl-c ######################################

def signal_handler(signal, frame):
    print("You pressed Ctrl+C!")
    sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)


### Configuration ######################################

STATUS_LED_PIN = 7
SERIAL_RFID_DEVICE = "/dev/ttyAMA0"


### Classes ############################################
class RfidDoor:

    def __init__(self):
        """ Init the engine
        """
        # Define the status led
        self.status_led = Led("Status led", STATUS_LED_PIN)

        # make the led blink 5 times quickly to say it is starting
        self.status_led.blink_n(5)

        # Define the rfid device
        self.rfid = RfidSerialMFRC522(SERIAL_RFID_DEVICE)

        # make the led blink 3 seconds to say the rfid has been successfully initiated
        self.status_led.blink(3000)

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
        if rfid_id == "1761ab7a":
            self.access_granted()
        else:
            self.access_denied()
 

    def access_granted(self):
        """ Access granted
        """
        self.status_led.blink(2)

    def access_denied(self):
        """ Access denied
        """
        self.status_led.blink_n(5)


if __name__ == "__main__":
    rfid_door = RfidDoor()
    rfid_door.listen_rfid()
    


