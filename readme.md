#Daemind

A simple daemon wrapper written in Python for the Mindwave headset for Neurosky (white versione with the dongle). 

http://store.neurosky.com/products/mindwave-1

This daemon create a second layer over the ThinkGear connector giving the access to the data via an UDP socket.
You can also open the script to understand how to eventualy integrate it in your own code.

It's a really simple code; it doesn't make any error check and of course could be written better.
It's purpose is to help you understand how to parse data from the headset and speed up your prototyping fase.

Remenber that you must start the ThinkGear Connector before the Daemind.

##Usage

> cd [your_daemind_folder_path]
> Python Daemind.py -p [port] -a [ip]

-p UDP socket (65000 if not specified)
-a IP  address (127.0.0.1 if not specified)

You can also make it executable

> chmod +x Daemind.py
> ./Daemind.py -p [port] -a [ip]

##Requirements 

This daemon is written in Python 2.6 but can easily be ported even in Python 3.x
Requires the following library (you should already have all of them)
- Time
- Queue
- Threading
- Json
- Sys
- Socket


