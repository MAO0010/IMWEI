from time import sleep
import serial
import tkinter
import re
import sys 
import pymysql

ser =serial.Serial("COM4", 115200, timeout=2)
data =""
condition = False
Celsiu_data=''
Fahrenheit_data=''
Humidity_data=''
ECHO_data=''
VAL=0
#傳送指令到arduino
def SerialWrite(command):
    ser.write(command)
    rv=ser.readline()#讀取arduino回傳訊息

    print (rv.decode("utf-8"))
    data = rv.decode("utf-8")
    print(data)
    sleep(1)
    ser.flushInput()#丟棄站存數據

msg=ser.readline().decode()
def SendCmdC():
    Arduino_cmd='c'
    cmd=Arduino_cmd.encode("utf-8")
    SerialWrite(cmd)
    condition = True
    while (condition):
        rvl=ser.readline()

        data = rvl.decode("utf-8")
        
        
        if (condition == False):
            break
                
        try:
            msg=ser.readline().decode()
            if(msg==''):
                continue
            else:
                
                print("msg={}".format(msg))
                msg_data=re.split(',|:', msg)
                LabelA.config(text= msg)
                LabelA.update_idletasks()
                Tkwindow.update()
                if("相對溼度"in str(msg_data[0])) and ("攝氏溫度"in str(msg_data[1])) and  ("華氏溫度"in str(msg_data[2])) and  ("距離"in str(msg_data[3])) :
                    Humidity_data = float(msg_data[0].split('：')[-1])
                    Celsiu_data = float(msg_data[1].split('：')[-1])
                    Fahrenheit_data = float(msg_data[2].split('：')[-1])
                    ECHO_data = float(msg_data[3].split('：')[-1])
                    VAL=scale.get()
                    VAL=float(VAL)
                    if float(Celsiu_data)>VAL:
                        tkinter.messagebox.showinfo(title='溫度過高',message='溫度過高')
                        Arduino_cmd='d'
                        cmd=Arduino_cmd.encode("utf-8")
                        SerialWrite(cmd)
                        sql=('INSERT INTO `dht`(`Celsiu`,`Fahrenheit`,`Humidity`)VALUES(%s,%s,%s)'%(Celsiu_data,Fahrenheit_data,Humidity_data))
                        try:
                           
                           db=pymysql.connect(host="172.20.10.4",user="root",password="",database="testt")
                           cursor1=db.cursor()
                           cursor1.execute(sql)
                           
                           db.commit()
                           print("success")
                        except  OSError:
                            db.rollback()
                            db.close()
                        db.close()
                        condition = False
                       
        except OSError as er:
            print(er)
                
def SendCmdD():
    Arduino_cmd='d'
    cmd=Arduino_cmd.encode("utf-8")
    SerialWrite(cmd)
    condition = False

    LabelA.config(text="Servo is running.")
    LabelA.update_idletasks()  
    Tkwindow.update()
 #連線至arduino
def print_selection(value):
    VAL=value
def Serial_Connect():
    print("Connecting to Arduino ..... ")

    LabelA.config(text="Connecting to Arduino ..... ")
    LabelA.update_idletasks()
    Tkwindow.update()
    sleep(1)
    for i in range (1,10):
        rv=ser.readline()
        print("Loading ... ")

        LabelA.config(text="Loading ... ")
        LabelA.update_idletasks()
        Tkwindow.update()

        print (rv.decode("utf-8"))
        ser.flushInput()
        sleep(1)
        Str_Message=rv.decode("utf-8")
    #收到字串為Ready 在LabeL顯示並關閉連線按鈕
        if Str_Message[0:5] == "Ready":
            print("Get Arduino Ready !")
            LabelA.config(text="Get Arduino Ready !")
            buttonStart.config(state="disabled")
            LabelA.update_idletasks()
            Tkwindow.update()
            break
def Exit():
    print("Exit ..... ")

    LabelA.config(text="Exit ..... ")
    LabelA.update_idletasks()
    Tkwindow.update()
    sleep(1)
    chr_num = 27 ##ESC
    cmd=(chr(chr_num).encode('utf-8'))
    SerialWrite(cmd)
    ser.close()
    Tkwindow. destroy()
 #Main
Tkwindow=tkinter. Tk()
Tkwindow. title("Python with arduino")
Tkwindow.minsize(600,400)
LabelA=tkinter. Label (Tkwindow,bg='white',
                       fg='black',
                       text="Press 'connect' button to start",
                       width=30,
                       height=10,
                       justify=tkinter. LEFT)
LabelA.pack(side=tkinter.TOP, fill=tkinter.BOTH, expand=True)


buttonC=tkinter.Button(Tkwindow,
                       anchor=tkinter.S,
                       text="SHOW DHT",
                       width=10,
                       height=1,
                       command=SendCmdC)
buttonC.pack(side=tkinter.LEFT)

buttonD=tkinter.Button(Tkwindow,
                       anchor=tkinter.S,
                       text="Servo",
                       width=10,
                       height=1,
                       command=SendCmdD,padx=3)
buttonD.pack(side=tkinter.LEFT)

buttonStart=tkinter.Button(Tkwindow,
                           anchor=tkinter.S,
                           text="Connect",
                           width=10,
                           height=1,
                         command=Serial_Connect)
buttonStart.pack(side=tkinter.RIGHT)

buttonEnd=tkinter.Button(Tkwindow,
                         anchor=tkinter.S,
                         text="Exit",
                         width=10,
                         height=1,
                         command=Exit)
buttonEnd.pack(side=tkinter.RIGHT)
scale=tkinter.Scale(Tkwindow,label="溫度設定",from_=20,to=35,orient='horizontal',length=200,show=True,tickinterval=3,resolution=0.01,command=print_selection)
scale.pack()
Tkwindow.mainloop()