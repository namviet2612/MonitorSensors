import numpy as np     # installed with matplotlib
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import serial
import tkinter as tk
from tkinter import ttk
from tkinter import *
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

#-----Global variables
debug_monitor_only = False
start_drawing = False
ser = serial.Serial()
comIsOpened = False
PlotButtonIsPressed = False

#-----Sensor data processing ----------
sensorData = np.array([])
aData = np.array([])

# initialize serial port
def SerialPortInit(comPort):
    global comIsOpened
    if debug_monitor_only==False:
        try:
            ser.port = comPort
            ser.baudrate = 115200
            ser.timeout = 10 # specify the timeout when using readline()
            ser.open()
        except serial.SerialException as e:
            print("\nError when opening the serial port\n")
            COMStatus.configure(text="Không thể kết nối cổng COM!", foreground = 'red')
        if ser.is_open==True:
            comIsOpened = True
            #print("\nAll right, serial port now open. Configuration:\n")
            #print(ser, "\n") # print serial parameters
            COMStatus.configure(text="Cổng COM đã kết nối!", foreground = 'black')
            connectCOM.configure(state=DISABLED)
            for item in sensorItem:
                item.buttonEnable()

def convertAmpe(bufferData0, bufferData1):
    rawData = (bufferData0 << 8) | bufferData1
    rawData = 4.0 + (16.0 / 4096.0) * rawData
    return rawData

def convertTemperaturePT100(Ampe):
    tempPT100Value = Ampe * (300.0 / 16.0) - (300.0 / 4.0)
    return round(tempPT100Value,2)

def convertAtmosphere(Ampe):
    barValue = Ampe * (10.0 / 16.0) - (10.0 / 4.0)
    return round(barValue,2)

def convertInfraRed(Ampe):
    tempInfraRed = Ampe * (400.0 / 16.0) - (400.0 / 4.0)
    return round(tempInfraRed,2)

def convertHumidity(Ampe):
    percentValue = Ampe * (100.0 / 16.0) - (100.0 / 4.0)
    return round(percentValue,2)

def convertVoltage(bufferData0, bufferData1):
    rawData = (bufferData0 << 8) | bufferData1
    rawData = (5.0 / 4096.0) * rawData
    return rawData

def convertDistance(volt):
    distanceValue = volt
    return round(distanceValue,2)

def convertWeight(volt):
    weightValue = volt
    return round(weightValue,2)

def convertLitre(bufferData0, bufferData1):
    rawData = (bufferData0 << 8) | bufferData1
    rawData = rawData / 361
    return round(rawData,2)

def convertCounter(bufferData0, bufferData1):
    rawData = (bufferData0 << 8) | bufferData1
    return rawData

def plot_data():
    global start_drawing, sensorData, comIsOpened, aData, current_Sensor, PlotButtonIsPressed
    for item in sensorItem:
        item.entry.delete(0, 'end')
        item.entry.insert(0, f'{item.value}')
    if (PlotButtonIsPressed == True):
        PlotButtonIsPressed = False
        #Try to clear all plot displayed data
        a_list = list(range(0, len(sensorData)))
        sensorData = np.delete(sensorData, a_list)
        root.after(500, plot_data)
        return
    else:
        pass
    if (comIsOpened==True):
        try:
            aData = list(ser.readline())
            aDataLength = len(aData)
            if ((aData[0] == 0x55) and (aData[1] == 0xAA) and (aData[aDataLength - 2] == 0xD) and (aData[aDataLength - 1] == 0xA)):
            #Pattern matched
                sensorItem[0].value = convertTemperaturePT100(convertAmpe(aData[2], aData[3]))
                sensorItem[1].value = convertAtmosphere(convertAmpe(aData[4], aData[5]))
                sensorItem[2].value = convertInfraRed(convertAmpe(aData[6], aData[7]))
                sensorItem[3].value = convertHumidity(convertAmpe(aData[8], aData[9]))
                sensorItem[4].value = convertDistance(convertVoltage(aData[10], aData[11]))
                sensorItem[5].value = convertWeight(convertVoltage(aData[12], aData[13]))
                sensorItem[6].value = convertCounter(aData[14], aData[15])
                sensorItem[7].value = convertCounter(aData[16], aData[17])
                sensorItem[8].value = convertLitre(aData[18], aData[19])
                sensorItem[9].value = convertCounter(aData[20], aData[21])
                sensorItem[10].value = convertCounter(aData[22], aData[23])
                if (start_drawing == True):
                    if (len(sensorData) < 100):
                        sensorData = np.append(sensorData, sensorItem[current_Sensor].value)
                    else:
                        sensorData[0:99] = sensorData[1:100]
                        sensorData[99] = sensorItem[current_Sensor].value
                    lines.set_xdata(np.arange(0,len(sensorData)))
                    lines.set_ydata(sensorData)
                    canvas.draw()
                else:
                    pass
            else:
                pass
        except serial.SerialException as e:
            #There is no new data from serial port
            comIsOpened = False
            start_drawing = False
            COMStatus.configure(text="Mất kết nối tới cổng COM! Thử kết nối lại", foreground = 'red')
            connectCOM.configure(state=NORMAL)
            for item in sensorItem:
                item.buttonDisable()
        except TypeError as error:
            print(error)
            ser.close()
            COMStatus.configure(text="Đã xảy ra lỗi. Ngắt kết nối cổng COM!", foreground = 'red')
            comIsOpened = False
            start_drawing = False
            for item in sensorItem:
                item.buttonDisable()
            connectCOM.configure(state=NORMAL)
    root.after(500, plot_data)

def plot_start():
    global start_drawing
    start_drawing = True

def plot_stop():
    global start_drawing
    start_drawing = False

# Class for a sensor
class sensor():
    def __init__(self, lable_name ,sensorNumber, sensorValue, y_min, y_max, y_title):
        self.y_title = y_title
        self.y_max = y_max
        self.y_min = y_min
        self.value = sensorValue
        self.entry = Entry(root, width=10)
        self.label = Label(root, text = lable_name, bg='#0f4b6e', fg='white', width=10, anchor='w')
        self.button = tk.Button(root, text = "Đồ thị", command = lambda: self.plot_startSensor(), state=DISABLED)
        self.number = sensorNumber 
    def placePosition(self, entry_X, entry_Y, label_X, label_Y, button_X, button_Y):        
        self.entry.place(x = entry_X, y = entry_Y)
        self.label.place(x= label_X, y = label_Y)
        self.button.place(x= button_X, y = button_Y)
    
    def plot_startSensor(self):
        global current_Sensor, fig, canvas, PlotButtonIsPressed
        current_Sensor = self.number
        PlotButtonIsPressed = True
        sTitle = "Dữ liệu cảm biến " + self.label.cget("text")
        ax.set_title(sTitle)
        ax.set_ylabel(self.y_title)
        ax.set_ylim(self.y_min, self.y_max)
        plot_start()

    def getValue(self):
        self.value = 0

    def buttonEnable(self):
        self.button.configure(state=NORMAL)

    def buttonDisable(self):
        self.button.configure(state=DISABLED)

# Main GUI 
root = tk.Tk()
root.title('Bàn thực hành cảm biến')
root.configure(background = 'light blue')
root.geometry("1200x800")

# Create figure for plotting
fig = Figure()
ax = fig.add_subplot(1, 1, 1)
ax.patch.set_facecolor('#F4EAEA')
ax.set_title('Dữ liệu cảm biến')
ax.set_xlabel('Thời gian')
ax.set_ylabel('Giá trị')
ax.set_xlim(0,100)
ax.set_ylim(-0.5,100)
lines = ax.plot([],[])[0]

canvas = FigureCanvasTkAgg(fig, master=root)
canvas.get_tk_widget().place(x = 100, y = 100, width = 600, height = 400)
canvas.draw()

# Create sensors list
sensorItem = []

# Create sensor 1
sensorItem.append(sensor('Nhiệt độ', 0, 0, 0, 350, 'độ C'))
sensorItem[0].placePosition(800, 100, 720, 100, 720, 125) 

# Create sensor 2
sensorItem.append(sensor('Áp suất', 1, 0, 0, 15, 'Bar'))
sensorItem[1].placePosition(800, 175, 720, 175, 720, 200)

## Create sensor 3
sensorItem.append(sensor('Hồng ngoại', 2, 0, 0, 500, 'độ C'))
sensorItem[2].placePosition(800, 250, 720, 250, 720, 275)

## Create sensor 4
sensorItem.append(sensor('Độ ẩm', 3, 0, 0, 100, '%'))
sensorItem[3].placePosition(800, 325, 720, 325, 720, 350)

## Create sensor 5
sensorItem.append(sensor('Siêu âm', 4, 0, 0, 5, 'm'))
sensorItem[4].placePosition(800, 400, 720, 400, 720, 425)

## Create sensor 6
sensorItem.append(sensor('Khối lượng', 5, 0, 0, 120, 'kg'))
sensorItem[5].placePosition(800, 475, 720, 475, 720, 500)

## Create sensor 7
sensorItem.append(sensor('Điện dung', 6, 0, 0, 20, 'mF'))
sensorItem[6].placePosition(1000, 100, 920, 100, 920, 125)

## Create sensor 8
sensorItem.append(sensor('Tiệm cận 2', 7, 0, 0, 100, 'xung'))
sensorItem[7].placePosition(1000, 175, 920, 175, 920, 200)

## Create sensor 9
sensorItem.append(sensor('Lưu lượng', 8, 0, 0, 100, 'lít'))
sensorItem[8].placePosition(1000, 250, 920, 250, 920, 275)

##create sensor 10
sensorItem.append(sensor('Tiệm cận 1', 9, 0, 0, 100, 'xung'))
sensorItem[9].placePosition(1000, 325, 920, 325, 920, 350)

##create sensor 11
sensorItem.append(sensor('Chuyển động', 10, 0, 0, 100, 'xung'))
sensorItem[10].placePosition(1000, 400, 920, 400, 920, 425)

# Create stop button
root.update()
stop = tk.Button(root, text = "Dừng", command = lambda: plot_stop())
stop.place(x = 400, y = 500)

#Create COM label
comSelectMessage = ttk.Label(root, text = "Lựa chọn cổng COM:")
comSelectMessage.place(x = 20, y = 20)

#Create combobox to select COM
comSelected = ttk.Combobox(root, width = 10)
comSelected.place(x = 150, y = 20)

comSelected['values'] = ('COM0', 'COM1', 'COM2', 'COM3', 'COM4',
                         'COM5', 'COM6', 'COM7', 'COM8', 'COM9',
                         'COM10', 'COM11', 'COM12', 'COM13', 'COM14')
comSelected.current(0)

#Button to connect COM
root.update()
connectCOM = tk.Button(root, text = "Kết nối", command = lambda: SerialPortInit(comSelected.get()))
connectCOM.place (x = 20, y = 40)

#COM open status message
root.update()
COMStatus = tk.Message(root, width = 500, background = 'light blue')
COMStatus.place (x = 80, y = 40)

#Title
root.update()
sTitle = Label(root, text = "BÀN THỰC HÀNH CẢM BIẾN", font=("Arial", 25), background = 'light blue')
sTitle.place(x= 350, y= 20)

root.after(500, plot_data)

root.mainloop()










    



