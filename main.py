#GUI libs
from PyQt5 import QtCore, QtGui, QtWidgets 
from PyQt5.QtCore import Qt , QEvent
from PyQt5.QtWidgets import QFileDialog , QLabel , QListWidget , QListWidgetItem ,QMessageBox , QMenu , QDialog , QPlainTextEdit ,QFileDialog ,QShortcut
from PyQt5.QtGui import QPixmap , QIcon ,QKeySequence

import os
import glob

#for reload my
from importlib import reload 	

#image procesing libs
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
from matplotlib import pyplot as plt
import cv2 

#user python file
import my

#unique ids for plt
import uuid

def strid() :
    return str(uuid.uuid1())


class Ui_MainWindow(object):

    inputFont = QtGui.QFont('Input Sans',16)
    img = None
    rollbackCount = 0
    storage = {}
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1100, 900)
        MainWindow.setMinimumSize(QtCore.QSize(1100, 900))
        MainWindow.setMaximumSize(QtCore.QSize(1100, 900))

        MainWindow.setWindowIcon(QtGui.QIcon('res/logo.png'))

        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")

        self.plainTextCode = QtWidgets.QPlainTextEdit(self.centralwidget)
        self.plainTextCode.setGeometry(QtCore.QRect(10, 668, 1080, 200))
        self.plainTextCode.setObjectName("plainTextCode")
        self.plainTextCode.setStyleSheet("QPlainTextEdit {background-color: #181818; color: white;}")

        self.exeCode = QtWidgets.QPushButton(self.centralwidget)
        self.exeCode.setGeometry(QtCore.QRect(10, 620, 94, 31))
        self.exeCode.setObjectName("exeCode")
        self.exeCode.setStyleSheet('background-color : #57a0d3')

        self.pltImage = QtWidgets.QPushButton(self.centralwidget)
        self.pltImage.setGeometry(QtCore.QRect(505, 625, 105, 31))
        self.pltImage.setObjectName("exeCode")
        self.pltImage.setStyleSheet('background-color : #18a558')

        self.rollback = QtWidgets.QPushButton(self.centralwidget)
        self.rollback.setGeometry(QtCore.QRect(700, 625, 105, 31))
        self.rollback.setObjectName("exeCode")
        self.rollback.setStyleSheet('background-color : #cbd5e1')

        self.saveImage = QtWidgets.QPushButton(self.centralwidget)
        self.saveImage.setGeometry(QtCore.QRect(1000, 620, 91, 31))
        self.saveImage.setObjectName("saveImage")

        self.addCode = QtWidgets.QPushButton(self.centralwidget)
        self.addCode.setGeometry(QtCore.QRect(120, 620, 91, 31))
        self.addCode.setObjectName("addCode")

        self.excCodeBar = QtWidgets.QPushButton(self.centralwidget)
        self.excCodeBar.setGeometry(QtCore.QRect(890, 620, 94, 31))
        self.excCodeBar.setObjectName("excCodeBar")
        self.excCodeBar.setStyleSheet('background-color : #57a0d3')

        self.lableImage = QtWidgets.QLabel(self.centralwidget)
        self.lableImage.setGeometry(QtCore.QRect(250, 20, 600, 600))
        self.lableImage.setAlignment(QtCore.Qt.AlignCenter)
        self.lableImage.setObjectName("lableImage")

        self.listWidget = QtWidgets.QListWidget(self.centralwidget)
        self.listWidget.setGeometry(QtCore.QRect(890, 10, 200, 600))
        self.listWidget.setObjectName("listWidget")
        self.listWidget.setStyleSheet("QListWidget {color: white; font-size: 14px;}")

        self.listWidget_2 = QtWidgets.QListWidget(self.centralwidget)
        self.listWidget_2.setGeometry(QtCore.QRect(10, 10, 200, 600))
        self.listWidget_2.setObjectName("listWidget_2")
        self.listWidget_2.setStyleSheet("QListWidget {color: white; font-size: 18px;}")

        #selected code lable
        self.selectedCode = QLabel(self.centralwidget)
        self.selectedCode.setGeometry(QtCore.QRect(230, 625, 280, 31))
        self.selectedCode.setObjectName('selectedCode')
        self.selectedCode.setStyleSheet("color: white; font-size: 10pt;")

        #shourtcut refresh images list
        self._update_key = QShortcut(QKeySequence(Qt.Key_F7), self.centralwidget)
        self._update_key.activated.connect(self.refreshImages)

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1100, 22))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

        #plaintextcode font
        self.plainTextCode.setFont(self.inputFont)

        #connect
        self.listWidget_2.clicked.connect(self.refSelectedCode)
        self.listWidget.itemDoubleClicked.connect(self.openImage)
        self.exeCode.clicked.connect(self.exeCodeClicked)
        self.addCode.clicked.connect(self.saveCode)
        self.listWidget_2.itemDoubleClicked.connect(self.showCode)
        self.excCodeBar.clicked.connect(self.exeSelectedCode)
        self.saveImage.clicked.connect(self.saveImg)
        self.pltImage.clicked.connect(self.pltImageFun)
        self.rollback.clicked.connect(self.rollbackimg)


        self.listWidget_2.clicked.connect(self.refSelectedCode)

        #sorting code list
        self.listWidget_2.setSortingEnabled(True)
    

    def video(self ,img ,fnc ,intr , name,bor = 0) :
        count = 0
        out = cv2.VideoWriter(f'videos/{name}.avi', cv2.VideoWriter_fourcc(*'DIVX'), 60, (img.shape[1], img.shape[0]), True)
        for i in range(bor ,img.shape[0]-bor) :
            for j in range(bor ,img.shape[1]-bor) :
                img[i][j] = fnc(img[i][j])
                count += 1
                if count >= intr :
                    count = 0
                    out.write(cv2.cvtColor(img, cv2.COLOR_RGB2BGR))
        out.release()
        return img

    #image rollback function
    def rollbackimg(self):
        if self.rollbackCount <= 1 :
            print('end of rollback')
            return
            
        self.rollbackCount -= 1

        self.img = Image.open(f'theimage/{self.rollbackCount}.jpg').convert('RGB')
        self.img = np.array(self.img)

        #refresh image
        self.pixmap = QPixmap(f'theimage/{self.rollbackCount}.jpg').scaled(600, 600, Qt.KeepAspectRatio,Qt.SmoothTransformation)
        self.lableImage.setPixmap(self.pixmap)
        print('image rollbacked')

    def refreshImages(self) :
        print('images list refreshed')
        self.listWidget.clear()
        extensions = ('*.jpg', '*.jpeg' ,'*.jfif' ,'*.webp')
        for j in extensions :
            for i in glob.glob(j) :
                item = QListWidgetItem(QIcon(i) , i)
                self.listWidget.insertItem(1,item)

    def refSelectedCode(self,item) :
        if self.listWidget_2.currentItem() is None :
            self.selectedCode.setText('Selected code : None')
            return
        self.selectedCode.setText('Selected code : '+self.listWidget_2.currentItem().text())

    def pltImageFun(self) :
        if self.img is None :
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Warning)
            msg.setText("No image wase selected")
            msg.setInformativeText("Please select image using images bar right side")
            msg.exec()
            return False
        plt.figure(strid())
        plt.imshow(self.img)
        plt.show()

    def saveImg(self) :
        #test
        if self.img is None :
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Warning)
            msg.setText("No image wase selected")
            msg.setInformativeText("Please select image using images bar right side")
            msg.exec()
            return False
            
        saveTo = QFileDialog.getSaveFileName(self.saveImage , filter="Image files (*.jpg)")
        if not saveTo[0]=='' :
            im = Image.fromarray(self.img)
            im.save(saveTo[0])


    def exeSelectedCode(self) :
        if self.selectedCode.text()[16:].strip() != 'None' :
            if not self.exePyText(self.getCodeByFilename(self.listWidget_2.currentItem().text())) :
                msg = QMessageBox()
                msg.setIcon(QMessageBox.Warning)
                msg.setText("No image wase selected")
                msg.setInformativeText("Please select image using images bar right side")
                msg.exec()
                return False
            else :
                reload(my)
                self.rollbackCount += 1
                im = Image.fromarray(self.img)
                im.save(f'theimage/{self.rollbackCount}.jpg')
                #refresh image
                self.pixmap = QPixmap(f'theimage/{self.rollbackCount}.jpg').scaled(600, 600, Qt.KeepAspectRatio,Qt.SmoothTransformation)
            self.lableImage.setPixmap(self.pixmap)
            return True
        else :
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Warning)
            msg.setText("No code was selected")
            msg.exec()
            return False
    #codes list menu

    #get code by file name
    def getCodeByFilename(self ,name) :
        f= open(f"codes//{name}.txt","r")
        code = f.read()
        return code

    #show saved code in pop up

    def showCode(self , item) :
        pup = QDialog()
        #pup.resize()
        pup.setWindowIcon(QIcon('res/python.png'))
        pup.setWindowTitle(item.text())
        code = (self.getCodeByFilename(item.text()))

        pup.setMinimumSize(QtCore.QSize(700, 270))
        pup.setMaximumSize(QtCore.QSize(700, 270))

        codeTextEdit = QPlainTextEdit(pup)
        codeTextEdit.setStyleSheet("QPlainTextEdit {background-color: #181818; color: white; font-size: 16pt;}")
        codeTextEdit.setGeometry(QtCore.QRect(0, 0, 700, 230))
        codeTextEdit.setPlainText(code)

        #delet and save btn
        def deleteCode():
            dlg = QMessageBox(deleteCodeBtn)
            dlg.setStyleSheet('background-color: #232430 ; font-size : 12pt')
            dlg.setWindowTitle("Delete code")
            dlg.setText("Are you sure you want to delete this code ?")
            dlg.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
            dlg.setIcon(QMessageBox.Question)
            ans = dlg.exec()

            if ans == QMessageBox.Yes:
                os.remove(f"codes//{item.text()}.txt")
                self.refreshCodes()
                self.refSelectedCode(item)
                pup.close()

        def saveCode():
            if  fileNameEdit.toPlainText().strip() == '' :
                msg = QMessageBox()
                msg.setIcon(QMessageBox.Warning)
                msg.setText("Name cannot be empty !")
                msg.exec()
                return False

            if ('codes\\'+fileNameEdit.toPlainText()+'.txt' in glob.glob('codes/*.txt')) and (fileNameEdit.toPlainText() != item.text()) :
                msg = QMessageBox()
                msg.setIcon(QMessageBox.Warning)
                msg.setText("File name allready exist !")
                msg.exec()
                return False

            dlg = QMessageBox(deleteCodeBtn)
            dlg.setStyleSheet('background-color: #232430 ; font-size : 12pt')
            dlg.setWindowTitle("Save changes")
            dlg.setText("Are you sure you want to save changes ?")
            dlg.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
            dlg.setIcon(QMessageBox.Question)
            ans = dlg.exec()

            if ans == QMessageBox.Yes:
                f= open(f"codes//{item.text()}.txt","w+")
                f.write(codeTextEdit.toPlainText())
                f.close()
                os.rename(f"codes//{item.text()}.txt",f"codes//{fileNameEdit.toPlainText()}.txt")
                self.refreshCodes()
                self.selectedCode.setText('Selected code : None')
                pup.close()    
            
        saveCodeBtn = QtWidgets.QPushButton(pup)
        saveCodeBtn.setText('Save changes')
        saveCodeBtn.setGeometry(QtCore.QRect(605, 235, 90, 30))
        

        deleteCodeBtn = QtWidgets.QPushButton(pup)
        deleteCodeBtn.setText('Delete')
        deleteCodeBtn.setGeometry(QtCore.QRect(545, 235, 50, 30))
        deleteCodeBtn.setStyleSheet("background-color: #f34542;")

        fileNameLabel = QLabel(pup)
        fileNameLabel.setText('Code Name')
        fileNameLabel.setGeometry(QtCore.QRect(10, 235, 90, 30))
        fileNameLabel.setStyleSheet('font-size : 12pt;')


        fileNameEdit = QtWidgets.QTextEdit(pup)
        fileNameEdit.setPlainText(item.text())
        fileNameEdit.setGeometry(QtCore.QRect(100, 235, 300, 30))
        fileNameEdit.setStyleSheet('background-color: #181818; color: white; font-size : 12pt')

        deleteCodeBtn.clicked.connect(deleteCode)
        saveCodeBtn.clicked.connect(saveCode)

        pup.exec_()



    def saveCode(self ) :
        if self.plainTextCode.toPlainText().strip() == '' :
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Warning)
            msg.setText("Code is empty")
            msg.exec()
            return False
        name, done = QtWidgets.QInputDialog.getText(self.addCode ,'Save new code', 'Enter your code name :')

        if done :
            if name.strip() == '' :
                msg = QMessageBox()
                msg.setIcon(QMessageBox.Warning)
                msg.setText("Name cannot be empty !")
                msg.exec()
                return False
            existing = glob.glob('codes/*.txt')
            if 'codes\\'+name+'.txt' in existing :
                msg = QMessageBox()
                msg.setIcon(QMessageBox.Warning)
                msg.setText(f"Code name '{name}' alredy exist")
                msg.exec()
                return False
        f= open(f"codes//{name}.txt","w+")
        f.write(self.plainTextCode.toPlainText())

        self.refreshCodes()
        
    def refreshCodes(self) :
        self.listWidget_2.clear()
        for i in glob.glob('codes/*.txt') :
            item = QListWidgetItem(QIcon('res/python.png') , i[6:-4])
            self.listWidget_2.insertItem(1,item)

    def openImage(self, item) :
        self.pixmap = QPixmap(item.text()).scaled(600, 600, Qt.KeepAspectRatio,Qt.SmoothTransformation)
        self.lableImage.setPixmap(self.pixmap)

        self.img = Image.open(item.text()).convert('RGB')
        self.img = np.array(self.img)

        print(f'image {item.text()} imported')
        self.rollbackCount = 1

        im = Image.fromarray(self.img)
        im.save(f'theimage/1.jpg')

        print((self.img.shape))

    def exePyText(self ,code) :
        if self.img is None :
            return False
        code = code.replace('img' , 'self.img')
        code = code.replace('storage' , 'self.storage')
        code = code.replace('video' , 'self.video')
        try:
            exec(code)
        except Exception as e: 
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Warning)
            msg.setText("Errore executing python code")
            msg.setInformativeText(str(e))
            msg.exec()
        return True

    def exeCodeClicked(self) :
        if self.plainTextCode.toPlainText().strip() == '' :
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Warning)
            msg.setText("Code is empty")
            msg.exec()
            return False
        reload(my)
        code = self.plainTextCode.toPlainText()

        if not self.exePyText(code) :
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Warning)
            msg.setText("No image wase selected")
            msg.setInformativeText("Please select image using images bar right side")
            msg.exec()
        else :
            self.rollbackCount += 1
            im = Image.fromarray(self.img)
            im.save(f'theimage/{self.rollbackCount}.jpg')
            #refresh image
            self.pixmap = QPixmap(f'theimage/{self.rollbackCount}.jpg').scaled(600, 600, Qt.KeepAspectRatio,Qt.SmoothTransformation)
            self.lableImage.setPixmap(self.pixmap)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Image processing python"))
        self.exeCode.setText(_translate("MainWindow", "Execute code"))
        self.saveImage.setText(_translate("MainWindow", "Save image"))
        self.addCode.setText(_translate("MainWindow", "Add code"))
        self.excCodeBar.setText(_translate("MainWindow", "Execute select"))
        self.lableImage.setText(_translate("MainWindow", "No image"))

        self.pltImage.setText(_translate("MainWindow", "Open image PIL"))
        self.rollback.setText(_translate("MainWindow", "Rollback image"))
        
        self.selectedCode.setText(_translate("MainWindow", "Selected code : None"))

        old_format = self.plainTextCode.currentCharFormat()
        color_format =  self.plainTextCode.currentCharFormat()
        color_format.setForeground(QtGui.QColor('green'))
        self.plainTextCode.setCurrentCharFormat(color_format)

        self.plainTextCode.insertPlainText('#Avoid using (img,storage) in your code reserved words.')
        self.plainTextCode.setCurrentCharFormat(old_format)

        #my edit / font size 
        plainTextfont = QtGui.QFont()
        plainTextfont.setPointSize(16)
        self.plainTextCode.setFont(plainTextfont)


        size = QtCore.QSize(80,80)
        self.listWidget.setIconSize(size)

        extensions = ('*.jpg', '*.jpeg' ,'*.jfif' ,'*.webp')
        for j in extensions :
            for i in glob.glob(j) :
                item = QListWidgetItem(QIcon(i) , i)
                self.listWidget.insertItem(1,item)

        #call saved codes to list
        size = QtCore.QSize(32,32)
        self.listWidget_2.setIconSize(size)
        for i in glob.glob('codes/*.txt') :
            item = QListWidgetItem(QIcon('res/python.png') , i[6:-4])
            self.listWidget_2.insertItem(1,item)

if __name__ == '__main__' :
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()

    File = open("Obit.qss",'r')
    with File:
        qss = File.read()
        app.setStyleSheet(qss)

    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    
    #clear theimage folder
    filelist = glob.glob('theimage/*.jpg')
    
    for f in filelist:
        os.remove(f)
        print(f'image {f} removed.')
    sys.exit(app.exec_())