from PyQt5 import QtCore, QtGui, QtWidgets
import pip._vendor.requests as request
from PyQt5 import QtCore as qtc
from PyQt5.QtWidgets import QMessageBox
import sys
from helper import headers


class Ui_DialogWindow_add(QtWidgets.QWidget):
    submitClicked = qtc.pyqtSignal(str)

    def setupUi(self, DialogWindow_add):
        DialogWindow_add.setObjectName("DialogWindow_add")
        DialogWindow_add.resize(480, 600)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(DialogWindow_add.sizePolicy().hasHeightForWidth())
        DialogWindow_add.setSizePolicy(sizePolicy)
        DialogWindow_add.setMinimumSize(QtCore.QSize(480, 600))
        DialogWindow_add.setMaximumSize(QtCore.QSize(480, 600))
        DialogWindow_add.setStyleSheet("background-color: rgb(100, 204, 197);")
        self.pushButton_dialog_add = QtWidgets.QPushButton(DialogWindow_add, clicked=lambda: self.addTickerToList())
        self.pushButton_dialog_add.setGeometry(QtCore.QRect(170, 550, 151, 31))
        font = QtGui.QFont()
        font.setFamily("MS Shell Dlg 2")
        font.setPointSize(10)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        self.pushButton_dialog_add.setFont(font)
        self.pushButton_dialog_add.setStyleSheet("border-radius: 50;; border : 1px solid black; padding: 4 12; \n"
"background-color: rgb(23, 107, 135);\n"
"border-color: rgb(218, 255, 251);\n"
"color: rgb(218, 255, 251);\n"
"font: 10pt \"MS Shell Dlg 2\";")
        self.pushButton_dialog_add.setObjectName("pushButton_dialog_add")
        self.label_dialog_add = QtWidgets.QLabel(DialogWindow_add)
        self.label_dialog_add.setGeometry(QtCore.QRect(-10, 10, 491, 41))
        font = QtGui.QFont()
        font.setFamily("MS Shell Dlg 2")
        font.setPointSize(14)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(9)
        self.label_dialog_add.setFont(font)
        self.label_dialog_add.setStyleSheet("font: 75 14pt \"MS Shell Dlg 2\";\n"
"color: rgb((0, 28, 48));")
        self.label_dialog_add.setAlignment(QtCore.Qt.AlignCenter)
        self.label_dialog_add.setObjectName("label_dialog_add")
        self.lineTicker_add = QtWidgets.QLineEdit(DialogWindow_add)
        self.lineTicker_add.setGeometry(QtCore.QRect(20, 60, 321, 31))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.lineTicker_add.setFont(font)
        self.lineTicker_add.setStyleSheet("background-color:  rgb(218, 255, 251);\n"
"color: rgb(0, 28, 48);\n"
"")
        self.lineTicker_add.setText("")
        self.lineTicker_add.setObjectName("lineTicker_add")
        self.tableWidget_stockList_add = QtWidgets.QTableWidget(DialogWindow_add)
        self.tableWidget_stockList_add.setGeometry(QtCore.QRect(20, 110, 438, 431))
        self.tableWidget_stockList_add.setStyleSheet("background-color: rgb(255, 255, 255);\n"
"color: rgb(0, 28, 48);")
        self.tableWidget_stockList_add.setObjectName("tableWidget_stockList_add")
        self.tableWidget_stockList_add.setColumnCount(4)
        self.tableWidget_stockList_add.setRowCount(0)
        item = QtWidgets.QTableWidgetItem()
        font = QtGui.QFont()
        font.setPointSize(9)
        item.setFont(font)
        self.tableWidget_stockList_add.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        font = QtGui.QFont()
        font.setPointSize(9)
        item.setFont(font)
        self.tableWidget_stockList_add.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        font = QtGui.QFont()
        font.setPointSize(9)
        item.setFont(font)
        self.tableWidget_stockList_add.setHorizontalHeaderItem(2, item)
        item = QtWidgets.QTableWidgetItem()
        font = QtGui.QFont()
        font.setPointSize(9)
        item.setFont(font)
        self.tableWidget_stockList_add.setHorizontalHeaderItem(3, item)
        self.tableWidget_stockList_add.horizontalHeader().setDefaultSectionSize(109)
        self.pushButton_dialog_add_2 = QtWidgets.QPushButton(DialogWindow_add, clicked=lambda: self.searchSymbol())
        self.pushButton_dialog_add_2.setGeometry(QtCore.QRect(360, 60, 91, 31))
        font = QtGui.QFont()
        font.setFamily("MS Shell Dlg 2")
        font.setPointSize(10)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        self.pushButton_dialog_add_2.setFont(font)
        self.pushButton_dialog_add_2.setStyleSheet("border-radius: 50;; border : 1px solid black; padding: 4 12; \n"
"background-color: rgb(23, 107, 135);\n"
"border-color: rgb(218, 255, 251);\n"
"color: rgb(218, 255, 251);\n"
"font: 10pt \"MS Shell Dlg 2\";")
        self.pushButton_dialog_add_2.setObjectName("pushButton_dialog_add_2")

        self.retranslateUi(DialogWindow_add)
        QtCore.QMetaObject.connectSlotsByName(DialogWindow_add)

        #load stock list
        self.loadStockList()

    def retranslateUi(self, DialogWindow_add):
        _translate = QtCore.QCoreApplication.translate
        DialogWindow_add.setWindowTitle(_translate("DialogWindow_add", "Search Symbol"))
        self.pushButton_dialog_add.setText(_translate("DialogWindow_add", "Add"))
        self.label_dialog_add.setText(_translate("DialogWindow_add", "Add Ticker to Watch List"))
        self.lineTicker_add.setPlaceholderText(_translate("DialogWindow_add", "Ticker"))
        item = self.tableWidget_stockList_add.horizontalHeaderItem(0)
        item.setText(_translate("DialogWindow_add", "Ticker"))
        item = self.tableWidget_stockList_add.horizontalHeaderItem(1)
        item.setText(_translate("DialogWindow_add", "Name"))
        item = self.tableWidget_stockList_add.horizontalHeaderItem(2)
        item.setText(_translate("DialogWindow_add", "Exchange"))
        item = self.tableWidget_stockList_add.horizontalHeaderItem(3)
        item.setText(_translate("DialogWindow_add", "Country"))
        self.pushButton_dialog_add_2.setText(_translate("DialogWindow_add", "Find Ticker"))

    def loadStockList(self):
        url = "https://twelve-data1.p.rapidapi.com/stocks"
        querystring = {"exchange":"NASDAQ","format":"json"}
        response = request.get(url, headers=headers, params=querystring).json()

        list = response['data']
        row=0
        self.tableWidget_stockList_add.setRowCount(len(list))
        for ticker in list:
            self.tableWidget_stockList_add.setItem(row, 0, QtWidgets.QTableWidgetItem(f"{ticker['symbol']}"))
            self.tableWidget_stockList_add.setItem(row, 1, QtWidgets.QTableWidgetItem(f"{ticker['name']}"))
            self.tableWidget_stockList_add.setItem(row, 2, QtWidgets.QTableWidgetItem(f"{ticker['exchange']}"))
            self.tableWidget_stockList_add.setItem(row, 3, QtWidgets.QTableWidgetItem(f"{ticker['country']}"))
            row=row+1

    def searchSymbol(self):
        try:
            symbol = self.lineTicker_add.text().upper()
            self.label_dialog_add.setText(f'You searched for {symbol}')
        except TypeError:
            QMessageBox.information(self, "Empty Field", "Please enter a valid ticker")

        url = "https://twelve-data1.p.rapidapi.com/symbol_search"
        querystring = {"symbol":symbol,"outputsize":"1"}
        response = request.get(url, headers=headers, params=querystring).json()

        row=0
        self.tableWidget_stockList_add.setRowCount(len(response['data']))

        self.lineTicker_add.clear()
        for ticker in response['data']:
            if ticker['country'] == 'United States':
                self.tableWidget_stockList_add.setItem(row, 0, QtWidgets.QTableWidgetItem(f"{ticker['symbol']}"))
                self.tableWidget_stockList_add.setItem(row, 1, QtWidgets.QTableWidgetItem(f"{ticker['instrument_name']}"))
                self.tableWidget_stockList_add.setItem(row, 2, QtWidgets.QTableWidgetItem(f"{ticker['exchange']}"))
                self.tableWidget_stockList_add.setItem(row, 3, QtWidgets.QTableWidgetItem(f"{ticker['country']}"))
                row=row+1
            else: return

    @QtCore.pyqtSlot(str)
    def addTickerToList(self):
        row = self.tableWidget_stockList_add.currentRow()
        ticker = self.tableWidget_stockList_add.item(row, 0).text()

        self.submitClicked.emit(ticker)
        self.close()        
        

            
if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    DialogWindow_add = QtWidgets.QDialog()
    ui = Ui_DialogWindow_add()
    ui.setupUi(DialogWindow_add)
    DialogWindow_add.show()
    sys.exit(app.exec_())
