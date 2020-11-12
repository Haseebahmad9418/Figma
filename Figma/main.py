from PyQt5.QtWidgets import QApplication
from figma import Ui_figma
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtCore import QTimer
import datetime
import socket
import sys
import os
import traceback
import logging
from collections import namedtuple

counter = False
currentTime = 0

totaldata=0
disk_ntuple = namedtuple('partition',  'device mountpoint fstype')
usage_ntuple = namedtuple('usage',  'total used free percent')

def disk_partitions(all=False):
    """Return all mountd partitions as a nameduple.
    If all == False return phyisical partitions only.
    """
    phydevs = []
    f = open("/proc/filesystems", "r")
    for line in f:
        if not line.startswith("nodev"):
            phydevs.append(line.strip())

    retlist = []
    f = open('/etc/mtab', "r")
    for line in f:
        if not all and line.startswith('none'):
            continue
        fields = line.split()
        device = fields[0]
        mountpoint = fields[1]
        fstype = fields[2]
        if not all and fstype not in phydevs:
            continue
        if device == 'none':
            device = ''
        ntuple = disk_ntuple(device, mountpoint, fstype)
        retlist.append(ntuple)
    return retlist


def disk_usage(path):
    """Return disk usage associated with path."""
    st = os.statvfs(path)
    free = (st.f_bavail * st.f_frsize)
    total = (st.f_blocks * st.f_frsize)
    used = (st.f_blocks - st.f_bfree) * st.f_frsize
    try:
        percent = ret = (float(used) / total) * 100
    except ZeroDivisionError:
        percent = 0
    # NB: the percentage is -5% than what shown by df due to
    # reserved blocks that we are currently not considering:
    # http://goo.gl/sWGbH
    return usage_ntuple(total/(1024*1024*1024), used/(1024*1024*1024), free/(1024*1024*1024), round(percent, 1))



class figma (QtWidgets.QMainWindow, Ui_figma):  # Class to acces Main.py GUI
    switch_recordaction = QtCore.pyqtSignal()

    def __init__(self):
        QtWidgets.QWidget.__init__(self)
        super(Ui_figma, self).__init__()
        self.setupUi(self)
        self.recordbtn.clicked.connect(lambda: self.recordAction())


    def recordAction(self):
        self.switch_recordaction.emit()
        pass


class Controller:  # Controller class which controlls all the functions
    def __init__(self):
        print("Initializing controller class")
        pass

    def sendMsgtoserver (self,msg):
        try:
            bytesToSend = str.encode(msg)
            bagRecorderSocket.settimeout(1)
            bagRecorderSocket.sendto(bytesToSend, bagRecorderPort)
            msgFromServer = bagRecorderSocket.recvfrom(bufferSize)
            responsefromServer = msgFromServer[0].decode().split(",")
            return responsefromServer
        except:
            return None



    def show_figma_page(self):
        self._figma = figma()
        self._figma.switch_recordaction.connect(self.showTime)
        self._figma.low.hide()
        self._figma.med.hide()
        self._figma.high.hide()
        self._figma.devicelogo1.hide()
        self._figma.devicelogo2.hide()
        self._figma.devicelogo3.hide()
        self._figma.devicelogo4.hide()
        self._figma.devicelogo1_3.hide()
        self._figma.devicelogo1_2.hide()
        self._figma.high_2.hide()
        self._figma.high_3.hide()
        self._figma.high_4.hide()
        self._figma.high_5.hide()
        self._figma.high_6.hide()
        self._figma.high_7.hide()
        self.updateTimer = QTimer()  # set interval to 1 s
        self.updateTimer.setInterval(100)  # 1000 ms = 1 s
        self.updateTimer.timeout.connect(self.updatorfunction)  # connect timeout signal to signal handler
        self.updateTimer.start()
        self.timer = QtCore.QTimer()
        self.timer.setInterval(1000)
        self.timer.timeout.connect(self.displayTime)
        self.timer.start()
        self._figma.show()


    def displayTime(self):
        self._figma.timelabel.setText(QtCore.QTime.currentTime().toString())  # QDateTime.currentDateTime()


    def updatorfunction(self):
        try:
            mountedusbdrivedata = 0
            usbName = '/media/ubuntu1804/datastore'
            isusb = os.path.ismount(usbName)
            if (isusb== True):
                mountedusbdrivedata = int(disk_usage(usbName)[2])
                print("Executing if loop: {}",mountedusbdrivedata)
            else:
                mountedusbdrivedata = 0
                print("No USB detected under: /media/ubuntu1804/datastore")
            self._figma.storagedatalabel.setText(str(mountedusbdrivedata)+" GB")
            # QApplication.processEvents()
        except Exception:
            print("Some error in disk storage occurred.")
            print("Unexpected error:", sys.exc_info()[0])
            logging.error(traceback.format_exc())
            pass

        try:
            statusSocket.settimeout(0.001)
            bytesAddressPair = statusSocket.recvfrom(bufferSize)
            message = bytesAddressPair[0]
            if (message != None):
                cmdcode = message.split(',')[0]
                print(cmdcode)
                if(cmdcode == '101'):
                    self._figma.distancelabel.setText(message.split(',')[1])
                    self._figma.timelabel_2.setText(message.split(',')[2])
                    self._figma.locationlabel.setText(message.split(',')[3])
                    QApplication.processEvents()
                elif (cmdcode == '102'):
                    self._figma.adsstatus.setText(message.split(',')[1])
                    QApplication.processEvents()
                elif (cmdcode == '103'):
                    self._figma.incamstatus.setText(message.split(',')[1])
                    QApplication.processEvents()
                elif (cmdcode == '104'):
                    self._figma.incamstatus_4.setText(message.split(',')[1])
                    QApplication.processEvents()
                elif (cmdcode == '105'):
                    self._figma.micstatus.setText(message.split(',')[1])
                    QApplication.processEvents()
                elif (cmdcode == '106'):
                    radiorange = int(message.split(',')[1])
                    if(radiorange <30):
                        self._figma.low.show()
                        self._figma.med.hide()
                        self._figma.high.hide()
                    elif(radiorange >69):
                        self._figma.high.show()
                        self._figma.med.hide()
                        self._figma.low.hide()
                    else:
                        self._figma.med.show()
                        self._figma.high.hide()
                        self._figma.low.hide()
                    QApplication.processEvents()
                elif (cmdcode == '201'):
                    self._figma.wificardstatus.setText(message.split(',')[1])
                    QApplication.processEvents()
                elif (cmdcode == '202'):
                    print(message)
                    devicesList = eval(message.decode('utf-8')[4:])
                    if(len(devicesList)==1):
                        self._figma.devicelogo1.show()
                        self._figma.high_2.show()
                        self._figma.high_2.setText(devicesList[0])
                        self._figma.devicelogo2.hide()
                        self._figma.high_3.hide()
                        self._figma.devicelogo3.hide()
                        self._figma.high_4.hide()
                        self._figma.devicelogo4.hide()
                        self._figma.high_5.hide()
                        self._figma.devicelogo1_3.hide()
                        self._figma.high_6.hide()
                        self._figma.devicelogo1_2.hide()
                        self._figma.high_7.hide()
                    elif(len(devicesList)==2):
                        self._figma.devicelogo1.show()
                        self._figma.high_2.show()
                        self._figma.high_2.setText(devicesList[0])
                        self._figma.devicelogo2.show()
                        self._figma.high_3.show()
                        self._figma.high_3.setText(devicesList[1])
                        self._figma.devicelogo3.hide()
                        self._figma.high_4.hide()
                        self._figma.devicelogo4.hide()
                        self._figma.high_5.hide()
                        self._figma.devicelogo1_3.hide()
                        self._figma.high_6.hide()
                        self._figma.devicelogo1_2.hide()
                        self._figma.high_7.hide()
                    elif (len(devicesList) ==3):
                        self._figma.devicelogo1.show()
                        self._figma.high_2.show()
                        self._figma.high_2.setText(devicesList[0])
                        self._figma.devicelogo2.show()
                        self._figma.high_3.show()
                        self._figma.high_3.setText(devicesList[1])
                        self._figma.devicelogo3.show()
                        self._figma.high_4.show()
                        self._figma.high_4.setText(devicesList[2])
                        self._figma.devicelogo4.hide()
                        self._figma.high_5.hide()
                        self._figma.devicelogo1_3.hide()
                        self._figma.high_6.hide()
                        self._figma.devicelogo1_2.hide()
                        self._figma.high_7.hide()
                    elif (len(devicesList) == 4):
                        self._figma.devicelogo1.show()
                        self._figma.high_2.show()
                        self._figma.high_2.setText(devicesList[0])
                        self._figma.devicelogo2.show()
                        self._figma.high_3.show()
                        self._figma.high_3.setText(devicesList[1])
                        self._figma.devicelogo3.show()
                        self._figma.high_4.show()
                        self._figma.high_4.setText(devicesList[2])
                        self._figma.devicelogo4.show()
                        self._figma.high_5.show()
                        self._figma.high_5.setText(devicesList[3])
                        self._figma.devicelogo1_3.hide()
                        self._figma.high_6.hide()
                        self._figma.devicelogo1_2.hide()
                        self._figma.high_7.hide()
                    elif (len(devicesList) == 5):
                        self._figma.devicelogo1.show()
                        self._figma.high_2.show()
                        self._figma.high_2.setText(devicesList[0])
                        self._figma.devicelogo2.show()
                        self._figma.high_3.show()
                        self._figma.high_3.setText(devicesList[1])
                        self._figma.devicelogo3.show()
                        self._figma.high_4.show()
                        self._figma.high_4.setText(devicesList[2])
                        self._figma.devicelogo4.show()
                        self._figma.high_5.show()
                        self._figma.high_5.setText(devicesList[3])
                        self._figma.devicelogo1_3.show()
                        self._figma.high_6.show()
                        self._figma.high_6.setText(devicesList[4])
                        self._figma.devicelogo1_2.hide()
                        self._figma.high_7.hide()
                    elif (len(devicesList) == 6):
                        self._figma.devicelogo1.show()
                        self._figma.high_2.show()
                        self._figma.high_2.setText(devicesList[0])
                        self._figma.devicelogo2.show()
                        self._figma.high_3.show()
                        self._figma.high_3.setText(devicesList[1])
                        self._figma.devicelogo3.show()
                        self._figma.high_4.show()
                        self._figma.high_4.setText(devicesList[2])
                        self._figma.devicelogo4.show()
                        self._figma.high_5.show()
                        self._figma.high_5.setText(devicesList[3])
                        self._figma.devicelogo1_3.show()
                        self._figma.high_6.show()
                        self._figma.high_6.setText(devicesList[4])
                        self._figma.devicelogo1_2.show()
                        self._figma.high_7.show()
                        self._figma.high_7.setText(devicesList[5])
                    else:
                        print("Received some garbage Value in 202 response")
                    pass
                    QApplication.processEvents()
                elif (cmdcode == '203'):
                    Signalrange = int(message.split(',')[1])
                    if (Signalrange < 10):
                        self._figma.lteSignal.setText("No Signals")
                    elif(Signalrange >49):
                        self._figma.lteSignal.setText("Good Strength")
                    else:
                        self._figma.lteSignal.setText("Poor Strength")
                    QApplication.processEvents()
                elif (cmdcode == '204'):
                    self._figma.awsConnectivity.setText(message.split(',')[1])
                    QApplication.processEvents()
                elif (cmdcode == '205'):
                    self._figma.transferspeed.setText(message.split(',')[1]+" "+"Mbps")
                    QApplication.processEvents()
                elif (cmdcode == '206'):
                    self._figma.transfereddata.setText(message.split(',')[1] + " " + "GB")
                    QApplication.processEvents()
        except Exception:
            print("Unexpected error:", sys.exc_info()[0])
            logging.error(traceback.format_exc())
            pass


    def showTime1(self):
        global currentTime
        t = str(datetime.datetime.now()-currentTime)[0:7]
        self._figma.timer.setText(t)


    def showTime(self):
        global counter, currentTime
        if (counter == False):
            msgFromClient = 's'
            msgFromServer = self.sendMsgtoserver(msgFromClient)
            print(msgFromServer)
            if (msgFromServer != None):
                if( len(msgFromServer) > 1):
                    if( msgFromServer[1] == 'Success'):
                        currentTime=datetime.datetime.now()
                        counter = True
                        self.qTimer = QTimer()  # set interval to 1 s
                        self.qTimer.setInterval(1000)  # 1000 ms = 1 s
                        self.qTimer.timeout.connect(self.showTime1)  # connect timeout signal to signal handler
                        self.qTimer.start()  # start timer
                    else:
                        print("Success not received msg = ")
                        print(msgFromServer[1])
                        pass
                else:
                    print("Success not received msg = ")
                    print(msgFromServer)
                    pass
        elif(counter == True):
            msgFromClient = '0'
            msgFromServer = self.sendMsgtoserver(msgFromClient)
            print(msgFromServer)
            if (msgFromServer != None):
                if( len(msgFromServer) > 1):
                    if( msgFromServer[1] == "Success"):
                        self.qTimer.stop()
                        counter = False
                    else:
                        print("Success not received msg = ")
                        print(msgFromServer[1])
                        pass
                else:
                    print("Success not received msg = ")
                    print(msgFromServer[1])
                    pass


def appExec():
    app = QtWidgets.QApplication(sys.argv)
    controller = Controller()
    print("Calling figmaMain")
    controller.show_figma_page()
    app.exec_()
    print("Sending Kill command to server ")
    msgFromClient = 'c'
    bytesToSend = str.encode(msgFromClient)
    bagRecorderSocket.sendto(bytesToSend, bagRecorderPort)
    print("Killed")



if __name__ == "__main__":

    # UDP client to send bag recording commands
    print("Creating a client side of UDP socket at 20001")
    bagRecorderPort = ("127.0.0.1", 20001)
    bufferSize = 1024  # Create a UDP socket at client side
    bagRecorderSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
    print("Created a UDP client at 20001")
    
    
    # UDP server to receive status updates
    print("Creating a UDP server at 20002")
    statusPort = ("127.0.0.1", 20002)
    statusBufferSize = 1024 
    statusSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
    statusSocket.bind(statusPort)
    print("Created a UDP server at 20002")
    
    
    print("Main")
    sys.exit(appExec())

