import sys
import subprocess
import time
from PyQt5.QtWidgets import *
from PyQt5 import QtGui, QtCore
from interface2 import App2

class App(QMainWindow):

    def __init__(self):
        super().__init__()

        self.interface()

    def interface(self):
        self.setWindowTitle('Disk Imaging Applications on Android Phone Using TWRP')
        self.resize(640, 480)
        self.setWindowIcon(QtGui.QIcon("C:/Users/Waldy/Desktop/Skripsi/icon/icon 3.png"))

        menubar = self.menuBar().addMenu('File')
        actionScan = menubar.addAction('Scan')
        actionScan.triggered.connect(self.clk_scn)
        actionExit = menubar.addAction('Exit')
        actionExit.triggered.connect(self.clk_Exit)
        menuAbout = self.menuBar().addMenu('About')
        actionAbout = menuAbout.addAction('About')
        actionAbout.triggered.connect(self.clk_about)

        self.pushBootloader = QPushButton('ADB Reboot-Bootloader', self)
        self.pushBootloader.setGeometry(60, 35, 150, 45)

        self.pushDownload = QPushButton('ADB Reboot-Download', self)
        self.pushDownload.setGeometry(230, 35, 150, 45)

        self.pushRecovery = QPushButton('ADB Reboot-Recovery', self)
        self.pushRecovery.setGeometry(400, 35, 150, 45)

        self.groupBox = QGroupBox("Detect Devices  :", self)
        self.groupBox.setGeometry(50, 90, 400, 140)
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(13)
        self.groupBox.setFont(font)

        self.tableWidget = QTableWidget(self.groupBox)
        self.tableWidget.setGeometry(10, 20, 380, 110)
        self.tableWidget.setColumnCount(3)
        self.tableWidget.setRowCount(0)
        self.tableWidget.setHorizontalHeaderItem(0, QTableWidgetItem('Serial Number'))
        self.tableWidget.setHorizontalHeaderItem(1, QTableWidgetItem('State'))
        self.tableWidget.setHorizontalHeaderItem(2, QTableWidgetItem('Type'))
        self.tableWidget.horizontalHeader().setDefaultSectionSize(125)
        self.tableWidget.horizontalHeader().setStretchLastSection(True)

        self.columnSer = QTextBrowser(self.groupBox)
        self.columnSer.setGeometry(10, 44, 125, 86)
        font = QtGui.QFont()
        font.setPointSize(11)
        self.columnSer.setFont(font)

        self.columnStat = QTextBrowser(self.groupBox)
        self.columnStat.setGeometry(135, 44, 125, 86)
        self.columnStat.setFont(font)

        self.columnType = QTextBrowser(self.groupBox)
        self.columnType.setGeometry(260, 44, 130, 86)
        self.columnType.setFont(font)

        self.pushScan = QPushButton("Scan", self)
        self.pushScan.setGeometry(460, 185, 80, 35)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("../../refres.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pushScan.setIcon(icon)
        self.pushScan.setIconSize(QtCore.QSize(18, 18))

        self.pushCheck = QPushButton('Check', self)
        self.pushCheck.setGeometry(460, 225, 80, 35)

        self.pushCon = QPushButton('Connect', self)
        self.pushCon.setGeometry(550, 195, 80, 55)

        self.groupBox_2 = QGroupBox('Detail  :', self)
        self.groupBox_2.setGeometry(50, 235, 400, 160)
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(12)
        self.groupBox_2.setFont(font)

        self.textDetail = QTextBrowser(self.groupBox_2)
        self.textDetail.setGeometry(10, 20, 381, 130)

        self.pushNext = QPushButton('Next', self)
        self.pushNext.setGeometry(530, 410, 81, 35)
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap("C:/Users/Waldy/Desktop/Skripsi/must_have_icon_set/Next/Next.ico"),
                        QtGui.QIcon.Normal,
                        QtGui.QIcon.Off)
        self.pushNext.setIcon(icon1)

        self.pushExit = QPushButton('Exit', self)
        self.pushExit.setGeometry(440, 410, 81, 35)
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap("C:/Users/Waldy/Desktop/Skripsi/must_have_icon_set/Delete/Delete.ico"),
                        QtGui.QIcon.Normal,
                        QtGui.QIcon.Off)
        self.pushExit.setIcon(icon2)
        self.pushExit.setIconSize(QtCore.QSize(16, 16))

        self.show()

        self.pushNext.setDisabled(True)
        self.pushScan.clicked.connect(self.clk_scn)
        self.pushNext.clicked.connect(self.clk_next)
        self.pushCheck.clicked.connect(self.clk_check)
        self.pushCon.clicked.connect(self.clk_con)
        self.pushExit.clicked.connect(self.clk_Exit)
        self.pushBootloader.clicked.connect(self.clk_Btlder)
        self.pushDownload.clicked.connect(self.clk_Dwnld)
        self.pushRecovery.clicked.connect(self.clk_Rcvry)


    def clk_scn(self):
        subprocess.getoutput('adb start-server')
        serial = subprocess.getoutput('adb devices -l')
        forSerial = subprocess.getoutput('adb get-serialno')
        forStatus = subprocess.getoutput('adb get-state')
        serialNo = forSerial
        status = forStatus
        model = serial[86:95]
        type = serial[57:120]

        self.columnSer.setText(serialNo)
        self.columnStat.setText(status)
        self.columnType.setText(model)

        if forSerial == 'unknown' :
            self.textDetail.setPlainText('Device Not Found')
        else:
            self.textDetail.setPlainText('Device is already')
            self.textDetail.append('Serial No\t: ' +serialNo)
            self.textDetail.append('Status\t: ' +status)
            self.textDetail.append('Type\t: ' +type)

    def clk_check(self):
        var = subprocess.getoutput('adb forward --list')
        text = "{var}".format(var=var)
        device = text[0:16]
        port = text[16:50]

        if text == '':
            self.textDetail.setPlainText("No Connected Devices")
        else:
            self.textDetail.append("Connected Device to\t: " +device)
            self.textDetail.append("Through the port\t: " +port)

    def clk_con(self):
        var2 = subprocess.getoutput('adb get-state')

        if var2 == 'recovery':
            var = subprocess.getoutput('adb forward tcp:8888 tcp:8888')
            text = "{var}".format(var=var)
            if text == '':
                self.textDetail.setPlainText("Device Connected")
                self.pushNext.setDisabled(False)

        elif var2 == 'unknown':
            QMessageBox.about(self, 'Caution','No Devices Detected')
            self.textDetail.setPlainText("Device Not Connected")

        elif var2 == 'device':
            QMessageBox.about(self, 'Caution', 'Device not in Recovery Mode')


    def clk_Exit(self):
        reply = QMessageBox.question(self, "Caution",
                                     "Are you sure to exit?", QMessageBox.No | QMessageBox.Yes)

        if reply == QMessageBox.Yes:
            subprocess.call('adb kill-server')
            QApplication.quit()
        else:
            pass


    def clk_Btlder(self):
        cekdev = subprocess.getoutput('adb get-state')

        if cekdev == 'unknown':
            QMessageBox.about(self, 'Caution', 'Device not found or device in bootloader mode')
            self.textDetail.setPlainText("Device not found or Device in bootloader mode")

        elif cekdev == 'recovery':
            QMessageBox.about(self, 'Caution', 'Device in Recovery Mode')
            self.textDetail.setPlainText("Device in Recovery Mode, You can do the Acquisition process")

        elif cekdev == 'device':
            subprocess.call('adb reboot bootloader')
            QMessageBox.about(self, "Waiting", "Wait until the phone stops processing")

            time.sleep(5)

            cekboot2 = subprocess.getoutput('adb get-state')

            if cekboot2 == 'device':
                self.textDetail.setPlainText("don't have booloader mode, please try the download mode")

            else:
                self.textDetail.setPlainText("Device in bootloader mode, please flashing file TWRP, don't forget unlock bootloder first")
                self.textDetail.append("Tutorial on website 'https://www.xda-developers.com/how-to-install-twrp/'")


    def clk_Dwnld(self):

        cekdev2 = subprocess.getoutput('adb get-state')

        if cekdev2 == 'unknown':
            QMessageBox.about(self, 'Caution', 'Device not found or Device in download mode')
            self.textDetail.setPlainText("Device not found or Device in download mode")

        elif cekdev2 == 'recovery':
            QMessageBox.about(self, 'Caution', 'Devices in Recovery Mode')
            self.textDetail.setPlainText("Device in Recovery Mode, You can do the Acqusition process")

        elif cekdev2 == 'device':
            subprocess.call('adb reboot download')
            QMessageBox.about(self, "Waiting", "Wait until the phone stops processing")

            time.sleep(5)

            cekboot2 = subprocess.getoutput('adb get-state')

            if cekboot2 == 'unknown':
                self.textDetail.setPlainText("Device in download mode, please flashing file TWRP your phone with odin")

            elif cekboot2 == 'device':
                self.textDetail.setPlainText("this phone don't have download mode, please flashing twrp with adb and fastboot or Apps twrp official")


    def clk_Rcvry(self):

        cekdev3 = subprocess.getoutput('adb get-state')

        if cekdev3 == 'unknown':
            QMessageBox.about(self, 'Caution', 'Device not found')
            self.textDetail.setPlainText("Device not found")

        elif cekdev3 == 'recovery':
            QMessageBox.about(self, 'Caution', 'Devices Recovery Mode')
            self.textDetail.setPlainText("Device in Recovery Mode, You can do the Acqusition process")

        elif cekdev3 == 'device':
            subprocess.call('adb reboot recovery')
            QMessageBox.about(self, "Waiting", "Wait until the phone stops processing")

            time.sleep(5)

            cekboot3 = subprocess.getoutput('adb get-state')

            if cekboot3 == 'recovery':
                self.textDetail.setPlainText("Device in recovery mode, You can do the Acqusition process")

            elif cekboot3 == 'device':
                self.textDetail.setPlainText("The Phone has not been installed TWRP")


    def clk_next(self):
        self.window2 = App2()
        self.window2.window1 = self
        self.window2.show()
        self.hide()

    def clk_about(self):
        QMessageBox.about(self, "About Application", "This Application is built with the Python programing language"
                                                     "\n\nThis Application is to acquire Android storage with recovery mode/TWRP based on Windows platform"
                                                     "\n\nThe Application can be run if the Android phone in recovery mode/TWRP designed to maintain the integrity of a files that will be generated"
                                                     "\n\nFor install TWRP can be visited on the site: https://twrp.me/Devices/ or https://www.xda-developers.com/how-to-install-twrp/"
                                                     "\n\nCopyright (C) 2018 - Waldy Nur Hamzah")

    def closeEvent(self, eventQCloseEvent):
        reply = QMessageBox.question(self, "Caution",
                                     "Are you sure to exit",
                                     QMessageBox.Yes | QMessageBox.No)
        if reply == QMessageBox.Yes:
            subprocess.call('adb kill-server')
            eventQCloseEvent.accept()
        else:
            eventQCloseEvent.ignore()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec())
