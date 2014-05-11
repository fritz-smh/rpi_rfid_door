rpi_rfid_door
=============

Open some motorized doors with rfid items

This is a project for the Raspberry Pi system.



Rpi configuration
-----------------

In order to use the dedicated UART pins on the raspberry pi, first they have to be removed from their default application which is debugging.
To do this, edit */boot/cmdline.txt* and replace 

    dwc_otg.lpm_enable=0 console=ttyAMA0,115200 kgdboc=ttyAMA0,115200 console=tty1 root=/dev/mmcblk0p2 rootfstype=ext4 elevator=deadline rootwait 

by 

    dwc_otg.lpm_enable=0 console=tty1 root=/dev/mmcblk0p2 rootfstype=ext4 elevator=deadline rootwait 

Then edit */etc/inittab* and comment this line: 

    0:23:respawn:/sbin/getty -L ttyAMA0 115200 vt100

became: 

    #0:23:respawn:/sbin/getty -L ttyAMA0 115200 vt100



Dependencies
------------

Depends on *rpi_libs* : https://github.com/fritz-smh/rpi_libs
This library will be installed during the install process ;)


How to wire it ?
----------------

![how to wire it] (rfid_door_bb.png)


Install
-------

Clone the repository:

    cd $HOME
    git clone https://github.com/fritz-smh/rpi_rfid_door.git
    cd rpi_rfid_door
    sudo ./install.sh

Edit the configuration file *$HOME/rpi_rfid_door/config.json* :

    {
      "config" : { "status_led_pin" : 7,
                   "door_relay_pin" : 11,
                   "serial_rfid_device" : "/dev/ttyAMA0",
                   "smtp_server" : "smtp.free.fr",
                   "my_email" : "someone@free.fr"
                 },
      "granted" : [ "1761ab7a"
                  ]
    }

To discover a rfid item id, launch the *read_tag.sh* script and use a rfid item. You should see something like this :

    $ ./read_tag.sh 
    Start to listen to the rfid reader
    Rfid item detected : 1761ab7a
    Rfid item detected : caddb53f

Just add the desired ids in the *config.json* file in the *granted* list.


And finally just start the tool :

    /etc/init.d/rfid_door start

Start sequence
--------------

When the program is starting :
* the led will blink 5 times very quickly before doing anything else
* when the rfid reader is set, the led will be on for 3 seconds
* the led will be off until any event occurs

Led and events
--------------

When a granted rfid item is detected :
* the led will be set on for 2 seconds
* the relay wil be set on for 1 second

When a non granted rfid item is detected :
* the led will blink quickly 5 times
