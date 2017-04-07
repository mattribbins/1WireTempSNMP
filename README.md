1-Wire Temperature Sensor
=========================

Requirements
------------
* Embedded device with 1-wire bus support (e.g. Raspberry Pi)
* 1-Wire sensors ([Sheepwalk Electronics](http://www.sheepwalkelectronics.co.uk/product_info.php?cPath=22&products_id=30) provide ready built sensors for the Pi.)

Software Installation
---------------------
Please note that the MIB values mentioned below need to paired up as follows:
* Sensor 0, snmpd pass-through MIB ending .0, script-0 MIB ending .1
* Sensor 1, snmpd pass-through MIB ending .2, script-1 MIB ending .3
* ... and so on.

These instructions assume using a Raspberry Pi unit. Other embedded devices may
vary.
* Install `snmpd` daemon
* Enable the 1-wire bus (for the Pi, use `raspbi-config`, alternatively `sudo modprobe w1-gpio; sudo modprobe w1-therm`)
* Copy temp-get.py script to /usr/local/bin/
* Copy temp-x bash script to /usr/local/bin/
* Set up Sensor 0. Copy temp-x to temp-0 and edit the script. Repeat as necessary
  * Edit the SNMP MIB to a unique value (e.g. .1.3.6.1.2.1.25.1.8.1).
  * Edit the python script call and update the 1-Wire UID for the relevant
  sensor
* Edit configuration based off snmpd.conf.example
  * Set up pass-through MIB, point to the temp-0 script and set the MIB paired
  to the one in the script (e.g. .1.3.6.1.2.1.25.1.8.0)
* Repeat the last two instructions for however many sensors on the 1-wire line.


Hardware Installation
---------------------
Install the 1-wire devices and connect as appropriate using direct cables or
CAT5e/RJ45.

Testing
-------
To test that the 1-wire devices are working correctly, navigate to the following directory and ls. Any valid temperature sensor devices will appear as 28-*
devices.
 ```
$ cd /sys/bus/w1/devices && ls
28-000008816ace  28-00000881a0ff  w1_bus_master1
```
You can now print the value from the w1_slave file.
```
$ cat 28-00000881a0ff/w1_slave
3e 01 4b 46 7f ff 02 10 6c : crc=6c YES
3e 01 4b 46 7f ff 02 10 6c t=19875
```
The t= value is the temperature in celsius*1000. If you receive a value that is
too high (80000) or too low (00000) or the CRC check fails, then there is an
issue with reading the value. Look at cable length, and whether the device needs
to be powered externally using a 5V USB cable.

Once the sensor is working correctly natively, and the setup of the snmpd is
completed, you can run a SNMP client to check values are coming through.
Check all SNMP values
```
$ snmpwalk -v 1 -c public 10.92.183.71
```
Check an individual SNMP trap
$ snmpget -v 1 -c public 10.92.183.71 .1.3.6.1.2.1.25.1.8.0
HOST-RESOURCES-MIB::hrSystem.8.1 = Gauge32: 19875
```

Useful links
-----
* [Guidelines for Reliable Long 1-Wire Networks](https://www.maximintegrated.com/en/app-notes/index.mvp/id/148).
* [Sheepwalk Electronics](http://www.sheepwalkelectronics.co.uk/) for
pre-assembled 1-wire components.
