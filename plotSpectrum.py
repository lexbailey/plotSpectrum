#!/usr/bin/env python3
import serial
import tkinter
import math

ser = serial.Serial("/dev/ttyACM0", 115200)

print("Spectrum")


winHeight = 500

window = tkinter.Tk()
canvas = tkinter.Canvas(window, height=winHeight, width=1000)
canvas.pack()
data = {}

def mainLoop():
	for i in range(100):
		try:
			chars = []
			chars.append(ser.read().decode("ascii"))
			while chars[-1] != '\n':
				chars.append(ser.read().decode("ascii"))
			line = "".join(chars[0:-1])
			print(line)
			try:
				(r, sample) = [int(x) for x in line.split("\t")]
				r = math.ceil(r/4)
				data[r] = math.ceil(winHeight - (sample/30000))
			except ValueError:
				pass
		except UnicodeDecodeError:
			pass
	dataKeys = sorted(data.keys())
	dataVals = [data[key] for key in dataKeys]
	canvas.delete(tkinter.ALL)
	for i in range(len(data)-1):
		j = i+1
		x1 = dataKeys[i]
		y1 = dataVals[i]
		x2 = dataKeys[j]
		y2 = dataVals[j]
		canvas.create_line(x1,y1,x2,y2, fill="red");
		print("line from %d, %d, to %d, %d" % (x1, y1, x2, y2))
	window.after(1, mainLoop)

window.after(1, mainLoop)
window.mainloop()
