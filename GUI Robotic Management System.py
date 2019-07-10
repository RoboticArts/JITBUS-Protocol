from src import jitbus
import time

from tkinter import *
from tkinter.ttk import *
from tkinter import ttk
from tkinter import messagebox

import sys
import glob
import serial
import pickle

from PIL import Image
from PIL import ImageTk


"""
saveVector = 1,2,3,4
#Recupera los datos de la ultima sesion
try:
    saveVector = pickle.load(open("data_rms","rb"))

#Sino existe el archivo, se crea
except FileNotFoundError:
    pickle.dump(saveVector, open("data_rms", "wb"))
"""


def serial_ports():
    """ Lists serial port names

        :raises EnvironmentError:
            On unsupported or unknown platforms
        :returns:
            A list of the serial ports available on the system
    """
    if sys.platform.startswith('win'):
        ports = ['COM%s' % (i + 1) for i in range(256)]
    elif sys.platform.startswith('linux') or sys.platform.startswith('cygwin'):
        # this excludes your current terminal "/dev/tty"
        ports = glob.glob('/dev/tty[A-Za-z]*')
    elif sys.platform.startswith('darwin'):
        ports = glob.glob('/dev/tty.*')
    else:
        raise EnvironmentError('Unsupported platform')

    result = []
    for port in ports:
        try:
            s = serial.Serial(port)
            s.close()
            result.append(port)
        except (OSError, serial.SerialException):
            pass
    return result

atomRMS = jitbus.JitbusUSB()

window = Tk()

w = 520 # width for the Tk root
h = 330 # height for the Tk root

# get screen width and height
ws = window.winfo_screenwidth() # width of the screen
hs = window.winfo_screenheight() # height of the screen

# calculate x and y coordinates for the Tk root window
x = (ws/2) - (w/2)
y = -100 + ((hs/2) - (h/2))

# set the dimensions of the screen
# and where it is placed
window.geometry('%dx%d+%d+%d' % (w, h, x, y))

#window.geometry('435x260')
window.title("Robotic Management System")


# https://iconscout.com/icon/machine-58
# https://iconscout.com/contributors/vincent-le-moign
# https://www.iconfinder.com/icons/3099458/3_face_robot_icon
# Emoji Icon by Vincent Le Moign
# Creative Commons (Attribution 3.0 Unported)
# https://creativecommons.org/licenses/by/3.0/

window.wm_iconbitmap('machine.ico')



def eventLoad():
    #Carga los datos de la ultima vez que se guardo
    saveVector = pickle.load(open("data_rms", "rb"))
    textId1.delete(0,END)
    textId2.delete(0,END)
    textId3.delete(0,END)
    textId4.delete(0,END)
    textId1.insert(END, saveVector[0])
    textId2.insert(END, saveVector[1])
    textId3.insert(END, saveVector[2])
    textId4.insert(END, saveVector[3])
    textData1.delete(0, END)
    textData2.delete(0, END)
    textData3.delete(0, END)
    textData4.delete(0, END)
    textData1.insert(END, saveVector[4])
    textData2.insert(END, saveVector[5])
    textData3.insert(END, saveVector[6])
    textData4.insert(END, saveVector[7])
    textMaskId1.delete(0,END)
    textMaskId2.delete(0, END)
    textMaskId3.delete(0, END)
    textMaskId4.delete(0, END)
    textMaskId1.insert(END, saveVector[8])
    textMaskId2.insert(END, saveVector[9])
    textMaskId3.insert(END, saveVector[10])
    textMaskId4.insert(END, saveVector[11])

def eventSave():
    #Guarda los datos introducidos en la interfaz
    saveVector = [
                  textId1.get(), textId2.get(), textId3.get(), textId4.get(),
                  textData1.get(),textData1.get(),textData1.get(),textData1.get(),
                  textMaskId1.get(),textMaskId2.get(),textMaskId3.get(),textMaskId4.get()
                 ]
    pickle.dump(saveVector, open("data_rms", "wb"))

    messagebox.showinfo('Save', 'Data successfully saved')

menu = Menu(window)
new_item = Menu(menu,tearoff=0)
new_item.add_command(label='Save', command = eventSave)
new_item.add_command(label='Load', command= eventLoad)
menu.add_cascade(label='File', menu=new_item)
window.config(menu=menu)


tab_control = ttk.Notebook(window)
tab1 = ttk.Frame(tab_control)
tab2 = ttk.Frame(tab_control)
tab3 = ttk.Frame(tab_control)

tab_control.add(tab3, text='    COM    ')
tab_control.add(tab1, text='    Test    ')
tab_control.add(tab2, text='    Auto    ')
tab_control.pack(expand=1, fill='both')

############################################################################
                         #    T E S T    #
############################################################################

sendSelected = IntVar()
sendRad1 = Radiobutton(tab1, value=1, variable=sendSelected)
sendSelected.set(1)
sendRad2 = Radiobutton(tab1, value=2, variable=sendSelected)
sendRad3 = Radiobutton(tab1, value=3, variable=sendSelected)
sendRad4 = Radiobutton(tab1, value=4, variable=sendSelected)

sendRad1.grid(column=0, row=2, padx = (15,5))
sendRad2.grid(column=0, row=4, padx = (15,5))
sendRad3.grid(column=0, row=6, padx = (15,5))
sendRad4.grid(column=0, row=8, padx = (15,5))


k=1
labelId1= Label(tab1, text="ID")
labelId1.grid(column=1, row=k, sticky=W, pady=(6, 0))
textId1= Entry(tab1, width=10)
textId1.insert(END, "0x0001")
textId1.grid(column=1, row=k + 1, padx=(0, 10))

labelData1= Label(tab1, text="Data")
labelData1.grid(column=2, row=k, sticky=W, pady=(6, 0))
textData1 = Entry(tab1, width=10)
textData1.insert(END, "10")
textData1.grid(column=2, row=k + 1)

k=3
labelId2= Label(tab1, text="ID")
labelId2.grid(column=1, row=k, sticky=W, pady=(6, 0))
textId2= Entry(tab1, width=10)
textId2.insert(END, "0x0002")
textId2.grid(column=1, row=k + 1, padx=(0, 10))

labelData2= Label(tab1, text="Data")
labelData2.grid(column=2, row=k, sticky=W, pady=(6, 0))
textData2 = Entry(tab1, width=10)
textData2.insert(END, "20")
textData2.grid(column=2, row=k + 1)

k=5
labelId3= Label(tab1, text="ID")
labelId3.grid(column=1, row=k, sticky=W, pady=(6, 0))
textId3= Entry(tab1, width=10)
textId3.insert(END, "0x0003")
textId3.grid(column=1, row=k + 1, padx=(0, 10))

labelData3= Label(tab1, text="Data")
labelData3.grid(column=2, row=k, sticky=W, pady=(6, 0))
textData3 = Entry(tab1, width=10)
textData3.insert(END, "30")
textData3.grid(column=2, row=k + 1)

k=7
labelId4= Label(tab1, text="ID")
labelId4.grid(column=1, row=k, sticky=W, pady=(6, 0))
textId4= Entry(tab1, width=10)
textId4.insert(END, "0x0004")
textId4.grid(column=1, row=k + 1, padx=(0, 10))

labelData4= Label(tab1, text="Data")
labelData4.grid(column=2, row=k, sticky=W, pady=(6, 0))
textData4 = Entry(tab1, width=10)
textData4.insert(END, "40")
textData4.grid(column=2, row=k + 1)

############################################################################
############################################################################

def clickedSend():

    valueSend = '0'

    if sendSelected.get() == 1:
        valueSend = textData1.get()
        idSend = textId1.get()
    if sendSelected.get() == 2:
        valueSend = textData2.get()
        idSend = textId2.get()
    if sendSelected.get() == 3:
        valueSend = textData3.get()
        idSend = textId3.get()
    if sendSelected.get() == 4:
        valueSend = textData4.get()
        idSend = textId4.get()

    dataNumberSend = float(str(valueSend))
    idNumberSend = int(idSend, 16)

    if (dataNumberSend - int(dataNumberSend))==0:
        dataNumberSend = int(dataNumberSend)

    #print(idNumberSend)
    #print(dataNumberSend)

    atomRMS.sendMsg(idNumberSend, dataNumberSend)

btn1 = Button(tab1, text="Send", command = clickedSend)
btn1.grid(column=1, row=9, columnspan=2, pady = (10,0))

############################################################################
############################################################################


getSelected = IntVar()
getRad1 = Radiobutton(tab1, value=1, variable= getSelected)
getSelected.set(1)
getRad2 = Radiobutton(tab1, value=2, variable= getSelected)
getRad3 = Radiobutton(tab1, value=3, variable= getSelected)
getRad4 = Radiobutton(tab1, value=4, variable= getSelected)

getRad1.grid(column=3, row=2, padx = (45,5))
getRad2.grid(column=3, row=4,padx = (45,5))
getRad3.grid(column=3, row=6, padx = (45,5))
getRad4.grid(column=3, row=8, padx = (45,5))

############################################################################
############################################################################

k = 1
labelMaskId1 = Label(tab1, text="Mask ID")
labelMaskId1.grid(column=4, row=k, sticky=W, pady = (6,0))
textMaskId1 = Entry(tab1, width=10)
textMaskId1.insert(END, "0x0001")
textMaskId1.grid(column=4, row=k+1,  padx = (0,10))

labelGetData1 = Label(tab1, text="Get Data")
labelGetData1.grid(column=5, row=k, sticky=W, pady = (6,0))
textGetData1 = Entry(tab1, width=10)
textGetData1.grid(column=5, row=k+1)


k = 3
labelMaskId2 = Label(tab1, text="Mask ID")
labelMaskId2.grid(column=4, row=k, sticky=W, pady = (6,0))
textMaskId2 = Entry(tab1, width=10)
textMaskId2.insert(END, "0x0002")
textMaskId2.grid(column=4, row=k+1,  padx = (0,10))

labelGetData2 = Label(tab1, text="Get Data")
labelGetData2.grid(column=5, row=k, sticky=W, pady = (6,0))
textGetData2 = Entry(tab1, width=10)
textGetData2.grid(column=5, row=k+1)


k = 5
labelMaskId3 = Label(tab1, text="Mask ID")
labelMaskId3.grid(column=4, row=k, sticky=W, pady = (6,0))
textMaskId3 = Entry(tab1, width=10)
textMaskId3.insert(END, "0x0003")
textMaskId3.grid(column=4, row=k+1,  padx = (0,10))

labelGetData3 = Label(tab1, text="Get Data")
labelGetData3.grid(column=5, row=k, sticky=W, pady = (6,0))
textGetData3 = Entry(tab1, width=10)
textGetData3.grid(column=5, row=k+1)


k = 7
labelMaskId4 = Label(tab1, text="Mask ID")
labelMaskId4.grid(column=4, row=k, sticky=W, pady = (6,0))
textMaskId4 = Entry(tab1, width=10)
textMaskId4.insert(END, "0x0004")
textMaskId4.grid(column=4, row=k+1,  padx = (0,10))

labelGetData4 = Label(tab1, text="Get Data")
labelGetData4.grid(column=5, row=k, sticky=W, pady = (6,0))
textGetData4 = Entry(tab1, width=10)
textGetData4.grid(column=5, row=k+1)


def clickedGet():


    if atomRMS.availableMsg() > 0:

        if getSelected.get() == 1:
            testMaskId = int(textMaskId1.get(), 16)
            if atomRMS.isThereDataFromMaskId(testMaskId) > 0:
                getId, getData = atomRMS.getLastDataFromMaskId(testMaskId)
                textGetData1.delete(0, END)
                textGetData1.insert(END, str(getData))

        if getSelected.get() == 2:
            testMaskId = int(textMaskId2.get(), 16)
            if atomRMS.isThereDataFromMaskId(testMaskId) > 0:
                getId, getData = atomRMS.getLastDataFromMaskId(testMaskId)
                textGetData2.delete(0, END)
                textGetData2.insert(END, str(getData))

        if getSelected.get() == 3:
            testMaskId = int(textMaskId3.get(), 16)
            if atomRMS.isThereDataFromMaskId(testMaskId) > 0:
                getId, getData = atomRMS.getLastDataFromMaskId(testMaskId)
                textGetData3.delete(0, END)
                textGetData3.insert(END, str(getData))

        if getSelected.get() == 4:
            testMaskId = int(textMaskId4.get(), 16)
            if atomRMS.isThereDataFromMaskId(testMaskId) > 0:
                getId, getData = atomRMS.getLastDataFromMaskId(testMaskId)
                textGetData4.delete(0, END)
                textGetData4.insert(END, str(getData))

    else:
        getId = 0
        getData = 0





btn2 = Button(tab1, text="Receive", command = clickedGet)
btn2.grid(column=4, row=9, columnspan=2, pady = (10,0))


############################################################################
                         #    A U T O    #
############################################################################

labelAutoId = Label(tab2, text="ID")
labelAutoId.grid(column=1, row=1, sticky=W, pady=(70, 0), padx=(65,0))
textAutoId = Entry(tab2, width=10)
textAutoId.insert(END, "0x0001")
textAutoId.grid(column=1, row=2, padx=(70, 10))

labelAutoData = Label(tab2, text="Data")
labelAutoData.grid(column=2, row=1, sticky=W, pady=(70, 0))
textAutoData = Entry(tab2, width=10)
textAutoData.grid(column=2, row=2,  padx=(0, 10))

labelAutoMaskId = Label(tab2, text="Mask ID")
labelAutoMaskId.grid(column=3, row=1, sticky=W, pady=(70, 0))
textAutoMaskId = Entry(tab2, width=10)
textAutoMaskId.insert(END, "0x0001")
textAutoMaskId.grid(column=3, row=2, padx=(0, 10))

labelAutoGetData = Label(tab2, text="Get Data")
labelAutoGetData.grid(column=4, row=1, sticky=W, pady=(70, 0))
textAutoGetData = Entry(tab2, width=10)
textAutoGetData.grid(column=4, row=2)


slider = IntVar()
slider.set('0.00')

def sliderEvent(pos):

    pos = float(pos)
    pos = round(pos,2)
    textAutoData.delete(0,END)
    textAutoData.insert(END, str(pos))
    #x = lambda s: slider.set('%0.2f' % float(s))

    idAutoSend = int(textAutoId.get(),16)
    valueAutoSend = float(textAutoData.get())

    atomRMS.sendMsg(idAutoSend,valueAutoSend)
    print("EnviadoI: ", idAutoSend)
    print("EnviadoD: ",valueAutoSend)

    autoMaskId = int(textAutoMaskId.get(), 16)

    time.sleep(0.02)

    if atomRMS.availableMsg() > 0:

        #getAutoId, getAutoData = atomRMS.getMsg()
        if atomRMS.isThereDataFromMaskId(autoMaskId):

            getAutoId, getAutoData = atomRMS.getDataFromMaskId(autoMaskId)

            print("RecibidoI: ", getAutoId)
            print("RecibidoD: ", getAutoData)
    else:
        getAutoId = 0
        getAutoData = 0
        print(0)
        print(0)

    print("-----------------------------")
    textAutoGetData.delete(0,END)
    textAutoGetData.insert(END, str(round(float(getAutoData),2)))


sld = Scale(tab2, from_=0, to_=1000, length=300, command= sliderEvent)
#sld = Scale(tab2, from_=0, to_=1000, length=300, command=lambda s: slider.set('%0.2f' % float(s)))
sld.grid(column=1, row=3, columnspan=5,padx=(65, 0), pady=(10,0))
textAutoData.configure(text=slider)

#labelSld = Label(tab2, textvariable=slider)
#labelSld.grid(column=1, row=4, columnspan=5)


############################################################################
                            #    P O R T    #
############################################################################


combo = Combobox(tab3, values = serial_ports(), state="readonly")
if serial_ports():
    combo.current(0)
combo.grid(column=0, row=0, columnspan = 2, sticky = W, pady = (20,0), padx = 10 )

#atomRMS.open("COM10", 2000000 , 0.00000001)
#atomRMS.sendMsg(1,1)

def clickedConnect():

    if atomRMS.isOpen()==1:
        atomRMS.close()
        labelConnection.configure(text="State: Not connected")
        combo.configure(state='readonly')
        btnConnect.configure(text="Connect")

    else:
        try:
            atomRMS.open(combo.get(), 2000000, 0.00000001)
            labelConnection.configure(text="State: Connected")
            combo.configure(state='disabled')
            btnConnect.configure(text="Disconnect")

        except serial.SerialException:
            labelConnection.configure(text="Port is busy")


btnConnect = Button(tab3, text="Connect", command = clickedConnect)
btnConnect.grid(column=3, row=0, pady = (20,0))

labelConnection = Label(tab3, text = "State: Not connected")
labelConnection.grid(column=4, row=0,pady = (20,0), padx = (5,0)  )


image = Image.open("atom2.jpeg")
image = image.resize((310, 190), Image.ANTIALIAS) ## The (250, 250) is (height, width)
render = ImageTk.PhotoImage(image)
img = Label(tab3, image=render)
img.image = render
img.place(x=187, y=65)

labelRA = Label(tab3, text = "Robotic Arts", font = "Monospace 14 italic").place(x= 27, y = 90)
labelC = Label(tab3, text = "All rights reserved \u00A9",
               font = "Monospace 9 italic").place(x= 27, y = 120)
labelDate = Label(tab3, text = "2017-2019", font = "Monospace 9 italic").place(x= 50, y = 140)
labelVersion = Label(tab3, text = "Version 0.0.1", font = "Monospace 9 italic").place(x= 43, y = 170)


window.mainloop()

