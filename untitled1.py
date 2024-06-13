from time import sleep
import serial
import tkinter as tk
from tkinter import messagebox

ser = serial.Serial("COM3", 115200, timeout=2)
data = ""
condition = False

Tkwindow = tk.Tk()
Tkwindow.title("Python with Arduino")
Tkwindow.minsize(600, 400)

var = tk.IntVar()
var2 = tk.IntVar()


def print_selection():
    if var.get() == True and var2.get() == False:
        LabelA.config(text='溫度警示開啟')
    elif var.get() == False and var2.get() == True:
        LabelA.config(text='濕度警示開啟')
    elif var.get() == False and var2.get() == False:
        LabelA.config(text='都不開')
    else:
        LabelA.config(text='都開了')


def SerialWrite(command):
    ser.write(command)
    rv = ser.readline()
    print(rv.decode("utf-8"))
    data = rv.decode("utf-8")
    sleep(1)
    ser.flushInput()


def print_selection2(value):
    rv2 = ser.readline()
    data2 = rv2.decode("utf-8")
    temperature = float(data2)
    if temperature > 28:
        messagebox.showwarning("Temperature Warning", "Temperature exceeds 28 degrees!")

    if data2 > value:
        Arduino_cmd = 'a'
        cmd = Arduino_cmd.encode("utf-8")
        SerialWrite(cmd)
    else:
        Arduino_cmd = 'b'
        cmd = Arduino_cmd.encode("utf-8")
        SerialWrite(cmd)


def SendCmdC():
    Arduino_cmd = 'c'
    cmd = Arduino_cmd.encode("utf-8")
    SerialWrite(cmd)
    condition = True
    while condition:
        rvl = ser.readline()
        data = rvl.decode("utf-8")
        print(data)
        LabelA.config(text=data)
        LabelA.update_idletasks()
        Tkwindow.update()
        if not condition:
            break


def Serial_Connect():
    print("Connecting to Arduino ..... ")
    LabelA.config(text="Connecting to Arduino ..... ")
    LabelA.update_idletasks()
    Tkwindow.update()
    sleep(1)
    for i in range(1, 10):
        rv = ser.readline()
        print("Loading ... ")
        LabelA.config(text="Loading ... ")
        LabelA.update_idletasks()
        Tkwindow.update()
        print(rv.decode("utf-8"))
        ser.flushInput()
        sleep(1)
        Str_Message = rv.decode("utf-8")
        if Str_Message[0:5] == "Ready":
            print("Get Arduino Ready !")
            LabelA.config(text="Get Arduino Ready !")
            buttonStart.config(state="disabled")
            LabelA.update_idletasks()
            Tkwindow.update()
            break


def Exit():
    a = messagebox.askquestion(title='Exit', message='是否關閉視窗')
    if a == 'yes':
        Tkwindow.destroy()


scale = tk.Scale(Tkwindow, label='', from_=15, to=35, orient='horizontal', length=200, show=True, tickinterval=3,
                 resolution=0.01, command=print_selection2)
scale.pack()


checkbutton = tk.Checkbutton(master=Tkwindow, text='溫度警示', variable=var,
                             onvalue=True, offvalue=False, command=print_selection)
checkbutton.pack()

checkbutton2 = tk.Checkbutton(master=Tkwindow, text='濕度警示', variable=var2,
                              onvalue=True, offvalue=False, command=print_selection)
checkbutton2.pack()

LabelA = tk.Label(Tkwindow, bg='white',
                   fg='black',
                   text="Press 'connect' button to start",
                   width=50,
                   height=10,
                   justify=tk.LEFT)
LabelA.pack(side=tk.TOP)

buttonC = tk.Button(Tkwindow,
                    anchor=tk.S,
                    text="SHOW DHT",
                    width=10,
                    height=1,
                    command=SendCmdC)
buttonC.pack(side=tk.LEFT)

buttonStart = tk.Button(Tkwindow,
                        anchor=tk.S,
                        text="Connect",
                        width=10,
                        height=1,
                        command=Serial_Connect)
buttonStart.pack(side=tk.RIGHT)

buttonEnd = tk.Button(Tkwindow,
                      anchor=tk.S,
                      text="Exit",
                      width=10,
                      height=1,
                      command=Exit)
buttonEnd.pack(side=tk.RIGHT)

Tkwindow.mainloop()