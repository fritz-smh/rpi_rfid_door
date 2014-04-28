rpi_rfid_door
=============

Open some motorized doors with rfid items

Dependencies
------------

Depends on *rpi_libs* : https://github.com/fritz-smh/rpi_libs


How to wire it ?
----------------

TODO : explain

Install
-------

Clone the repositories :
* this one
* rpi_libs

In this copy of the repository : 
* edit *start.sh* to set the PYTHONPATH to the folder containing *rpi_libs*.
* run start.sh

Start sequence
--------------

When the program is starting :
* the led will blink 5 times very quickly before doing anything else
* when the rfid reader is set, the led will be on for 3 seconds
* the led will be off until any event occurs

Led and events
--------------

TODO
