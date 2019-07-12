"""
---------------------------------------------------------------------
Robotic Arts Corporation
All Rights Reserved 2017-2019
---------------------------------------------------------------------
Attribution-NonCommercial-ShareAlike 4.0 International (CC BY-NC-SA 4.0)
https://creativecommons.org/licenses/by-nc-sa/4.0/
---------------------------------------------------------------------
File: example_getDataFromMaskId.py

Description: This example shows how to receive one by one the available
messages in the buffer that have the specified ID. Remember to connect
the FTDI module in loopback mode. For more information consult the readme
file

----------------------------------------------------------------------
		Version: 0.0.1						| Last Modification: 10/07/2019

		Author: Robert Vasquez Zavaleta
		Contact: roboticarts1@gmail.com
"""

import jitbus
import time

myJitbus = jitbus.JitbusUSB()
myJitbus.open("COM10", 3000000 , 0.00000001)


#We will send and receive data 20 times
for x in range(20):

    print("Iteration: ", x )

    #We send four messages in a row, two with an ID and two with other
    myJitbus.sendMsg(0x1D4, x)
    myJitbus.sendMsg(0x0FF, x+1)
    myJitbus.sendMsg(0x0FF, x+2)
    myJitbus.sendMsg(0x1D4, x+3)

    print("Id: ",0x1D4," Sent: ", x)
    print("Id: ",0x0FF," Sent: ", x+1)
    print("Id: ",0x0FF, " Sent: ", x+2)
    print("Id: ",0x1D4, " Sent: ", x+3)

    #2 ms pause due to computer USB latency
    time.sleep(0.002)

    #Check if there are messages available
    if myJitbus.availableMsg() > 0:

        #Get the number of messages available that have the specified ID
        numberOfMsgsWithID = myJitbus.isThereDataFromMaskId(0x1D4)

        #Get all the messages one by one with the specified ID
        for w in range (numberOfMsgsWithID):

            getId, getData = myJitbus.getDataFromMaskId(0x1D4)

            print("Message ", w + 1, "from buffer")
            print("ID Recibido:   ", getId)
            print("Dato Recibido: ", getData)

    print("-----------------------------------------------------")
