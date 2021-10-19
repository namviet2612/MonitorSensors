import numpy as np     # installed with matplotlib
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import serial
import tkinter as tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

debug_monitor_only = True
start_drawing = False
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

#-----Sensor data processing ----------
sensorData0 = np.array([])
sensorData1 = np.array([])
sensorData2 = np.array([])
sensorData3 = np.array([])
sensorData4 = np.array([])
sensorData5 = np.array([])
sensorData6 = np.array([])
sensorData7 = np.array([])
sensorData8 = np.array([])
sensorData9 = np.array([])



def plot_data():
    global start_drawing, sensorData0
    if debug_monitor_only==False:
        aData = ser.readline()
        aData.decode()
    else:
        aData = [10, 20, 30, 40, 50, 60, 70, 80, 90, 100]

    if (start_drawing == True):
        if (len(sensorData0) < 100):
            sensorData0 = np.append(sensorData0, aData[0])
        else:
            sensorData0[0:99] = sensorData0[1:100]
            sensorData0[99] = aData[0]
        lines.set_xdata(np.arange(0,len(sensorData0)))
        lines.set_ydata(sensorData0)
        canvas.draw()

    root.after(1, plot_data)

def plot_start():
    global start_drawing
    start_drawing = True

def plot_stop():
    global start_drawing
    start_drawing = False

# Main GUI 
root = tk.Tk()
root.title('Real Time Plot')
root.configure(background = 'light blue')
root.geometry("900x600")

# Create figure for plotting
fig = Figure()
ax = fig.add_subplot(1, 1, 1)
ax.set_title('Sensors data')
ax.set_xlabel('Time')
ax.set_ylabel('Value')
ax.set_xlim(0,100)
ax.set_ylim(-0.5,100)
lines = ax.plot([],[])[0]

canvas = FigureCanvasTkAgg(fig, master=root)
canvas.get_tk_widget().place(x = 100, y = 100, width = 600, height = 400)
canvas.draw()

# Create button
root.update()
start = tk.Button(root, text = "Start", command = lambda: plot_start())
start.place(x = 100, y = 500)

root.update()
stop = tk.Button(root, text = "Stop", command = lambda: plot_stop())
stop.place(x = 500, y = 500)

root.after(1, plot_data)
root.mainloop()










    



