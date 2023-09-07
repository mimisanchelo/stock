import sys
from PyQt5.uic import loadUi
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QMainWindow, QDialog, QApplication, QPushButton, QTableView, QTableWidget, QMessageBox
from PyQt5.QtGui import QFont as qfont
import pip._vendor.requests as request
from dialogWindow import Ui_DialogWindow_add

from database import Database
from helper import headers
import os
from dotenv import load_dotenv
load_dotenv()

#import icons
import resource_rc



class MainWindow(QMainWindow):
    data = Database()

    def __init__(self):
        super(MainWindow, self).__init__()
        
        #load UI file
        loadUi('mainWindow.ui', self)

        # FIND WIDGETS MAIN WINDOW
        self.addTicker_main = self.findChild(QPushButton, 'pushButton_addTicker_main')
        self.deleteTicker_main = self.findChild(QPushButton, 'pushButton_deleteTicker_main')
        self.clearList_main = self.findChild(QPushButton, 'pushButton_clearList_main')
        self.table_watchlist = self.findChild(QTableWidget, 'table_watchlist')
        self.tableWidget_sum_1 = self.findChild(QTableWidget, 'tableWidget_summary_1')
        self.tableWidget_sum_2 = self.findChild(QTableWidget, 'tableWidget_summary_2')
        self.tableWidget_sum_3 = self.findChild(QTableWidget, 'tableWidget_summary_3')
        self.pushButton_sum_main = self.findChild(QPushButton, 'pushButton_summary_main')

        #connect btns
        self.addTicker_main.clicked.connect(self.openAddTicker)
        self.deleteTicker_main.clicked.connect(self.deleteTicker)
        self.clearList_main.clicked.connect(self.clearWatchList)
        self.pushButton_sum_main.clicked.connect(self.fetchTickerInformation)

        self.fetch_watchlist()
        font = qfont()
        font.setPointSize(9)
        self.table_watchlist.setFont(font)
        
        
        #show the app
        self.show()
        
    #on start
    def fetch_watchlist(self):
        for ticker in self.data.show_watchList():
            rowPosition = self.table_watchlist.rowCount()
            self.table_watchlist.insertRow(rowPosition)
            # fetch fresh data
            url = "https://twelve-data1.p.rapidapi.com/quote"
            querystring = {"symbol":ticker[1],"interval":"1day","outputsize":"30","format":"json"}
            response_ticker = request.get(url, headers=headers, params=querystring).json()

            # fetch actual price data
            url_price = "https://twelve-data1.p.rapidapi.com/price"

            query = {"symbol":ticker[1],"format":"json","outputsize":"30"}
            response_price = request.get(url_price, headers=headers, params=query).json()
            print(response_price)
            # display data
            self.table_watchlist.setItem(rowPosition, 0, QtWidgets.QTableWidgetItem(ticker[1]))
            self.table_watchlist.setItem(rowPosition, 1, QtWidgets.QTableWidgetItem(ticker[2]))
            self.table_watchlist.setItem(rowPosition, 2, QtWidgets.QTableWidgetItem(f"{float(response_price['price']):.2f}"))
            self.table_watchlist.setItem(rowPosition, 3, QtWidgets.QTableWidgetItem(f"{float(response_ticker['change']):.2f}"))
            self.table_watchlist.setItem(rowPosition, 4, QtWidgets.QTableWidgetItem(f"{float(response_ticker['percent_change']):.2f}"))
            self.table_watchlist.setItem(rowPosition, 5, QtWidgets.QTableWidgetItem(f"{response_ticker['volume']}"))
            

    # FETCH TICKER INFORMATION
    def fetchTickerInformation(self):
        #get ticker
        itemRow = self.table_watchlist.currentRow()
        ticker = self.table_watchlist.item(itemRow, 0).text()

        #fetch data
        url = "https://twelve-data1.p.rapidapi.com/quote"
        querystring = {"symbol":ticker,"interval":"1day","outputsize":"30","format":"json"}
        response = request.get(url, headers=headers, params=querystring).json()

        #fetch profile
        url_profile = "https://twelve-data1.p.rapidapi.com/profile"
        querystring = {"symbol":ticker}
        response_profile = request.get(url_profile, headers=headers, params=querystring).json()

        try:
            # SUMMARY_1
            self.tableWidget_sum_1.setItem(0, 0, QtWidgets.QTableWidgetItem(f"{float(response['open']):.2f}"))
            self.tableWidget_sum_1.setItem(0, 1, QtWidgets.QTableWidgetItem(f"{float(response['high']):.2f}"))
            self.tableWidget_sum_1.setItem(0, 2, QtWidgets.QTableWidgetItem(f"{float(response['low']):.2f}"))
            self.tableWidget_sum_1.setItem(0, 3, QtWidgets.QTableWidgetItem(f"{float(response['close']):.2f}"))
            self.tableWidget_sum_1.setItem(0, 4, QtWidgets.QTableWidgetItem(f"{float(response['previous_close']):.2f}"))
            self.tableWidget_sum_1.setItem(0, 5, QtWidgets.QTableWidgetItem(f"{response['volume']}"))
            self.tableWidget_sum_1.setItem(0, 6, QtWidgets.QTableWidgetItem(f"{response['average_volume']}"))

            #SUMMARY_2
            self.tableWidget_sum_2.setItem(0, 0, QtWidgets.QTableWidgetItem(f"{float(response['fifty_two_week']['high']):.2f}"))
            self.tableWidget_sum_2.setItem(0, 1, QtWidgets.QTableWidgetItem(f"{float(response['fifty_two_week']['low']):.2f}"))
            self.tableWidget_sum_2.setItem(0, 2, QtWidgets.QTableWidgetItem(f"{response['fifty_two_week']['range']}"))         

            #SUMMARY_3
            self.tableWidget_sum_3.setHorizontalHeaderItem(0, QtWidgets.QTableWidgetItem(f'{ticker} PROFILE'))
            self.tableWidget_sum_3.setItem(0, 0, QtWidgets.QTableWidgetItem(f"{response_profile['name']}"))
            self.tableWidget_sum_3.setItem(0, 1, QtWidgets.QTableWidgetItem(f"{response_profile['exchange']}"))
            self.tableWidget_sum_3.setItem(0, 2, QtWidgets.QTableWidgetItem(f"{response_profile['sector']}"))
            self.tableWidget_sum_3.setItem(0, 3, QtWidgets.QTableWidgetItem(f"{response_profile['industry']}"))
            self.tableWidget_sum_3.setItem(0, 4, QtWidgets.QTableWidgetItem(f"{response_profile['employees']}"))
            self.tableWidget_sum_3.setItem(0, 5, QtWidgets.QTableWidgetItem(f"{response_profile['type']}"))
            self.tableWidget_sum_3.setItem(0, 6, QtWidgets.QTableWidgetItem(f"{response_profile['website']}"))

        except KeyError:
            QMessageBox.information(self, "Ticker information", f"Ticker: {ticker} not Found.\nPlease check your spelling and try again.")

    # CLEAR WATCHLIST
    def clearWatchList(self):
        self.data.clear_watchList()
        self.table_watchlist.setRowCount(0)

    # DELETE TICKER FROM WATCHLIST
    def deleteTicker(self):
        # choose ticker
        itemRow = self.table_watchlist.currentRow()
        ticker = self.table_watchlist.item(itemRow, 0).text()
        # delete from db
        self.data.delete_ticker(ticker)
        # delete from the table
        SelectedRow = self.table_watchlist.currentRow()
        self.table_watchlist.removeRow(SelectedRow)       
    
    # ADD TICKER TO WATCHLIST FROM DIALOG WINDOW
    def openAddTicker(self):
        self.dialogAdd = QtWidgets.QDialog()
        self.ui = Ui_DialogWindow_add()
        self.ui.setupUi(self.dialogAdd)
        self.ui.submitClicked.connect(self.displayAddedTicker)
        self.dialogAdd.show()

    # DISPLAY ADDED TICKER
    def displayAddedTicker(self, ticker):
        # QUOTE
        url_quote = "https://twelve-data1.p.rapidapi.com/quote"
        querystring = {"symbol":ticker,"interval":"1day","outputsize":"30","format":"json"}
        response_quote = request.get(url_quote, headers=headers, params=querystring).json()

        # #REAL-TIME PRICE
        url_price = "https://twelve-data1.p.rapidapi.com/price"
        query = {"symbol":ticker,"format":"json","outputsize":"30"}
        response_price = request.get(url_price, headers=headers, params=query).json()

        # ADD DATA TO DB
        self.data.add_ticker(ticker, response_quote['name'], response_quote['exchange'])

        # display data
        rowPosition = self.table_watchlist.rowCount()
        
        self.table_watchlist.insertRow(rowPosition)
        try:
            self.table_watchlist.setItem(rowPosition, 0, QtWidgets.QTableWidgetItem(ticker))
            self.table_watchlist.setItem(rowPosition, 1, QtWidgets.QTableWidgetItem(f"{response_quote['name']}"))
            self.table_watchlist.setItem(rowPosition, 2, QtWidgets.QTableWidgetItem(f"{float(response_price['price']):.2f}"))
            self.table_watchlist.setItem(rowPosition, 3, QtWidgets.QTableWidgetItem(f"{float(response_quote['change']):.2f}"))
            self.table_watchlist.setItem(rowPosition, 4, QtWidgets.QTableWidgetItem(f"{float(response_quote['percent_change']):.2f}"))
            self.table_watchlist.setItem(rowPosition, 5, QtWidgets.QTableWidgetItem(f"{response_quote['volume']}"))
        except KeyError:
            print('das')
            # self.table_watchlist.setItem(rowPosition, 2, QtWidgets.QTableWidgetItem("No Data Found"))

       



 
app = QApplication(sys.argv)
window = MainWindow()
app.exec_()













