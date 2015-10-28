# -*- coding: utf-8 -*-
from Tkinter import *
import numpy as np
import cv2
import serial

# Define root window
root = Tk()
root.title("Rico Vision Controller")
root.resizable(width=FALSE, height=FALSE)

lower_u_chrominance = IntVar()
upper_u_chrominance = IntVar()
lower_v_chrominance = IntVar()
upper_v_chrominance = IntVar()

# Adds HUE controls
def add_chrominance_control():
    chrominance_control_frame = Frame(root)
    chrominance_control_frame.pack(side=LEFT)
    Label(chrominance_control_frame, text="Lower U").pack()
    Scale(chrominance_control_frame, variable=lower_u_chrominance, from_=0, to=255, resolution=1, length=255, showvalue=False, orient=HORIZONTAL).pack()
    Label(chrominance_control_frame, text="Upper U").pack()
    Scale(chrominance_control_frame, variable=upper_u_chrominance, from_=0, to=255, resolution=1, length=255, showvalue=False, orient=HORIZONTAL).pack()
    Label(chrominance_control_frame, text="Lower V").pack()
    Scale(chrominance_control_frame, variable=lower_v_chrominance, from_=0, to=255, resolution=1, length=255, showvalue=False, orient=HORIZONTAL).pack()
    Label(chrominance_control_frame, text="Upper V").pack()
    Scale(chrominance_control_frame, variable=upper_v_chrominance, from_=0, to=255, resolution=1, length=255, showvalue=False, orient=HORIZONTAL).pack()

# Add displays
add_chrominance_control()

# Render window
root.mainloop()
