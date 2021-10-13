import numpy as np     # installed with matplotlib
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import serial

debug_monitor_only = True
# functions
# initialize serial port
if debug_monitor_only==False:
    ser = serial.Serial()
    ser.port = 'COM4'
    ser.baudrate = 19323
    ser.timeout = 10 # specify the timeout when using readline()
    ser.open()
    if ser.is_open==True:
	    print("\nAll right, serial port now open. Configuration:\n")
	    print(ser, "\n") # print serial parameters
    else:
        print("\nError when opening the serial port\n")

# Create figure for plotting
plt.close('all')
fig = plt.figure()
ax = fig.add_subplot(1, 1, 1)
sensorData0 = []
sensorData1 = []
sensorData2 = []
sensorData3 = []
sensorData4 = []
sensorData5 = []
sensorData6 = []
sensorData7 = []
sensorData8 = []
sensorData9 = []

def dataPlot(self):
    if debug_monitor_only==False:
        aData = ser.readline()
        aData.decode()
    else:
        aData = [10, 20, 30, 40, 50, 60, 70, 80, 90, 100]

    sensorData0.append(aData[0])
    sensorData1.append(aData[1])
    sensorData2.append(aData[2])
    sensorData3.append(aData[3])
    sensorData4.append(aData[4])
    sensorData5.append(aData[5])
    sensorData6.append(aData[6])
    sensorData7.append(aData[7])
    sensorData8.append(aData[8])
    sensorData9.append(aData[9])
    ax.clear()
    ax.plot(sensorData0, label="sensorData0")
    ax.plot(sensorData1, label="sensorData1")
    ax.plot(sensorData2, label="sensorData2")
    ax.plot(sensorData3, label="sensorData3")
    ax.plot(sensorData4, label="sensorData4")
    ax.plot(sensorData5, label="sensorData5")
    ax.plot(sensorData6, label="sensorData6")
    ax.plot(sensorData7, label="sensorData7")
    ax.plot(sensorData8, label="sensorData8")
    ax.plot(sensorData9, label="sensorData9")

ani = animation.FuncAnimation(fig, dataPlot, interval = 1000)
plt.show()





    



