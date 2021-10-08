
from math import radians
import numpy as np     # installed with matplotlib
import matplotlib.pyplot as plt

import serial

def serialDataFetching():
    ser = serial.Serial('COM4', 19323)
    print(ser.name)

def dataPlot():
    x = np.arange(0, radians(1800), radians(12))
    plt.plot(x, np.cos(x), 'b')
    plt.show()

serialDataFetching()



