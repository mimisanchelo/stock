import sys
from PyQt5.uic import loadUi
from PyQt5 import QtWidgets, QtGui
from PyQt5.QtWidgets import QMainWindow, QWidget, QLabel, QComboBox, QLineEdit, QApplication, QStackedWidget, QPushButton, QTableWidget, QMessageBox
from PyQt5.QtGui import QFont as qfont, QValidator, QIntValidator, QDoubleValidator
from PyQt5.QtCore import Qt
import pip._vendor.requests as request
from dialogWindow import Ui_DialogWindow_add

from database import Database
from helper import headers
from dotenv import load_dotenv
load_dotenv()

#import icons
import resource_rc

class MainWindow(QMainWindow):
    
    data = Database()
    currentUser = (4, 'admin@mail.ru', '123456')

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
        self.user_btn = self.findChild(QPushButton, 'user_btn')
        self.watchlist_btn = self.findChild(QPushButton, 'watchlist_btn')
        self.calculator_btn = self.findChild(QPushButton, 'calculator_btn')
        self.stackedWidget = self.findChild(QStackedWidget, 'stackedWidget')
        self.login_btn_welcome = self.findChild(QPushButton, 'pushButton_login')
        self.signup_btn_welcome = self.findChild(QPushButton, 'pushButton_signup')
        self.signup_btn_login = self.findChild(QPushButton, 'pushButton_signup_3')
        self.signup_btn_signup = self.findChild(QPushButton, 'pushButton_signup_signup')
        self.login_btn_login = self.findChild(QPushButton, 'pushButton_login_3')
        self.login_btn_signup = self.findChild(QPushButton, 'pushButton_login_signupPage')
        self.errorLabel_signup = self.findChild(QLabel, 'label_Error_signup')
        self.errorLabel_login = self.findChild(QLabel, 'label_Error_login')
        self.inputEmail_login = self.findChild(QLineEdit, 'lineEdit_login_login')
        self.inputPassword_login = self.findChild(QLineEdit, 'lineEdit_password_login')
        self.inputEmail_signup = self.findChild(QLineEdit, 'lineEdit_email_signup')
        self.inputPassword_signup1 = self.findChild(QLineEdit, 'lineEdit_password_signup1')
        self.inputPassword_signup2 = self.findChild(QLineEdit, 'lineEdit_password_signup2')

        self.comboBox_tickers = self.findChild(QComboBox, 'comboBox_tickers')
        self.table_targetPrice = self.findChild(QTableWidget, 'tableWidget_targetPrice')
        self.lineEdit_curentPrice = self.findChild(QLineEdit, 'lineEdit_curentPrice')
        self.lineEdit_totalShares = self.findChild(QLineEdit, 'lineEdit_totalShares')
        self.label_RiskedinTrade = self.findChild(QLabel, 'label_RiskedinTrade')
        self.lineEdit_precentRisked = self.findChild(QLineEdit, 'lineEdit_precentRisked')
        self.lineEdit_precentGained = self.findChild(QLineEdit, 'lineEdit_precentGained')
        self.pushButton_addtoTrack = self.findChild(QPushButton, 'pushButton_addtoTrack')
        self.table_trackingTickers = self.findChild(QTableWidget, 'table_trackingTickers')
        self.deleteToTrack_btn = self.findChild(QPushButton, 'pushButton_delTickerTrack')

        #pages
        self.watchlist_page = self.findChild(QWidget, 'watchlitMenu_page') 
        self.welcome_page = self.findChild(QWidget, 'welcome_page') 
        self.login_page = self.findChild(QWidget, 'login_page') 
        self.signup_page = self.findChild(QWidget, 'signup_page') 
        self.calculator_page = self.findChild(QWidget, 'entry_exit_page') 
        
        #------------ CONNECT BTNs
        # watchlist menu
        self.addTicker_main.clicked.connect(self.openAddTicker)
        self.deleteTicker_main.clicked.connect(self.deleteTicker)
        self.clearList_main.clicked.connect(self.clearWatchList)
        # on click show data of ticker
        self.table_watchlist.selectionModel().selectionChanged.connect(self.fetchTickerInformation)
        self.comboBox_tickers.activated.connect(self.calculator_loadTickerInfo)
        

        self.lineEdit_totalShares.textChanged[str].connect(self.calculator_riskedTrade)
        self.lineEdit_precentRisked.textChanged[str].connect(self.calculator_precentRisked)
        self.lineEdit_precentGained.textChanged[str].connect(self.calculator_precentGained)
        self.pushButton_addtoTrack.clicked.connect(self.addtoTrack)
        self.deleteToTrack_btn.clicked.connect(self.deletetoTrack)

        
        # CONNECT PAGES
        self.user_btn.clicked.connect(self.on_user_btn)
        self.watchlist_btn.clicked.connect(self.on_watchlist)
        self.calculator_btn.clicked.connect(self.on_calculator)
        # --------------------------
        self.login_btn_welcome.clicked.connect(self.on_login_btn)
        self.signup_btn_welcome.clicked.connect(self.on_signup_btn)
        self.login_btn_signup.clicked.connect(self.on_login_btn)
        self.signup_btn_signup.clicked.connect(self.signupFunction)
        self.signup_btn_login.clicked.connect(self.on_signup_btn)
        self.login_btn_login.clicked.connect(self.loginFunction)
        
        
        # set font_size
        self.fetch_watchlist()
        font = qfont()
        font.setPointSize(9)
        self.table_watchlist.setFont(font)
        # turn off edit triggers
        self.table_watchlist.setEditTriggers(QTableWidget.NoEditTriggers)
        self.tableWidget_sum_1.setEditTriggers(QTableWidget.NoEditTriggers)
        self.tableWidget_sum_2.setEditTriggers(QTableWidget.NoEditTriggers)
        self.tableWidget_sum_3.setEditTriggers(QTableWidget.NoEditTriggers)

        # passwordMODE
        self.inputPassword_signup1.setEchoMode(QtWidgets.QLineEdit.Password)
        self.inputPassword_signup2.setEchoMode(QtWidgets.QLineEdit.Password)
        self.inputPassword_login.setEchoMode(QtWidgets.QLineEdit.Password)
        
        
        #show the app
        self.show()

    # SWITCH PAGES
    def on_user_btn(self):
        self.stackedWidget.setCurrentWidget(self.welcome_page)
    def on_login_btn(self):
        self.stackedWidget.setCurrentWidget(self.login_page)
    def on_signup_btn(self):
        self.stackedWidget.setCurrentWidget(self.signup_page)
    def on_watchlist(self):
        self.stackedWidget.setCurrentWidget(self.watchlist_page)
        self.fetch_watchlist()
    def on_calculator(self):
        self.stackedWidget.setCurrentWidget(self.calculator_page)
        self.calculator_loadDataUser()

    # DELETE FROM TO TRACK LIST
    def deletetoTrack(self):
        itemRow = self.table_trackingTickers.currentRow()
        ticker = self.table_trackingTickers.item(itemRow, 0).text()
        # delete from db
        self.data.delete_position_to_track(ticker)
        # delete from the table
        SelectedRow = self.table_trackingTickers.currentRow()
        self.table_trackingTickers.removeRow(SelectedRow)    

    # ADD TO TRACK LIST
    def addtoTrack(self):  
        rowPosition = self.table_trackingTickers.rowCount()
        self.table_trackingTickers.insertRow(rowPosition)
        try:
            takeProfit = self.table_targetPrice.item(2,0).text().replace('$', '')
            stopLoss = self.table_targetPrice.item(5,0).text().replace('$', '')
            totalShares = self.lineEdit_totalShares.text()
            entryPrice = self.lineEdit_curentPrice.text()   
            symbol = self.comboBox_tickers.currentText()

            url = "https://twelve-data1.p.rapidapi.com/price"
            querystring = {"symbol":'AAPL',"format":"json","outputsize":"30"}
            response_price = request.get(url, headers=headers, params=querystring).json()

            self.table_trackingTickers.setItem(rowPosition, 0, QtWidgets.QTableWidgetItem(symbol))
            self.table_trackingTickers.setItem(rowPosition, 6, QtWidgets.QTableWidgetItem(takeProfit))
            self.table_trackingTickers.setItem(rowPosition, 7, QtWidgets.QTableWidgetItem(stopLoss))
            self.table_trackingTickers.setItem(rowPosition, 2, QtWidgets.QTableWidgetItem(totalShares))
            self.table_trackingTickers.setItem(rowPosition, 1, QtWidgets.QTableWidgetItem(entryPrice))
            self.table_trackingTickers.setItem(rowPosition, 3, QtWidgets.QTableWidgetItem(f"{float(response_price['price']):.2f}"))
            
            earned = float(response_price['price']) - float(entryPrice)
            self.table_trackingTickers.setItem(rowPosition, 4, QtWidgets.QTableWidgetItem(f'{earned:.2f}'))
            if earned > 0:
                self.table_trackingTickers.item(rowPosition, 4).setForeground(QtGui.QColor(0,255,0))
            else: 
                self.table_trackingTickers.item(rowPosition, 4).setForeground(QtGui.QColor(255,0,0))

            self.data.add_position_to_track(self.currentUser[0], symbol, entryPrice, totalShares, takeProfit, stopLoss)
        except AttributeError:
            QMessageBox.warning(self, 'Warning', 'Please fill all the fields to track the trade')
              

    # FETCH USER`S DATA ON LOAD CALCULATOR PAGE
    def calculator_loadDataUser(self):
        if self.currentUser == None:
            QMessageBox.information(self, "Need to Login", "Please Login to your account to plan your futher trades")
        else:
            #clear
            self.comboBox_tickers.clear()
            self.table_trackingTickers.setRowCount(0)

            #add rows to table
            rowPosition = self.table_trackingTickers.rowCount()
            self.table_trackingTickers.insertRow(rowPosition)

            #loop data
            for ticker in self.data.show_watchList(self.currentUser[0]):
                self.comboBox_tickers.addItem(ticker[1])

            url = "https://twelve-data1.p.rapidapi.com/price"
            querystring = {"symbol":'AAPL',"format":"json","outputsize":"30"}
            response_price = request.get(url, headers=headers, params=querystring).json()

            userTracker = self.data.fetch_user_tracks(self.currentUser[0])[0]
            #display data on the table
            print(userTracker)
            self.table_trackingTickers.setItem(rowPosition, 6, QtWidgets.QTableWidgetItem(f'{userTracker[5]}'))
            self.table_trackingTickers.setItem(rowPosition, 7, QtWidgets.QTableWidgetItem(f'{userTracker[6]}'))
            self.table_trackingTickers.setItem(rowPosition, 2, QtWidgets.QTableWidgetItem(f'{userTracker[4]}'))
            self.table_trackingTickers.setItem(rowPosition, 1, QtWidgets.QTableWidgetItem(f'{userTracker[3]}'))
            self.table_trackingTickers.setItem(rowPosition, 0, QtWidgets.QTableWidgetItem(f'{userTracker[2]}'))
            self.table_trackingTickers.setItem(rowPosition, 3, QtWidgets.QTableWidgetItem(f"{float(response_price['price']):.2f}"))

            earned = float(response_price['price']) - float(userTracker[3])
            self.table_trackingTickers.setItem(rowPosition, 4, QtWidgets.QTableWidgetItem(f"{earned:.2f}"))
            if earned > 0:
                self.table_trackingTickers.item(rowPosition, 4).setForeground(QtGui.QColor(0,255,0))
            else: 
                self.table_trackingTickers.item(rowPosition, 4).setForeground(QtGui.QColor(255,0,0))

            

    def calculator_loadTickerInfo(self):
        # if self.comboBox_tickers.currentText() == 'None':
        #     QMessageBox.information(self, "Empty Ticker", "Please pick a ticker from the list")
        # else:
        url = "https://twelve-data1.p.rapidapi.com/price"
        querystring = {"symbol":'AAPL',"format":"json","outputsize":"30"}
        response_price = request.get(url, headers=headers, params=querystring).json()
        self.lineEdit_curentPrice.setText(f"{float(response_price['price']):.2f}")

    # SET TOTAL $ CALC RISKED IN TRADE
    def calculator_riskedTrade(self):
        # check if current price is set
        if self.lineEdit_curentPrice.text() == '':
            QMessageBox.information(self, "Ticker", "Please choose a ticker from the list")
            return
        
        #validate share values
        validator = QIntValidator(0, 999999999)
        self.lineEdit_totalShares.setValidator(validator)

        try:
            labelRisked = float(self.lineEdit_curentPrice.text()) * int(self.lineEdit_totalShares.text())
        except ValueError:
            if self.lineEdit_totalShares.text() == '':
                return
            QMessageBox.information(self, "Wrong Input", "Please entry a valid number")
            return
        
        self.label_RiskedinTrade.setText(str(f'{labelRisked:.2f}'))
       
    # SET % RISKED IN TRADE
    def calculator_precentRisked(self):
        # check if current price is set
        # if self.lineEdit_curentPrice.text() == '' and self.label_RiskedinTrade.text() == '':
        #     QMessageBox.information(self, "Ticker", "Please choose a ticker from the list")
        #     return
        
        #validate %Risked value
        validator = QDoubleValidator(0, 9999, 2)
        self.lineEdit_precentRisked.setValidator(validator)

        try:
            #set max loss
            maxLoss = float(self.lineEdit_precentRisked.text()) * float(self.label_RiskedinTrade.text()) / 100
            self.table_targetPrice.setItem(6, 0, QtWidgets.QTableWidgetItem(f'$ {maxLoss:.2f}'))

            #set stop loss
            priceForShare = float(self.lineEdit_precentRisked.text()) * float(self.lineEdit_curentPrice.text()) / 100
            stopLoss = float(self.lineEdit_curentPrice.text()) - priceForShare
            self.table_targetPrice.setItem(5, 0, QtWidgets.QTableWidgetItem(f'$ {stopLoss:.2f}'))

        except ValueError:
            if self.lineEdit_precentRisked.text() == '':
                self.table_targetPrice.setItem(5, 0, QtWidgets.QTableWidgetItem(''))
                self.table_targetPrice.setItem(6, 0, QtWidgets.QTableWidgetItem(''))

            


    def calculator_precentGained(self):
        # check if current price is set
        if self.lineEdit_curentPrice.text() == '' and self.label_RiskedinTrade.text() == '':
            QMessageBox.information(self, "Ticker", "Please choose a ticker from the list")
            return
        
        #validate %Risked value
        validator = QDoubleValidator(0, 9999, 2)
        self.lineEdit_precentGained.setValidator(validator)

        try:
            self.calculator_riskedTrade()

            #set max gained price
            maxGained = float(self.lineEdit_precentGained.text()) * float(self.label_RiskedinTrade.text()) / 100
            self.table_targetPrice.setItem(3, 0, QtWidgets.QTableWidgetItem(f'$ {maxGained:.2f}'))

            #set leaving trade
            priceForShare = float(self.lineEdit_precentGained.text()) * float(self.lineEdit_curentPrice.text()) / 100
            stopGain = float(self.lineEdit_curentPrice.text()) + priceForShare
            self.table_targetPrice.setItem(2, 0, QtWidgets.QTableWidgetItem(f'$ {stopGain:.2f}'))

            #rise to
            priceRise = priceForShare * float(self.lineEdit_totalShares.text())
            self.table_targetPrice.setItem(0, 0, QtWidgets.QTableWidgetItem(f'$ {priceRise:.2f}'))
            
        except ValueError:
            if self.lineEdit_precentRisked.text() == '':
                self.table_targetPrice.setItem(2, 0, QtWidgets.QTableWidgetItem(''))
                self.table_targetPrice.setItem(3, 0, QtWidgets.QTableWidgetItem(''))


    # LOGIN SYSTEM2
    def loginFunction(self):
        user = self.inputEmail_login.text()
        password = self.inputPassword_login.text()

        if len(user) == 0 or len(password) == 0:
            self.errorLabel_login.setText('Please fill in all fields')
        else:
            profile = self.data.get_user_profile(user)
            if password == profile[2]:
                self.errorLabel_login.setText('')
                self.stackedWidget.setCurrentIndex(0)
                print("Successfully logged in.")
                self.currentUser = profile
                self.fetch_watchlist()
            else:
                self.inputEmail_login.setText('')
                self.inputPassword_login.setText('')
                
                self.errorLabel_login.setText("Invalid username or password")

    # SIGNUP SYSTEM
    def signupFunction(self):
        user = self.inputEmail_signup.text()
        password = self.inputPassword_signup1.text()
        password2 = self.inputPassword_signup2.text()

        if len(user) == 0 or len(password) == 0:
            self.errorLabel_signup.setText('Please fill in all fields')
        elif password != password2:
            self.errorLabel_signup.setText('Passwords do not match')
        else:
            if self.data.check_email(user) != None:
                self.errorLabel_signup.setText("Current email is already taken")
                self.inputEmail_signup.text('')
                self.inputPassword_signup1.text('')
                self.inputPassword_signup2.text('')
            else:
                #add data
                self.data.insert_user_profile(user,password)
                #move on
                self.stackedWidget.setCurrentIndex(2)
                QMessageBox.information(self, 'Success', 'You have successfully signed up') 
                
    #on start
    def fetch_watchlist(self):
        if self.currentUser == None:
             return 
        else:
            #clear tab
            self.table_watchlist.setRowCount(0)
            #load data of spec user
            for ticker in self.data.show_watchList(self.currentUser[0]):
                rowPosition = self.table_watchlist.rowCount()
                self.table_watchlist.insertRow(rowPosition)
                # fetch fresh data
                # url = "https://twelve-data1.p.rapidapi.com/quote"
                # querystring = {"symbol":ticker[1],"interval":"1day","outputsize":"30","format":"json"}
                # response_ticker = request.get(url, headers=headers, params=querystring).json()

                # # fetch actual price data
                # url_price = "https://twelve-data1.p.rapidapi.com/price"

                # query = {"symbol":ticker[1],"format":"json","outputsize":"30"}
                # response_price = request.get(url_price, headers=headers, params=query).json()
                # display data
                # self.table_watchlist.setItem(rowPosition, 0, QtWidgets.QTableWidgetItem(ticker[1]))
                # self.table_watchlist.setItem(rowPosition, 1, QtWidgets.QTableWidgetItem(ticker[2]))
                # self.table_watchlist.setItem(rowPosition, 2, QtWidgets.QTableWidgetItem(f"{float(response_price['price']):.2f}"))
                # self.table_watchlist.setItem(rowPosition, 3, QtWidgets.QTableWidgetItem(f"{float(response_ticker['change']):.2f}"))
                # self.table_watchlist.setItem(rowPosition, 4, QtWidgets.QTableWidgetItem(f"{float(response_ticker['percent_change']):.2f}"))
                # self.table_watchlist.setItem(rowPosition, 5, QtWidgets.QTableWidgetItem(f"{response_ticker['volume']}"))

                # if float(response_ticker['change']) > 0 and float(response_ticker['percent_change']) > 0:
                #     self.table_watchlist.item(rowPosition, 3).setForeground(QtGui.QColor(0,255,0))
                #     self.table_watchlist.item(rowPosition, 4).setForeground(QtGui.QColor(0,255,0))
                
                # else:
                #     self.table_watchlist.item(rowPosition, 3).setForeground(QtGui.QColor(255,0,0))
                #     self.table_watchlist.item(rowPosition, 4).setForeground(QtGui.QColor(255,0,0))

            

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
            self.tableWidget_sum_3.setColumnCount(0)
            self.tableWidget_sum_3.setHorizontalHeaderItem(0, QtWidgets.QTableWidgetItem('TICKER PROFILE'))
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
            pass

        if float(response_quote['change']) > 0 and float(response_quote['percent_change']) > 0:
                self.table_watchlist.item(rowPosition, 3).setForeground(QtGui.QColor(0,255,0))
                self.table_watchlist.item(rowPosition, 4).setForeground(QtGui.QColor(0,255,0))
        else:
            self.table_watchlist.item(rowPosition, 3).setForeground(QtGui.QColor(255,0,0))
            self.table_watchlist.item(rowPosition, 4).setForeground(QtGui.QColor(255,0,0))


       



 
app = QApplication(sys.argv)
window = MainWindow()
app.exec_()













