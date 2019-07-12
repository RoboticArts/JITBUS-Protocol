"""
---------------------------------------------------------------------
Robotic Arts Corporation
All Rights Reserved 2017-2019
---------------------------------------------------------------------
Attribution-NonCommercial-ShareAlike 4.0 International (CC BY-NC-SA 4.0)
https://creativecommons.org/licenses/by-nc-sa/4.0/
---------------------------------------------------------------------
File: getAllDataFromMaskId.py

Description: This example shows how to get all the messages with a specific
ID from the buffer all at once. Remember to connect the FTDI module in loopback
mode. For more information consult the readme file

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

    #We send five messages in a row, two with an ID and three with other
    myJitbus.sendMsg(0x1D4, x)
    myJitbus.sendMsg(0x0FF, x+1)
    myJitbus.sendMsg(0x0FF, x + 2)
    myJitbus.sendMsg(0x0FF, x + 3)
    myJitbus.sendMsg(0x1D4, x + 4)

    print("Id: ",0x1D4," Sent: ", x)
    print("Id: ",0x0FF," Sent: ", x+1)
    print("Id: ",0x0FF, " Sent: ",x+2)
    print("Id: ",0x0FF, " Sent: ",x+3)
    print("Id: ",0x1D4, " Sent: ",x+4)

    #2 ms pause due to computer USB latency
    time.sleep(0.002)

    #Check if there are messages available
    if myJitbus.availableMsg() > 0:

        #Check for messages with the specific ID available
        if myJitbus.isThereDataFromMaskId(0x1D4) > 0:

            #Get all messages with ID 0x1D4
            getId, getData = myJitbus.getAllDataFromMaskId(0x1D4)
            print("ID received:   ", getId)
            print("Data received: ", getData)

        if myJitbus.isThereDataFromMaskId(0x0FF) > 0:

            #Get all messages with ID 0x1D4
            getId, getData = myJitbus.getAllDataFromMaskId(0xFF)
            print("ID received:   ", getId)
            print("Data received: ", getData)


    print("-----------------------------------------------------")
