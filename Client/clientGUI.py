from ftplib import FTP
from PyQt5.uic import loadUi
from PyQt5 import QtWidgets
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QDialog,QFileDialog, QApplication,QScrollArea
import sys
import os
import requests
import shutil 

class ApplicationScreen(QDialog):

    def __init__(self):

        super(ApplicationScreen,self).__init__()
        loadUi("FaceDetection.ui",self)
        self.pathLabel.setText("")
        self.currentFileName = ""
        self.iCounter = 0
        self.jCounter = 0
        self.ftp = None
        self.setColumnWidthTables()
        self.setRowCountTables()
        self.selectButton.clicked.connect(self.openFileExplorer)
        self.uploadButton.clicked.connect(self.uploadFile)

    def setFTP(self, newFtp):
        self.ftp = newFtp

    def openFileExplorer(self):
        path = QFileDialog.getOpenFileName(self, 'Open a file', '','All Files (*.*)')
        if path != ('', ''):
            self.setCurrentPath(path[0])

    def uploadFile(self):
        filename = self.currentFileName 
        self.ftp.storbinary('STOR '+filename, open(filename, 'rb'))
        self.ftp.quit()
        self.imageTable.setItem(self.iCounter,self.jCounter + 1,QtWidgets.QTableWidgetItem("Image Uploaded...")) 

    def setCurrentPath(self, currentPath):
        self.pathLabel.setText(currentPath)
        #cmd = "cp {0} ~/NetworkChallenge-FaceDetection/Client/".format(currentPath)
        dest = shutil.move(currentPath, os.getcwd())
        #os.system(cmd) 
        pathList = currentPath.split("/")
        self.currentFileName = pathList[-1]
        self.imageTable.setItem(self.iCounter,self.jCounter,QtWidgets.QTableWidgetItem(self.currentFileName))
        self.imageTable.setItem(self.iCounter,self.jCounter + 1,QtWidgets.QTableWidgetItem(""))
        self.imageTable.setItem(self.iCounter,self.jCounter + 2,QtWidgets.QTableWidgetItem(""))

    def setColumnWidthTables(self):
        self.imageTable.setColumnWidth(0,300)
        self.imageTable.setColumnWidth(1,300)
        self.imageTable.setColumnWidth(2,300)

    def setRowCountTables(self):
        
        self.imageTable.setRowCount(1)



def mainGUI():
    app = QApplication(sys.argv)
    GUI = ApplicationScreen()
    scroll = QScrollArea()
    scroll.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
    scroll.setWidget(GUI)
    widget = QtWidgets.QStackedWidget()
    widget.addWidget(scroll)
    widget.setWindowTitle("Face Detection Network Challenge")
    widget.showMaximized()
    FTP_PORT = 2121
    ftp = FTP('')
    ftp.connect('localhost',FTP_PORT)
    ftp.login()
    ftp.cwd('') #replace with your directory
    ftp.retrlines('LIST')
    GUI.setFTP(ftp)
    sys.exit(app.exec())



"""

def downloadFile():
 filename = 'fotico.jpeg' #replace with your file in the directory ('directory_name')
 localfile = open(filename, 'wb')
 ftp.retrbinary('RETR ' + filename, localfile.write, FTP_PORT)
 ftp.quit()
 localfile.close()

def check_file():
    print("Work")
    r = requests.post('http://localhost:23336/api/checkimage', json={"imname": "processed-amigos.jpg"})
    r.status_code
    print(r.json())
    #JSON
    y = r.json()
    print(y["status"]) 


#downloadFile()
#check_file()

"""

if __name__ == "__main__":
    mainGUI()
