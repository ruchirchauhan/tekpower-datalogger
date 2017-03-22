# tekpower-datalogger
A Plotting utility for tekpower multimeters

This python based utility written for linux has been tested on tekpower multimeter model no: TP9605BT
but I am sure with few tweaks here and there, if at all, it can be used for other models as well.

So this tekpower model and likes have a communication feature over RS232, using which we should be able to plot and log the data in ral time, but turns out there is no reliable data logger app for PC, so I wrote one on my own, and want to share it here for anyone else who has been in search of such a thing.
This app is written mainly for linux os but can be ported to windows as well.

# How to use the app:
Requirements:
Linux
Python 2.7.x
pyQt4
pyqtgraph
numpy >1.10.x

Follow the steps to have the app working on a linux machine:
I am not giving any webpage links here because they might change in future, so anyone following these steps will have to figure out for their specific case, what the installation will take.

1. Install numpy >1.10.x if you don't have it already
2. Install pyQt4 python 2.7 bindings
3. Install pyqtgraph
4. Install pyserial
5. plug in tekpower RS232 to computer and figure out the device name for it. Should show up something as 'ttyUSBX' X-number
    example: linux-machine$ ls /dev/ttyUSB0
6. In file app-tekpower-datalogger.py, search for /dev/tty/USB0 and replace it with your device name
7. Execute app from terminal: ./app-tekpower-datalogger.py
8. To stop recording: hit enter on terminal
9. To close app: close the plot window as well

That's it. Hope you find it useful.
