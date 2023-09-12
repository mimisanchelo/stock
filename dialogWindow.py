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
        DialogWindow_add.resize(475, 600)
        self.pushButton_dialog_add = QtWidgets.QPushButton(DialogWindow_add, clicked=lambda: self.addTickerToList())
        self.pushButton_dialog_add.setGeometry(QtCore.QRect(170, 550, 151, 31))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.pushButton_dialog_add.setFont(font)
        self.pushButton_dialog_add.setObjectName("pushButton_dialog_add")
        self.label_dialog_add = QtWidgets.QLabel(DialogWindow_add)
        self.label_dialog_add.setGeometry(QtCore.QRect(-10, 10, 491, 41))
        font = QtGui.QFont()
        font.setPointSize(16)
        self.label_dialog_add.setFont(font)
        self.label_dialog_add.setAlignment(QtCore.Qt.AlignCenter)
        self.label_dialog_add.setObjectName("label_dialog_add")
        self.lineTicker_add = QtWidgets.QLineEdit(DialogWindow_add)
        self.lineTicker_add.setGeometry(QtCore.QRect(20, 60, 321, 31))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.lineTicker_add.setFont(font)
        self.lineTicker_add.setText("")
        self.lineTicker_add.setObjectName("lineTicker_add")
        self.tableWidget_stockList_add = QtWidgets.QTableWidget(DialogWindow_add)
        self.tableWidget_stockList_add.setGeometry(QtCore.QRect(20, 110, 438, 431))
        self.tableWidget_stockList_add.setObjectName("tableWidget_stockList_add")
        self.tableWidget_stockList_add.setColumnCount(5)
        self.tableWidget_stockList_add.setRowCount(0)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_stockList_add.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_stockList_add.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_stockList_add.setHorizontalHeaderItem(2, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_stockList_add.setHorizontalHeaderItem(3, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_stockList_add.setHorizontalHeaderItem(4, item)
        self.tableWidget_stockList_add.horizontalHeader().setDefaultSectionSize(109)
        self.pushButton_dialog_find = QtWidgets.QPushButton(DialogWindow_add, clicked=lambda: self.searchSymbol())
        self.pushButton_dialog_find.setGeometry(QtCore.QRect(360, 60, 91, 31))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.pushButton_dialog_find.setFont(font)
        self.pushButton_dialog_find.setObjectName("pushButton_dialog_add_2")

        self.retranslateUi(DialogWindow_add)
        QtCore.QMetaObject.connectSlotsByName(DialogWindow_add)
        self.loadStockList()

    def retranslateUi(self, DialogWindow_add):
        _translate = QtCore.QCoreApplication.translate
        DialogWindow_add.setWindowTitle(_translate("DialogWindow_add", "Dialog"))
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
        item = self.tableWidget_stockList_add.horizontalHeaderItem(4)
        item.setText(_translate("DialogWindow_add", "Currency"))
        self.pushButton_dialog_find.setText(_translate("DialogWindow_add", "Find Ticker"))

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
            self.tableWidget_stockList_add.setItem(row, 4, QtWidgets.QTableWidgetItem(f"{ticker['currency']}"))
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
                self.tableWidget_stockList_add.setItem(row, 4, QtWidgets.QTableWidgetItem(f"{ticker['currency']}"))
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
