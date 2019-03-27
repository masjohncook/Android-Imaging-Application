import sys
import subprocess
import time
import datetime
import os
import pyadb3
import hashlib
import logging
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5 import QtGui, QtCore


class ShellHpInt(QThread):

    def run(self):
        try:
            shellInt = pyadb3.ADB()
            shellInt.run_shell_cmd("dd if=/dev/block/mmcblk0 | busybox nc -l -p 8888")

        except Exception:
            print("Error")

class ShellHpExt(QThread):

    def run(self):
        try:
            shellExt = pyadb3.ADB()
            shellExt.run_shell_cmd("dd if=/dev/block/mmcblk1 | busybox nc -l -p 8888")

        except Exception:
            print("Error")


class NetcatInt(QThread):
    def run(self):
        ncDetail = App2.textDetailGlobal
        ncOutFile = App2.outFileGlobal
        ncNameFileLog = App2.lineFileGlobal
        ncDirect = App2.devPath
        ncExam = App2.globalExa

        ncNameFileInt = ncNameFileLog+ "_Int"
        fullNameFile = ncNameFileInt + ".dd"
        bDirect = "/" + fullNameFile
        allDirect = ncDirect + bDirect

        ncLog = ncNameFileLog+ ".log"
        ncOutLog = ncDirect + "/" + ncLog

        klikMulaiInt = App2.klikMulai

        logging.basicConfig(filename=ncOutLog, level=logging.INFO, format='%(levelname)s:%(message)s')

        try:
            commentNcInt = subprocess.getoutput('nc 127.0.0.1 8888 > ' + ncOutFile + '/' + fullNameFile)

        except Exception:
            print("Error")

        if commentNcInt == '':
            selesaiAkusisiInt = datetime.datetime.today().strftime("%d %B %Y, %H:%M:%S")
            ncDetail.append("---- The Process of Acquisition Internal Storage has been Completed ----")
            ncDetail.append("Start Acquistion\t: " + klikMulaiInt)
            ncDetail.append("End Acquistion\t: " + selesaiAkusisiInt)
            ncDetail.append("\t\t----- Calculate Hashing Internal -----")

            block_size = 2 ** 20
            md5a = hashlib.md5()
            with open(allDirect, 'rb') as fileCloning:
                while True:
                    readCloning = fileCloning.read(block_size)
                    if not readCloning:
                        break
                    md5a.update(readCloning)

            hasilCloningInt = md5a.hexdigest()

            adbHashInt = pyadb3.ADB()
            coHashInt = adbHashInt.run_shell_cmd("md5sum /dev/block/mmcblk0")
            splitHashInt = "{coHashInt}".format(coHashInt=coHashInt)
            hasilHashInt = splitHashInt[2:34]

            ncDetail.append("File Name\t\t: " + fullNameFile)
            ncDetail.append("Directory\t\t: " + allDirect)
            ncDetail.append("Md5 Source\t\t: " + hasilHashInt)
            ncDetail.append("Md5 Cloning\t\t: " + hasilCloningInt)

            logging.info("Examiner\t\t: {}\n".format(ncExam))
            logging.info("---- The Results of an Internal Image File ----")
            logging.info("Storage\t\t: Internal")
            logging.info("Source Directory\t: /dev/block/mmcblk0\n")
            logging.info("Start Acquistion\t: {}".format(klikMulaiInt))
            logging.info("End Acquistion\t: {}\n".format(selesaiAkusisiInt))
            logging.info("File Name\t\t: {}".format(fullNameFile))
            logging.info("Directory\t\t: {}".format(allDirect))
            logging.info("Source MD5 Hash\t: {}".format(hasilHashInt))
            logging.info("Cloning MD5 Hash\t: {}".format(hasilCloningInt))

            if hasilHashInt == hasilCloningInt:
                ncDetail.append("Md5 Hash Matched\n")
                logging.info("MD5 Hash Matched\n")
            else:
                ncDetail.append("Md5 Hash Not Matched\n")
                logging.info("MD5 Hash Not Matched\n")

class NetcatExt(QThread):
    def run(self):
        ncDetail = App2.textDetailGlobal
        ncOutFile = App2.outFileGlobal
        ncNameFileLog = App2.lineFileGlobal
        ncDirect = App2.devPath
        ncExam = App2.globalExa

        ncNameFileExt = ncNameFileLog+ "_Ext"
        fullNameFile = ncNameFileExt + ".dd"
        bDirect = "/" + fullNameFile
        allDirect = ncDirect + bDirect

        ncLog = ncNameFileLog+ ".log"
        ncOutLog = ncDirect + "/" + ncLog

        klikMulaiExt = App2.klikMulai

        logging.basicConfig(filename=ncOutLog, level=logging.INFO, format='%(levelname)s:%(message)s')

        try:
            commentNcExt = subprocess.getoutput('nc 127.0.0.1 8888 > ' + ncOutFile + '/' + fullNameFile)

        except Exception:
            print("Error")

        if commentNcExt == '':
            selesaiAkusisiExt = datetime.datetime.today().strftime("%d %B %Y, %H:%M:%S")
            ncDetail.append("---- The Process of Acquisition External Storage has been Completed ----")
            ncDetail.append("Start Acquisition\t: " + klikMulaiExt)
            ncDetail.append("End Acquisition\t: " + selesaiAkusisiExt)
            ncDetail.append("\t\t----- Calculate Hashing External -----")

            block_size = 2 ** 20
            md5b = hashlib.md5()
            with open(allDirect, 'rb') as fileCloning:
                while True:
                    readCloning = fileCloning.read(block_size)
                    if not readCloning:
                        break
                    md5b.update(readCloning)

            hasilCloningExt = md5b.hexdigest()

            adbHashExt = pyadb3.ADB()
            coHashExt = adbHashExt.run_shell_cmd("md5sum /dev/block/mmcblk1")
            splitHashExt = "{coHashExt}".format(coHashExt=coHashExt)
            hasilHashExt = splitHashExt[2:34]

            ncDetail.append("File Name\t\t: " +fullNameFile)
            ncDetail.append("Directory\t\t: " +allDirect)
            ncDetail.append("Md5 Source\t\t: " + hasilHashExt)
            ncDetail.append("Md5 Cloning\t\t: " +hasilCloningExt)

            logging.info("Examiner\t\t: {}\n".format(ncExam))
            logging.info("---- The Results of an External Image File ----")
            logging.info("Storage\t\t: External")
            logging.info("Source Directory\t: /dev/block/mmcblk1\n")
            logging.info("Start Acquisition\t: {}".format(klikMulaiExt))
            logging.info("End Acquisition\t: {}\n".format(selesaiAkusisiExt))
            logging.info("File Name\t\t: {}".format(fullNameFile))
            logging.info("Directory\t\t: {}".format(allDirect))
            logging.info("Source MD5 Hash\t: {}".format(hasilHashExt))
            logging.info("Cloning MD5 Hash\t: {}".format(hasilCloningExt))

            if hasilHashExt == hasilCloningExt:
                ncDetail.append("Md5 Hash Matched\n")
                logging.info("MD5 Hash Matched\n")
            else:
                ncDetail.append("Md5 Hash Not Matched\n")
                logging.info("MD5 Hash Not Matched\n")


TIME_LIMIT = 1000000000

class ProgressBarInt(QThread):

    countChangedInt = pyqtSignal(int)
    def run(self):
        count = 0
        pbNameFile = App2.lineFileGlobal+ "_Int"
        PbOutFileInt = App2.outFileGlobal
        PbNameFileInt = pbNameFile +".dd"
        PbAll = PbOutFileInt+"/"+PbNameFileInt
        PbAllReplace = PbAll.replace("/","//")

        while count < TIME_LIMIT:
            count +=1
            time.sleep(1)
            size=0
            try:
                size = os.path.getsize(PbAllReplace)
                size = size / 1024

            except:
                print("File Belum ada")

            self.countChangedInt.emit(size)
            if (size >= App2.sizePbInt):
                break

TIME_LIMIT2 = 1000000000
class ProgressBarExt(QThread):

    countChangedExt = pyqtSignal(int)

    def run(self):
        count = 0
        pbNameFile = App2.lineFileGlobal+ "_Ext"
        PbOutFileExt = App2.outFileGlobal
        PbNameFileExt = pbNameFile + ".dd"
        PbAll = PbOutFileExt + "/" + PbNameFileExt
        PbAllReplace = PbAll.replace("/", "//")

        while count < TIME_LIMIT2:
            count += 1
            time.sleep(1)
            size = 0
            try:
                size = os.path.getsize(PbAllReplace)
                size = size / 1024

            except:
                print("File Belum ada")

            self.countChangedExt.emit(size)
            if (size >= App2.sizePbExt):
                break


class App2(QMainWindow):
    sizePbInt=0
    sizePbExt=0

    def __init__(self):
        super().__init__()
        self.window1 = None
        self.directBack = False

        self.interface()

    def interface(self):
        self.resize(640, 480)
        self.setWindowTitle('Disk Imaging Applications on Android Phone Using TWRP')
        self.setWindowIcon(QtGui.QIcon("C:/Users/Waldy/Desktop/Skripsi/icon/icon 3.png"))

        menubar = self.menuBar().addMenu('File')
        actionExit = menubar.addAction('Exit')
        actionExit.triggered.connect(self.clk_Exit)
        menuAbout = self.menuBar().addMenu('About')
        actionAbout = menuAbout.addAction('About')
        actionAbout.triggered.connect(self.clk_about)

        self.groupBox = QGroupBox("Destination File :", self)
        self.groupBox.setGeometry(40, 25, 540, 165)
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(13)
        self.groupBox.setFont(font)

        self.textFileInt = QLabel('File Name    : ', self.groupBox)
        self.textFileInt.setGeometry(30, 25, 130, 25)
        font = QtGui.QFont()
        font.setPointSize(11)
        self.textFileInt.setFont(font)

        self.lineFile = QLineEdit(self.groupBox)
        self.lineFile.setGeometry(130, 25, 320, 25)

        self.textImage = QLabel('Image Type  :', self.groupBox)
        self.textImage.setGeometry(30, 55, 81, 25)
        font = QtGui.QFont()
        font.setPointSize(11)
        self.textImage.setFont(font)

        self.checkDD = QRadioButton('Raw (.dd)', self.groupBox)
        self.checkDD.setGeometry(130, 60, 81, 20)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.checkDD.setFont(font)

        self.textStorage = QLabel('Storage      :', self.groupBox)
        self.textStorage.setGeometry(290, 55, 81, 25)
        font = QtGui.QFont()
        font.setPointSize(11)
        self.textStorage.setFont(font)

        self.radioExternal = QCheckBox('External', self.groupBox)
        self.radioExternal.setGeometry(370, 70, 81, 20)
        self.radioExternal.toggled.connect(self.radio_toggled)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.radioExternal.setFont(font)

        self.radioInternal = QCheckBox('Internal', self.groupBox)
        self.radioInternal.setGeometry(370, 55, 81, 20)
        self.radioInternal.toggled.connect(self.radio_toggled)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.radioInternal.setFont(font)

        self.textExa = QLabel('Examiner     :', self.groupBox)
        self.textExa.setGeometry(30, 95, 82, 25)
        font = QtGui.QFont()
        font.setPointSize(11)
        self.textExa.setFont(font)

        self.lineExa = QLineEdit(self.groupBox)
        self.lineExa.setGeometry(130, 95, 320, 25)

        self.textOut = QLabel('Output Location  :', self.groupBox)
        self.textOut.setGeometry(30, 130, 121, 25)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.textOut.setFont(font)

        self.lineOut = QLineEdit(self.groupBox)
        self.lineOut.setGeometry(130, 130, 320, 25)
        self.lineOut.setDisabled(True)

        self.toolFolder = QToolButton(self.groupBox)
        self.toolFolder.setGeometry(455, 130, 31, 25)
        self.toolFolder.setText("")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("C:/Users/Waldy/Desktop/Skripsi/must_have_icon_set/Folder/Folder.ico"),
                       QtGui.QIcon.Normal,
                       QtGui.QIcon.Off)
        self.toolFolder.setIcon(icon)
        self.toolFolder.setIconSize(QtCore.QSize(20, 20))

        self.textProgressInt = QLabel('Acquisition Progress : Int :', self)
        self.textProgressInt.setGeometry(20, 200, 155, 25)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.textProgressInt.setFont(font)

        self.progressBar = QProgressBar(self)
        self.progressBar.setGeometry(180, 200, 400, 25)
        self.progressBar.setProperty("value", 0)

        self.textProgressExt = QLabel('Ext :', self)
        self.textProgressExt.setGeometry(145, 230, 155, 25)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.textProgressExt.setFont(font)

        self.progressBarExt = QProgressBar(self)
        self.progressBarExt.setGeometry(180, 230, 400, 25)
        self.progressBarExt.setProperty("value", 0)

        self.groupBox2 = QGroupBox('Detail  :', self)
        self.groupBox2.setGeometry(40, 255, 540, 160)
        font = QtGui.QFont()
        font.setPointSize(11)
        font.setWeight(50)
        self.groupBox2.setFont(font)

        self.textBrowser = QTextBrowser(self.groupBox2)
        self.textBrowser.setGeometry(10, 20, 520, 130)

        self.pushBack = QPushButton('Back', self)
        self.pushBack.setGeometry(440, 425, 81, 35)
        self.pushBack.setLayoutDirection(QtCore.Qt.LeftToRight)
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap("C:/Users/Waldy/Desktop/Skripsi/must_have_icon_set/Previous/Previous.ico"),
                        QtGui.QIcon.Normal,
                        QtGui.QIcon.Off)
        self.pushBack.setIcon(icon1)
        self.pushBack.setIconSize(QtCore.QSize(18, 18))

        self.pushExtract = QPushButton('Extract', self)
        self.pushExtract.setGeometry(530, 425, 81, 35)
        self.pushExtract.setLayoutDirection(QtCore.Qt.LeftToRight)
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap("C:/Users/Waldy/Desktop/Skripsi/extrak.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pushExtract.setIcon(icon1)
        self.pushExtract.setIconSize(QtCore.QSize(18, 20))

        self.show()

        self.pushExtract.setDisabled(True)

        self.lineFile.textChanged.connect(self.disableExtract)
        self.lineOut.textChanged.connect(self.disableExtract)
        self.lineExa.textChanged.connect(self.disableExtract)
        self.checkDD.toggled.connect(self.disableExtract)
        self.radioInternal.toggled.connect(self.disableExtract)
        self.radioExternal.toggled.connect(self.disableExtract)

        self.toolFolder.clicked.connect(self.clk_fold)
        self.pushExtract.clicked.connect(self.clk_extr)
        self.pushBack.clicked.connect(self.clk_back)

    def disableExtract(self):

        if self.checkDD.isChecked() and self.radioInternal.isChecked() and len(self.lineFile.text() and self.lineExa.text() and self.lineOut.text()) > 0:
            self.pushExtract.setDisabled(False)
            if self.radioExternal.isChecked():
                self.pushExtract.setDisabled(False)

        elif self.checkDD.isChecked() and self.radioExternal.isChecked() and len(self.lineFile.text() and self.lineExa.text() and self.lineOut.text()) > 0:
            self.pushExtract.setDisabled(False)
            if self.radioInternal.isChecked():
                self.pushExtract.setDisabled(False)

        else:
            self.pushExtract.setDisabled(True)

    def onCountChangedInt(self, value):
        self.progressBar.setValue(value)

    def onCountChangedExt(self, value):
        self.progressBarExt.setValue(value)


    def clk_fold(self):
        self.folderPath = QFileDialog.getExistingDirectory(self, 'Select Folder')
        self.lineOut.setText(self.folderPath)

    def clk_Exit(self):
        reply = QMessageBox.question(self, "Caution",
                                     "Äre you sure to exit?", QMessageBox.No | QMessageBox.Yes)

        if reply == QMessageBox.Yes:
            subprocess.call('adb kill-server')
            QApplication.quit()
        else:
            pass

    def clk_back(self):
        self.directBack = True
        self.window1.show()
        self.destroy()
        self.close()


    def closeEvent(self, eventQCloseEvent):
        if self.directBack == True:
            eventQCloseEvent.accept()
        else:
            reply = QMessageBox.question(self, "Caution",
                                         "All running processes will be canceled \nAre you sure to exit",
                                         QMessageBox.Yes | QMessageBox.No)
            if reply == QMessageBox.Yes:
                subprocess.call('adb kill-server')
                eventQCloseEvent.accept()
            else:
                eventQCloseEvent.ignore()


    def clk_extr(self):
        App2.outFileGlobal = self.lineOut.text()
        App2.lineFileGlobal = self.lineFile.text()
        App2.textDetailGlobal = self.textBrowser
        App2.globalExa = self.lineExa.text()
        App2.devPath = self.folderPath
        App2.klikMulai = datetime.datetime.today().strftime("%d %B %Y, %H:%M:%S")
        checkint = self.radioInternal.isChecked()
        checkExt = self.radioExternal.isChecked()

        self.textBrowser.setPlainText("Examiner\t   : " +App2.globalExa)

        if checkint and checkExt:
            self.textBrowser.setPlainText("Storage\t\t: Internal")
            self.textBrowser.append("Source Directory Int\t: /dev/block/mmcblk0")

            adbSize = pyadb3.ADB()
            adbSizeOut = adbSize.run_shell_cmd("cat /proc/partitions | grep mmcblk0")
            sizeSplitInt = adbSizeOut.split()[2]
            sizeReplace = "{sizeSplitInt}".format(sizeSplitInt=sizeSplitInt).replace("b", "").replace("'", "")
            sizeforInt = int(sizeReplace)/1024/1024
            self.progressBar.setMaximum(int(sizeReplace))
            App2.sizePbInt = int(sizeReplace)
            self.textBrowser.append("Size Storage Int\t:" +str(sizeforInt) +" GB\n")

            self.textBrowser.append("Storage\t\t: External")
            self.textBrowser.append("Source Directory Ext\t: /dev/block/mmcblk1")

            adbSize2 = pyadb3.ADB()
            adbSizeOut2 = adbSize2.run_shell_cmd("cat /proc/partitions | grep mmcblk1")
            sizeSplitExt = adbSizeOut2.split()[2]
            sizeReplace2 = "{sizeSplitExt}".format(sizeSplitExt=sizeSplitExt).replace("b", "").replace("'", "")
            sizeforExt = int(sizeReplace2)/1024/1024
            self.progressBarExt.setMaximum(int(sizeReplace2))
            App2.sizePbExt = int(sizeReplace2)
            self.textBrowser.append("Size Storage Ext\t:" +str(sizeforExt) +" GB\n")

            self.forShellInt = ShellHpInt()
            self.forShellInt.start()

            time.sleep(3)

            self.forNcInt = NetcatInt()
            self.forNcInt.start()
            self.bar1 = ProgressBarInt()
            self.bar1.countChangedInt.connect(self.onCountChangedInt)
            self.bar1.start()

            time.sleep(3)

            self.forShellExt = ShellHpExt()
            self.forShellExt.start()

            time.sleep(3)

            self.forNcExt = NetcatExt()
            self.forNcExt.start()
            self.bar2 = ProgressBarExt()
            self.bar2.countChangedExt.connect(self.onCountChangedExt)
            self.bar2.start()


        elif self.radioInternal.isChecked():
            self.textBrowser.setPlainText("Storage\t\t: Internal")
            self.textBrowser.append("Source Directory Int\t: /dev/block/mmcblk0")

            adbSize = pyadb3.ADB()
            adbSizeOut = adbSize.run_shell_cmd("cat /proc/partitions | grep mmcblk0")
            sizeSplitInt = adbSizeOut.split()[2]
            sizeReplace = "{sizeSplitInt}".format(sizeSplitInt=sizeSplitInt).replace("b", "").replace("'", "")
            sizeforInt = int(sizeReplace) /1024/1024
            self.progressBar.setMaximum(int(sizeReplace))
            App2.sizePbInt = int(sizeReplace)
            self.textBrowser.append("Size Storage Int\t:" +str(sizeforInt) +" GB\n")

            self.forShellInt = ShellHpInt()
            self.forShellInt.start()

            time.sleep(3)

            self.forNcInt = NetcatInt()
            self.forNcInt.start()
            self.bar1 = ProgressBarInt()
            self.bar1.countChangedInt.connect(self.onCountChangedInt)
            self.bar1.start()

        elif self.radioExternal.isChecked():
            self.textBrowser.append("Storage\t\t: External")
            self.textBrowser.append("Source Directory Ext\t: /dev/block/mmcblk1")

            adbSize2 = pyadb3.ADB()
            adbSizeOut2 = adbSize2.run_shell_cmd("cat /proc/partitions | grep mmcblk1")
            sizeSplitExt = adbSizeOut2.split()[2]
            sizeReplace2 = "{sizeSplitExt}".format(sizeSplitExt=sizeSplitExt).replace("b", "").replace("'", "")
            sizeforExt = int(sizeReplace2) /1024/1024
            self.progressBarExt.setMaximum(int(sizeReplace2))
            App2.sizePbExt = int(sizeReplace2)
            self.textBrowser.append("Size Storage Ext\t:" +str(sizeforExt) +" GB\n")

            self.forShellExt = ShellHpExt()
            self.forShellExt.start()

            time.sleep(3)

            self.forNcExt = NetcatExt()
            self.forNcExt.start()
            self.bar2 = ProgressBarExt()
            self.bar2.countChangedExt.connect(self.onCountChangedExt)
            self.bar2.start()

        else:
            self.textBrowser.setPlainText("no choice")


    def radio_toggled(self):

        App2.radioExt = self.radioExternal.isChecked()
        App2.radioInt = self.radioInternal.isChecked()

        if App2.radioInt and App2.radioExt:
            self.textBrowser.setPlainText("Storage\t\t: Internal")
            self.textBrowser.append("Source Directory Int\t: /dev/block/mmcblk0")
            self.textBrowser.append("Storage\t\t: External")
            self.textBrowser.append("Source Directory Ext\t: /dev/block/mmcblk1")

        elif self.radioInternal.isChecked():
            self.textBrowser.setPlainText("Storage\t\t: Internal")
            self.textBrowser.append("Source Directory Int\t: /dev/block/mmcblk0")

        elif self.radioExternal.isChecked():
            cekStatusExt = pyadb3.ADB()
            statusExt = cekStatusExt.run_shell_cmd("cat /proc/partitions | grep mmcblk1")
            cekExt = "{statusExt}".format(statusExt=statusExt).replace("b", "").replace("'", "")
            self.textBrowser.append(str("adakek" + cekExt))
            if cekExt == '':
                self.textBrowser.append("external storage not found")
                self.radioExternal.setCheckState(False)
                self.radioExternal.setDisabled(True)
            else:
                self.textBrowser.setPlainText("Storage\t\t: External")
                self.textBrowser.append("Source Directory Ext\t: /dev/block/mmcblk1")


    def clk_about(self):
        QMessageBox.about(self, "About", "This Application is built with the Python programing language"
                                         "\n\nThis Application is to acquire Android storage with recovery mode/TWRP based on Windows platform"
                                         "\n\nThe Application can be run if the Android phone in recovery mode/TWRP designed to maintain the integrity of a files that will be generated"
                                         "\n\nFor install TWRP can be visited on the site: https://twrp.me/Devices/ or https://www.xda-developers.com/how-to-install-twrp/"
                                         "\n\nCopyright (C) 2018 - Waldy Nur Hamzah")


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App2()
    sys.exit(app.exec())
