#!/bin/bash

# first, let's check install.sh is run as root
if [ "$(id -u)" != "0" ]; then
   echo "This script must be run as root" 1>&2
   exit 1
fi

# get the folder of the rfid tool
FOLDER=$(dirname $(readlink -f $0))

# get the user/group of the folder of the rfid tool
USER=$(ls -ld $FOLDER | awk '{print $3}')
GROUP=$(ls -ld $FOLDER | awk '{print $4}')

### external libraries related tasks #########################

echo "Install external libs ..."
mkdir $FOLDER/external_libs/
cd $FOLDER/external_libs/

echo "- rpi_libs (from https://github.com/fritz-smh/rpi_libs.git) ..."
git clone https://github.com/fritz-smh/rpi_libs.git
touch $FOLDER/external_libs/__init__.py
chown -R $USER:$GROUP $FOLDER/external_libs/

### init.d related tasks #####################################

# copy the init.d file
echo "Copy the init.d file as /etc/init.d/rfid_door ..."
cp $FOLDER/install/init.sample /etc/init.d/rfid_door

echo "Configure the init.d file ..."
sudo chmod +x /etc/init.d/rfid_door

# update the init.d file
sed -i "s#___INSTALL_PATH___#$FOLDER#g" /etc/init.d/rfid_door

# set the init script to be called on system startup
echo "Configure auto startup ..."
update-rc.d rfid_door defaults

echo "End"

