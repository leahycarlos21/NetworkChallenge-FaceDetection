from ftplib import FTP
from PyQt5.uic import loadUi
from PyQt5 import QtGui, QtWidgets
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
        self.btn_sell = None
        self.setColumnWidthTables()
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
        #self.ftp.storbinary('STOR '+filename, open(filename, 'rb'))
        #self.ftp.quit()
        self.imageTable.setItem(self.iCounter - 1,self.jCounter + 1,QtWidgets.QTableWidgetItem("Image Uploaded...")) 

    def setCurrentPath(self, currentPath):
        self.pathLabel.setText(currentPath)
        #cmd = "cp {0} ~/NetworkChallenge-FaceDetection/Client/".format(currentPath)
        dest = shutil.move(currentPath, os.getcwd())
        #os.system(cmd) 
        pathList = currentPath.split("/")
        self.currentFileName = pathList[-1]
        self.setRowCountTables(self.iCounter + 1)
        self.imageTable.setItem(self.iCounter,self.jCounter,QtWidgets.QTableWidgetItem(self.currentFileName))
        self.imageTable.setItem(self.iCounter,self.jCounter + 1,QtWidgets.QTableWidgetItem(""))
        self.btn_sell = QtWidgets.QPushButton('Show')
        self.btn_sell.clicked.connect(self.handlerButton)
        self.imageTable.setCellWidget(self.iCounter, self.jCounter + 2, self.btn_sell)
        self.iCounter += 1

    def setColumnWidthTables(self):
        self.imageTable.setColumnWidth(0,300)
        self.imageTable.setColumnWidth(1,300)
        self.imageTable.setColumnWidth(2,300)

    def setRowCountTables(self, rowNumber):
        
        self.imageTable.setRowCount(rowNumber)
        
    def handlerButton(self):

        button = self.sender()
        index = self.imageTable.indexAt(button.pos())
        if index.isValid():
            fileName = self.imageTable.item(index.row(),0).text()
            image = QtGui.QImage('./' + fileName)
            pixmap = QtGui.QPixmap.fromImage(image)
            self.imageLabel.setPixmap(pixmap.scaled(461, 321, Qt.KeepAspectRatio))
        


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
    #FTP_PORT = 2121
    #ftp = FTP('')
    #ftp.connect('localhost',FTP_PORT)
    #ftp.login()
    #ftp.cwd('') #replace with your directory
    #ftp.retrlines('LIST')
    #GUI.setFTP(ftp)
    sys.exit(app.exec())


if __name__ == "__main__":
    mainGUI()
