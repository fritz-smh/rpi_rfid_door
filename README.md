rpi_rfid_door
=============

Open some motorized doors with rfid items

This is a project for the Raspberry Pi system.



Rpi configuration
-----------------

In order to use the dedicated UART pins on the raspberry pi, first they have to be removed from their default application which is debugging.
To do this edit */boot/cmdline.txt* and */etc/inittab* and replace ::

    dwc_otg.lpm_enable=0 console=ttyAMA0,115200 kgdboc=ttyAMA0,115200 console=tty1 root=/dev/mmcblk0p2 rootfstype=ext4 elevator=deadline rootwait 

by ::

    dwc_otg.lpm_enable=0 console=tty1 root=/dev/mmcblk0p2 rootfstype=ext4 elevator=deadline rootwait 

Then edit */etc/inittab* and comment this line: ::

    0:23:respawn:/sbin/getty -L ttyAMA0 115200 vt100

became: ::

    #0:23:respawn:/sbin/getty -L ttyAMA0 115200 vt100



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
