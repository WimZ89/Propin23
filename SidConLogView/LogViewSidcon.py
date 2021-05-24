import sys
from PyQt5.QtWidgets import QApplication, QWidget, QHBoxLayout
import serial
from threading import Thread
import queue
from PyQt5.Qt import QTextCursor, QTimer, QTextEdit, QButtonGroup, QVBoxLayout,\
    QPushButton, QKeySequence, QIcon, QSize, QPixmap
from PyQt5.Qt import QGroupBox, QBoxLayout, QTableView, QStandardItemModel, QTableWidget, QColor,\
    QTableWidgetItem, Qt

import io
import json
# from _overlapped import NULL
from time import sleep
from copy import deepcopy
from datetime import datetime
import serial.tools.list_ports

#repo: https://repositories.mic-o-data.nl/svn/TestTooling/Miscellaneous/Wim/MiscTest(python)

Testing=False
Sandboxing = False

comports=["COM21","COM19"]
comport="Unknown"
# comport="COM19"
loglines_all=[]
loglines=[]
loglines_modem=[]
loglines_press=[]
logs=[loglines,loglines_all,loglines_modem,loglines_press]
MOFlinesRxQ=queue.Queue()
MOFlinesTxQ=queue.Queue()
MOFRxcount = 0
MOFRxcount_last = 0
TestLinesQ=queue.Queue()


SidConOUT_Init={
    "Out":{},
    "In":{},
    "Mem":{},
    "Vars":{},
    "State":{},
    "Count":{},
    "Time" :{},
    }

SidConOUT = deepcopy(SidConOUT_Init)

destination= {
    "#O":"Out"  ,
    "#I":"In"   ,
    "#M":"Mem"  ,
    "#V":"Vars" ,
    "#S":"State" ,
    "#C":"Count" ,
    "#T":"Time" ,
     }

replacelist=[
    "SidconOutputs.a.BIT.OUT_",
    "SidconInputs.a.BIT.IN_",
    "sidcon_app_status.",
    "sidcon_configuratie.",
    "sidcon_communication.", 
    ]

def logs_stamp(tag):
    for log in logs:
        log +=["STAMP %s : %s"%(tag,str(datetime.now()))]

def logs_clear():
    for log in logs:
        log.clear()
        
def print_test(*args, **kwargs):
    mystring = io.StringIO()
    print(*args, file=mystring, **kwargs)
    contents = mystring.getvalue()
    mystring.close()
    TestLinesQ.put(contents.strip())
    
def TB_GetVar(Type,Name):
    try :
        return SidConOUT[Type][Name]
    except:
        return "Not found"

def TB_ShowVar(Type,Name):
    value=TB_GetVar(Type,Name)
    print_test(Name,"=",value)
    return value

def TB_CheckVar(Type,Name,expected):
    value=TB_GetVar(Type,Name)
    result = expected==value
#     TestLines=
    print_test(Name,"=",value,result)
    return value

commands={}
def TB_Command(command):
    print_test("Command",command)
    MOFlinesTxQ.put(commands[command])
    
def TestBench():
    global Testing,commands
    commands=json.loads(open("LogViewSidcon.json","r").read())["Table"]
    Testing=True
    print_test("Start testing")
    TB_ShowVar("In","WasteLevelInMm")
    TB_ShowVar("In","Actual_motor_current")
    TB_Command("ButtonStart")
    sleep(1.1)
    TB_ShowVar("In","Actual_motor_current")
    TB_ShowVar("In","WasteLevelInMm")
    TB_Command("ButtonStart")
    sleep(1.1)
    TB_Command("ButtonReverse")
    sleep(1.1)
    TB_Command("ButtonStart")
    sleep(1.1)
    TB_Command("ButtonReverse")
    sleep(1.1)
    TB_Command("ButtonStart")
    
    print_test("Testing done")
    Testing=False
    

def StartThread(function):
    newthread=Thread(target=function, daemon=True)
    newthread.name=function.__name__
    newthread.start()



widdata={"TEST":1}
def savelog(data,filen):
    filen="logs/Sidon_log_%s.txt"%filen
    print("saving", len(data),"lines","to",filen)
    lines="\n".join(data)
    f = open(filen,"w")
    f.write(lines)
    f.close()
    print("done")

class MyApp(QWidget):
    def clearUILogs(self):
        global SidConOUT
        self.texts=[self.Term,self.modem,self.press,self.test]
        self.texts=[self.modem,self.press,self.test]
        for text in self.texts:
            text.setPlainText("")
        self.Vars.clear()
        SidConOUT = deepcopy(SidConOUT_Init)


    def Buttonclick(self):
        cmd=self.buttons[self.sender().text()]
#         print ("Clicked", cmd)
        if cmd == "Mute":
            self.mute = not self.mute
            
        elif cmd.startswith("Clear"):
            print (loglines)
            logs_clear()
            logs_stamp("Clear log")
            print (loglines)
            self.clearUILogs()
        elif cmd.startswith("SaveLog"):
#             open("logfile.txt","w").write(loglines_all.join("\n"))
            logs_stamp("Saved log")
            savelog(loglines_all,"all")
            savelog(loglines,"unsorted")
            savelog(loglines_modem,"modem")
            savelog(loglines_press,"press")
            print("saving", len(loglines_all),"lines")
        elif cmd.startswith("RunTests"):
            if not Testing:
                StartThread(TestBench)
        else:
            MOFlinesTxQ.put(cmd)
    
    def UIKeyDown(self, e):
        key=e.key()
        if key == Qt.Key_Shift:
            self.shiftState=True
            return
        elif e.key() == Qt.Key_Escape:
            MOFlinesTxQ.put("%c"%27)
            return
        if key > 128:
            return
        if not self.shiftState and key > 64:
            key+=97-65 # to lower
        MOFlinesTxQ.put("%c"%key)
    def UIKeyUp(self, e):
        key=e.key()
        if key == Qt.Key_Shift:
            self.shiftState=False
            return
                 
    def NewButton(self,box,name,command):
        new=QPushButton(name)
        new.clicked.connect(self.Buttonclick)
        box.addWidget(new)
    
    def __init__(self):
        super().__init__()
        self.mute=False
        self.initUI()

    def TimeTick(self):
        global MOFRxcount_last,MOFRxcount
        while (TestLinesQ.qsize()!=0):
            self.test.append(TestLinesQ.get())
            self.test.moveCursor(QTextCursor.End)
        while (MOFlinesRxQ.qsize()!=0):
            self.process_logline(MOFlinesRxQ.get())
        if ( self.sec10 == 10):
            bytestransfered=MOFRxcount-MOFRxcount_last
            kbsec=bytestransfered/0.1/1000
            stats ="Rx speed %8.2f kB/s\n"%(kbsec)
            stats+="Rx Muted %s\n"%self.mute
            stats+="Comport %s"%comport
            self.stats.setPlainText(stats)
#             self.test.append(stats.strip())
            MOFRxcount_last=MOFRxcount
            self.sec10 = 0
            self.sec += 1
        else:
            self.sec10 += 1

    def func_mappingSignal(self):
        self.ntableView.clicked.connect(self.func_test)

    def func_test(self, item):
        cellContent = item.data()
        print(cellContent)  # test
        sf = "You clicked on {}".format(cellContent)
        print(sf)            

    def createTable(self):
            colc=2
            self.Vars = QTableWidget()
            self.Vars.setColumnCount(colc)
            self.SetTable(SidConOUT)
            self.Vars.itemClicked.connect(self.on_clickTable)
            self.Vars.verticalHeader().hide()
            
    def on_clickTable(self):
#         print("\n")
        for currentQTableWidgetItem in self.Vars.selectedItems():
            row=currentQTableWidgetItem.row()
#             print(currentQTableWidgetItem.row(), currentQTableWidgetItem.column(), currentQTableWidgetItem.text())
            var=self.Vars.item(row,0).text()
#             print(var)
            cmd=self.inputs.setdefault(var,"\e")
#             print(cmd)
            self.Vars.clearSelection()
            MOFlinesTxQ.put(cmd)
                

        
    def initUI(self):

        self.shiftState=False
        self.tick=QTimer()
        self.tick.setInterval(100)
        self.tick.timeout.connect(self.TimeTick)
        self.tick.start()
        self.sec10=0
        self.sec=0
        
        self.createTable()
        self.Term = QTextEdit()
        self.Term.keyPressEvent=self.UIKeyDown
        self.Term.keyReleaseEvent=self.UIKeyUp
        self.modem = QTextEdit()
        self.press = QTextEdit()
        self.test = QTextEdit()
        self.stats = QTextEdit()
        hboxbot = QHBoxLayout()
        hboxbot.addWidget(self.modem, 2)
        hboxbot.addWidget(self.press, 1)
        hboxbot.addWidget(self.test, 1)
        hboxbot.addWidget(self.stats, 1)
        hboxtop = QHBoxLayout()
        hboxtop.addWidget(self.Term, 2)
        hboxtop.addWidget(self.Vars, 2)
        
        gbox=QVBoxLayout()
        bgrp = QGroupBox("Comm")
        bgrp.setLayout(gbox)
        self.settings=json.loads(open("LogViewSidcon.json","r").read())
        self.buttons = self.settings["Buttons"]
        self.inputs  = self.settings["Table"]
        for key in self.buttons.keys():
            self.NewButton(gbox,key,self.buttons[key])
        hboxtop.addWidget(bgrp,1)
        
        vbox = QVBoxLayout()
        vbox.addLayout(hboxtop,3)
        vbox.addLayout(hboxbot,2)
        self.setLayout(vbox)
        
        self.setWindowTitle('LogView SidCon V1.0')
#         pixmap = QPixmap ('SidCon.png')
#         l=24
#         app_icon = QIcon(pixmap.scaled(l, l))
#         app.setWindowIcon(app_icon)
        self.setGeometry(10, 100, 1000, 600)
        self.show()

    def process_logline(self,line):
        if self.mute:
            return
        found=False
        if "--- JUST RESET ---" in line:
            pass
            self.clearUILogs()
#             logs_clear()
            logs_stamp("JUST RESET")

            MOFlinesTxQ.put("sleep 0.5")
            MOFlinesTxQ.put("%c"%27)
            MOFlinesTxQ.put("sleep 0.5")
            MOFlinesTxQ.put("%c"%27)
            MOFlinesTxQ.put("sleep .5")
            MOFlinesTxQ.put("PTV") #turn on sendvars after reset
            if Sandboxing :
                MOFlinesTxQ.put("sleep .5")
                MOFlinesTxQ.put("PTS") #turn on zandbak after reset

        for key in destination.keys():
            if line.startswith(key):
                words=line[2:].split()
                if len(words)<2:
                    print("###ERROR",line)
                    break;
                varname=words[0]
                varvalue=words[1]
                for rep in replacelist:
                    varname=varname.replace(rep,"")
                SidConOUT[destination[key]][varname]=varvalue
                self.SetTable(SidConOUT)
                found=True
        if not found:
            if line=="":
                pass
            elif line.startswith("MODEM"):
                loglines_modem.append(line)
                self.modem.append(line)
                self.modem.moveCursor(QTextCursor.End)
            elif line.startswith("PRESS") or line.startswith("DRUM"):
                loglines_press.append(line)
                self.press.append(line)
                self.press.moveCursor(QTextCursor.End)
            else:
                loglines.append(line)
                self.Term.append(line)
                self.Term.moveCursor(QTextCursor.End)
            
            

    def SetTable(self,data):
        onoff={"On":QColor(0, 255, 153),"Off":QColor(230, 243, 255),}
        colors=[
            QColor(153, 255, 204),
            QColor(102, 255, 255),
            QColor(153, 204, 255),
            QColor(255, 204, 255),
            QColor(255, 255, 204),
            QColor(255, 204, 255),
            QColor(255, 255, 204),
            QColor(204, 255, 153),
            QColor(255, 230, 204),    ]
        row=0
        rowhdr=[]
        rowh=12
        self.Vars.verticalHeader().setMaximumSectionSize(15)
        for key in data.keys():
            color=colors[0]
            colors = colors[1:] + [colors[0]]
            for var in data[key].keys():
                if row == self.Vars.rowCount():
                    self.Vars.insertRow(self.Vars.rowCount())
                self.Vars.setRowHeight(row,rowh)
                rowhdr += " " #[key]

                cell=QTableWidgetItem(var)
                cell.setTextAlignment(Qt.AlignRight|Qt.AlignVCenter)
                cell.setBackground(color)
                self.Vars.setItem(row,0,cell)

                value=data[key][var]
                cell=QTableWidgetItem(value)
                cell.setBackground(onoff.setdefault(value, QColor(255, 255, 230)))
                self.Vars.setItem(row,1,cell)
                row+=1
                
                
        self.Vars.setVerticalHeaderLabels(rowhdr)
        self.Vars.setHorizontalHeaderLabels(["Name","Value"])
        self.Vars.resizeColumnsToContents();

def MOFSerialTx():
    while True:
        try:
            cmd=MOFlinesTxQ.get()
            if "sleep" in cmd:
                cmd = cmd.split()
#                 print(cmd)
                sleep (float(cmd[1]))
            else:
#             sleep(0.4)
                utf=cmd.encode('utf-8')
                numb=ser.write(utf)
                ser.flush()
#                 print ("wrote",numb,"bytes",utf)
        except:
            print("Write failed")
    
def MOFSerialRx():
    global ser,loglines_all,comports,MOFRxcount,MOFRxcount_last,comport
    while True:
        try:
            while True:
                line=ser.readline()
#                 print(line)
                MOFRxcount+=len(line)
                line=line.decode('utf-8').strip()
                loglines_all += [line]
                MOFlinesRxQ.put(line)
        except:
            print("Connection lost")
            t=0
            ser=0;
            while True: 
                try:
                    comport="Unknown"
                    Found=False
                    while not Found:
                        sleep(0.5)
                        ports = serial.tools.list_ports.comports()
                        for port, desc, hwid in sorted(ports):
                            if "WVSIDCON" in hwid:
                                print("Found SidCon on",port)
                                comport=port
                                Found=True
                                break
                    ser=serial.Serial(comport)
                except:
                    print("No connection",t)
                    t+=1
                    sleep(0.500)
                if ser!=0:
                    print ("Connected to", comport)
                    MOFRxcount=0
                    MOFRxcount_last=0
                    break
            
    
if __name__ == '__main__':
    ser=None
        
    StartThread(MOFSerialRx)
    StartThread(MOFSerialTx)

    app = QApplication(sys.argv)
    ex = MyApp()
    sys.exit(app.exec_())