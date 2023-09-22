import sys
from PyQt5.uic import loadUi
from PyQt5 import QtWidgets, QtGui
from PyQt5.QtWidgets import QMainWindow, QWidget,QTextEdit, QListWidget,  QLabel, QComboBox, QLineEdit, QApplication, QStackedWidget, QPushButton, QTableWidget, QMessageBox
from PyQt5.QtGui import QFont as qfont, QIntValidator, QDoubleValidator
from PyQt5.QtCore import Qt
from dialogWindow import Ui_DialogWindow_add

import threading
import time
import bcrypt

#websocket
# from twelvedata import TDClient

#import icons
import resource_rc

from database import Database
from helper import send_alert, get_quote_symbol, get_price_symbol, get_profile_symbol
from dotenv import load_dotenv
load_dotenv()     
        


class MainWindow(QMainWindow):
    
    data = Database()
    currentUser = None

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
        self.news_btn = self.findChild(QPushButton, 'news_btn')
        self.alert_btn = self.findChild(QPushButton, 'alert_btn')
        self.market_btn = self.findChild(QPushButton, 'market_btn')
        self.label_page = self.findChild(QLabel, 'label_page')
        self.nav_userName = self.findChild(QLabel, 'label_nav_userName')
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
        self.inputName_login = self.findChild(QLineEdit, 'lineEdit_name_login')
        self.inputPassword_login = self.findChild(QLineEdit, 'lineEdit_password_login')
        self.inputEmail_signup = self.findChild(QLineEdit, 'lineEdit_email_signup')
        self.inputPassword_signup1 = self.findChild(QLineEdit, 'lineEdit_password_signup1')
        self.inputPassword_signup2 = self.findChild(QLineEdit, 'lineEdit_password_signup2')

        # calculator page
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

        # alert page
        self.alertSet_btn = self.findChild(QPushButton, 'pushButton_alertSet')
        self.textAlert = self.findChild(QTextEdit, 'textEdit_alertSummary')
        self.lineEdit_email = self.findChild(QLineEdit, 'lineEdit_alertEmail')
        self.lineEdit_value = self.findChild(QLineEdit, 'lineEdit_alertValue')
        self.lineEdit_ticker = self.findChild(QLineEdit, 'lineEdit_alertTicker')
        self.comboBox_symbol = self.findChild(QComboBox, 'comboBox_alertTickers')
        self.comboBox_upDown = self.findChild(QComboBox, 'comboBox_alertUpDown')
        self.comboBox_alertType = self.findChild(QComboBox, 'comboBox_alertType')

        #news page

        #pages
        self.watchlist_page = self.findChild(QWidget, 'watchlitMenu_page') 
        self.welcome_page = self.findChild(QWidget, 'welcome_page') 
        self.login_page = self.findChild(QWidget, 'login_page') 
        self.signup_page = self.findChild(QWidget, 'signup_page') 
        self.calculator_page = self.findChild(QWidget, 'entry_exit_page')
        self.alert_page = self.findChild(QWidget, 'alert_page')
        self.news_page = self.findChild(QWidget, 'news_page')
        self.market_page = self.findChild(QWidget, 'market_page')
        self.profile_page = self.findChild(QWidget, 'user_page')
        self.edit_page = self.findChild(QWidget, 'edit_user_page')

        #profile
        self.edit_profile_btn = self.findChild(QPushButton, 'pushButton_user_edit')
        self.delete_usersAlert_btn = self.findChild(QPushButton, 'pushButton_del_userAlerts')
        self.user_logout_btn = self.findChild(QPushButton, 'pushButton_user_logout')
        self.label_username = self.findChild(QLabel, 'label_userName')
        self.label_email = self.findChild(QLabel, 'label_userEmail')
        self.list_usersAlert = self.findChild(QListWidget, 'listWidget_userAlerts')
        
        #------------ CONNECT BTNs
        # watchlist menu
        self.addTicker_main.clicked.connect(self.openAddTicker)
        self.deleteTicker_main.clicked.connect(self.deleteTicker)
        self.clearList_main.clicked.connect(self.clearWatchList)
        # on click show data of ticker
        self.table_watchlist.selectionModel().selectionChanged.connect(self.fetchTickerInformation)
        self.comboBox_tickers.activated.connect(self.calculator_loadTickerInfo)
        self.comboBox_symbol.activated.connect(self.alert_chooseSymbol)
        

        self.lineEdit_totalShares.textChanged[str].connect(self.calculator_riskedTrade)
        self.lineEdit_precentRisked.textChanged[str].connect(self.calculator_precentRisked)
        self.lineEdit_precentGained.textChanged[str].connect(self.calculator_precentGained)
        self.pushButton_addtoTrack.clicked.connect(self.addtoTrack)
        self.deleteToTrack_btn.clicked.connect(self.deletetoTrack)

        
        # CONNECT PAGES
        self.user_btn.clicked.connect(self.on_user_btn)
        self.watchlist_btn.clicked.connect(self.on_watchlist)
        self.calculator_btn.clicked.connect(self.on_calculator)
        self.market_btn.clicked.connect(self.on_market)
        self.news_btn.clicked.connect(self.on_news)
        self.alert_btn.clicked.connect(self.on_alert)
        # --------------------------
        self.login_btn_welcome.clicked.connect(self.on_login_btn)
        self.signup_btn_welcome.clicked.connect(self.on_signup_btn)
        self.login_btn_signup.clicked.connect(self.on_login_btn)
        self.signup_btn_signup.clicked.connect(self.signupFunction)
        self.signup_btn_login.clicked.connect(self.on_signup_btn)
        self.login_btn_login.clicked.connect(self.loginFunction)
        # --------------------------------
        self.alertSet_btn.clicked.connect(self.alert_setAlert)
        # --------------------------------
        self.delete_usersAlert_btn.clicked.connect(lambda: self.del_userAlert())
        self.user_logout_btn.clicked.connect(self.logout)

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
        self.table_trackingTickers.setEditTriggers(QTableWidget.NoEditTriggers)
        self.table_targetPrice.setEditTriggers(QTableWidget.NoEditTriggers)

        # passwordMODE
        self.inputPassword_signup1.setEchoMode(QtWidgets.QLineEdit.Password)
        self.inputPassword_signup2.setEchoMode(QtWidgets.QLineEdit.Password)
        self.inputPassword_login.setEchoMode(QtWidgets.QLineEdit.Password)
        
        # check if price hit the set price
        threading.Timer(20.0, self.alert_conditions).start()

        # welcome page
        self.stackedWidget.setCurrentWidget(self.watchlist_page)
        
        if self.currentUser != None:
            self.nav_userName.setText(self.currentUser[3])

        #show the app
        self.show()

    # SWITCH PAGES
    def on_user_btn(self):
        if self.currentUser == None:
            self.stackedWidget.setCurrentWidget(self.welcome_page)
            self.label_page.setText('AUTHORIZATION')
            self.nav_userName.setText('')
        else:
            self.stackedWidget.setCurrentWidget(self.profile_page)
            self.label_page.setText('PROFILE')
            self.label_username.setText(self.currentUser[3])
            self.label_email.setText(self.currentUser[1])

            alerts = self.data.fetch_users_alerts(self.currentUser[0])
            if len(alerts) == 0:
                self.list_usersAlert.addItem('Set Alert on Ticker to be aware')
            else:
                self.list_usersAlert.clear()
                for alert in alerts:
                    self.list_usersAlert.addItem(f'Alert Set on: {alert[2]} when {alert[3]} is {alert[4]} {alert[5]}')

    def on_login_btn(self):
        self.stackedWidget.setCurrentWidget(self.login_page)
        self.label_page.setText('LOGIN')
    def on_signup_btn(self):
        self.stackedWidget.setCurrentWidget(self.signup_page)
        self.label_page.setText('SIGNUP')
    def on_watchlist(self):
        self.stackedWidget.setCurrentWidget(self.watchlist_page)
        self.fetch_watchlist()
        #self.updated()
        self.label_page.setText('WATCHLIST')
    def on_calculator(self):
        self.stackedWidget.setCurrentWidget(self.calculator_page)
        self.calculator_loadDataUser()
        self.label_page.setText('CALCULATOR')
    def on_alert(self):
        self.stackedWidget.setCurrentWidget(self.alert_page)
        self.alert_loadUserData()
        self.label_page.setText('ALERT')
    def on_news(self):
        self.stackedWidget.setCurrentWidget(self.news_page)
    def on_market(self):
        self.stackedWidget.setCurrentWidget(self.market_page)

    # WEBSOCKET CONNECTION **(WORKS BUT DUNNO HOW TO DISPLAY PROPERLY)
    # def updated(self):
    #     td = TDClient(apikey=os.getenv('WEBSOCKET_API_KEY'))
    #     ws = td.websocket(symbols="AAPL", on_event=self.on_event)
    #     ws.subscribe(['AAPL'])
    #     ws.connect()
    #     while True:
    #         ws.heartbeat()
    #         time.sleep(10) 

    # WEBSOCKET EVENT ***(DUNNO HOW TO IMPLEMENT THIS)
    # def on_event(self, e):
    #       rowPosition = self.table_watchlist.rowCount()
    #       print(e['price'])
    #       self.table_watchlist.item(rowPosition, 2).setText(f"{e['price']:.2f}")
    

    
    # DELETE PROFILE USER ALERT
    def del_userAlert(self):
        try:
            alert = self.list_usersAlert.currentRow()
            selected_row = self.list_usersAlert.currentItem().text()
            ticker = selected_row.split(' ')[3]
            self.list_usersAlert.takeItem(alert)
            self.data.delete_alert(self.currentUser[0], ticker)
        except AttributeError:
            QMessageBox.critical(self, 'Error', 'Please select an alert notification to delete')

    # display chosen ticker
    def alert_chooseSymbol(self):
        self.lineEdit_ticker.setText(self.comboBox_symbol.currentText())

    def alert_loadUserData(self):
        if self.currentUser != None:
            #clear
            self.comboBox_symbol.clear()
            #loop data
            for ticker in self.data.show_watchList(self.currentUser[0]):
                self.comboBox_symbol.addItem(ticker[1])

            self.lineEdit_email.setText(self.currentUser[1])
            self.textAlert.setPlainText('Notify me when stock [SYMBOL] [COMPANY NAME] Price is below [TARGET VALUE]')

    def alert_conditions(self):
        alerts = self.data.fetch_users_alerts(self.currentUser[0])
        
        while len(alerts) >= 0:
            for alert in alerts:
                if alert[3] == 'Price':
                    response = get_price_symbol(alert[2])
                    new_price = response['price']

                    if float(new_price) < alert[5] and alert[4] == 'Above':
                        pass

                    elif float(new_price) >= alert[5] and alert[4] == 'Above':
                        # send and then delete alert
                        self.send_emailAlert(alert[6], alert[2], alert[7])
                        self.data.delete_alert(alert[0], alert[2])

                    elif float(new_price) <= alert[5] and alert[4] == 'Below':
                        # send and then delete alert
                        self.send_emailAlert(alert[6], alert[2], alert[7])
                        self.data.delete_alert(alert[0], alert[2])

                    elif float(new_price) >= alert[5] and alert[4] == 'Below':
                        pass
                    

                elif alert[3] == 'Daily Price Change':
                    response = get_quote_symbol(alert[2])
                    price_change = response['change']

                    if abs(float(price_change)) < alert[5] and alert[4] == 'Above':
                        return
                    elif abs(float(price_change)) >= alert[5] and alert[4] == 'Above':
                        # send and then delete alert
                        self.send_emailAlert(alert[6], alert[2], alert[7])
                        self.data.delete_alert(alert[0], alert[2])

                    elif abs(float(price_change)) <= alert[5] and alert[4] == 'Below':
                        # send and then delete alert
                        self.send_emailAlert(alert[6], alert[2], alert[7])
                        self.data.delete_alert(alert[0], alert[2])
                    elif abs(float(price_change)) >= alert[5] and alert[4] == 'Below':
                        pass
                
                else:
                    response = get_quote_symbol(alert[2])
                    price_change = response['percent_change']

                    if abs(float(price_change)) < alert[5] and alert[4] == 'Above':
                        pass
                    elif abs(float(price_change)) >= alert[5] and alert[4] == 'Above':
                        # send and then delete alert
                        self.send_emailAlert(alert[6], alert[2], alert[7])
                        self.data.delete_alert(alert[0], alert[2])

                    elif abs(float(price_change)) <= alert[5] and alert[4] == 'Below':
                        # send and then delete alert
                        self.send_emailAlert(alert[6], alert[2], alert[7])
                        self.data.delete_alert(alert[0], alert[2])
                    elif abs(float(price_change)) >= alert[5] and alert[4] == 'Below':
                        pass
                    
                time.sleep(20)

    def alert_setAlert(self):
        try:
            reciever = self.lineEdit_email.text()
            symbol = self.lineEdit_ticker.text()
            message = self.textAlert.toPlainText()
            upOrDown = self.comboBox_upDown.currentText()
            value = self.lineEdit_value.text()
            type = self.comboBox_alertType.currentText()

            if symbol == '' or reciever == '' or message == '' or value == '':
                QMessageBox.information(self, "Empty fields", "Please fill out all the fields")
                return
            else:
                # add an alert to db
                self.data.add_alert(self.currentUser[0], symbol, type, upOrDown, value, reciever, message)
                QMessageBox.information(self, "Success", f"Alert on ticker {symbol} was added.\nNotification will be send when\n{type} is {upOrDown} {value} ")
                #clear inputs
                message.setText('')
                symbol.setText('')
                value.setText('')
        except AttributeError:
            QMessageBox.information(self, "Empty fields", "Please fill out all the fields")
            return
    
    def send_emailAlert(self, receiver, symbol, message):
        send_alert(receiver, symbol, message) 

    # DELETE FROM TO TRACK LIST
    def deletetoTrack(self):
        try:
            itemRow = self.table_trackingTickers.currentRow()
            ticker = self.table_trackingTickers.item(itemRow, 0).text()
            # delete from db
            self.data.delete_position_to_track(ticker)
            # delete from the table
            SelectedRow = self.table_trackingTickers.currentRow()
            self.table_trackingTickers.removeRow(SelectedRow)   
        except AttributeError:
            QMessageBox.information(self, "Error", "Please select a ticker to delete from the list")
            return

    # ADD TO TRACK LIST
    def addtoTrack(self):  
        try:
            # assign data to track
            takeProfit = self.table_targetPrice.item(2,0).text().replace('$', '')
            stopLoss = self.table_targetPrice.item(5,0).text().replace('$', '')
            totalShares = self.lineEdit_totalShares.text()
            entryPrice = self.lineEdit_curentPrice.text()   
            symbol = self.comboBox_tickers.currentText()

            #check if field is not empty
            if totalShares == '':
                QMessageBox.information(self, 'Warning', 'Please fill all the fields to track the trade')
                return

            # fetch ticker price
            symbol_price = get_price_symbol(symbol)

            # add row
            rowPosition = self.table_trackingTickers.rowCount()
            self.table_trackingTickers.insertRow(rowPosition)

            # display data
            self.table_trackingTickers.setItem(rowPosition, 0, QtWidgets.QTableWidgetItem(symbol))
            self.table_trackingTickers.setItem(rowPosition, 6, QtWidgets.QTableWidgetItem(takeProfit))
            self.table_trackingTickers.setItem(rowPosition, 7, QtWidgets.QTableWidgetItem(stopLoss))
            self.table_trackingTickers.setItem(rowPosition, 2, QtWidgets.QTableWidgetItem(totalShares))
            self.table_trackingTickers.setItem(rowPosition, 1, QtWidgets.QTableWidgetItem(entryPrice))
            self.table_trackingTickers.setItem(rowPosition, 3, QtWidgets.QTableWidgetItem(f"{float(symbol_price['price']):.2f}"))
            
            earned = float(symbol_price['price']) - float(entryPrice)
            self.table_trackingTickers.setItem(rowPosition, 4, QtWidgets.QTableWidgetItem(f'{earned:.2f}'))
            if earned > 0:
                self.table_trackingTickers.item(rowPosition, 4).setForeground(QtGui.QColor(0,255,0))
            else: 
                self.table_trackingTickers.item(rowPosition, 4).setForeground(QtGui.QColor(255,0,0))

            self.data.add_position_to_track(self.currentUser[0], symbol, entryPrice, totalShares, takeProfit, stopLoss)
        except AttributeError:
            QMessageBox.information(self, 'Warning', 'Please fill all the fields to track the trade')
            return
              

    # FETCH USER`S DATA ON LOAD CALCULATOR PAGE
    def calculator_loadDataUser(self):
        if self.currentUser == None:
            QMessageBox.information(self, "Need to Login", "Please Login to your account to plan your futher trades")
        else:   
            #clear
            self.comboBox_tickers.clear()
        
            #loop data
            for ticker in self.data.show_watchList(self.currentUser[0]):
                self.comboBox_tickers.addItem(ticker[1])

            # fetch ticker price
            symbol_price = get_price_symbol(ticker[1])

            userTracker = self.data.fetch_user_tracks(self.currentUser[0])

            if userTracker == None:
                self.table_trackingTickers.setRowCount(0)
                QMessageBox.information(self, 'No User`s Track', 'Please Login to Track')
            
            #add rows to table
            rowPosition = self.table_trackingTickers.rowCount()
            self.table_trackingTickers.insertRow(rowPosition)

            #display data on the table
            for ticker in userTracker:
                self.table_trackingTickers.setItem(rowPosition, 6, QtWidgets.QTableWidgetItem(f'{ticker[5]}'))
                self.table_trackingTickers.setItem(rowPosition, 7, QtWidgets.QTableWidgetItem(f'{ticker[6]}'))
                self.table_trackingTickers.setItem(rowPosition, 2, QtWidgets.QTableWidgetItem(f'{ticker[4]}'))
                self.table_trackingTickers.setItem(rowPosition, 1, QtWidgets.QTableWidgetItem(f'{ticker[3]}'))
                self.table_trackingTickers.setItem(rowPosition, 0, QtWidgets.QTableWidgetItem(f'{ticker[2]}'))
                self.table_trackingTickers.setItem(rowPosition, 3, QtWidgets.QTableWidgetItem(f"{float(symbol_price['price']):.2f}"))

                earned = float(symbol_price['price']) - float(ticker[3])
                self.table_trackingTickers.setItem(rowPosition, 4, QtWidgets.QTableWidgetItem(f"{earned:.2f}"))
                if earned > 0:
                    self.table_trackingTickers.item(rowPosition, 4).setForeground(QtGui.QColor(0,255,0))
                else: 
                    self.table_trackingTickers.item(rowPosition, 4).setForeground(QtGui.QColor(255,0,0))


    def calculator_loadTickerInfo(self):
        ticker = self.comboBox_tickers.currentText()
        if ticker == None:
            QMessageBox.information(self, "Empty Ticker", "Please pick a ticker from the list")
        else:
            try:
                response_price = get_price_symbol(ticker)
                self.lineEdit_curentPrice.setText(f"{float(response_price['price']):.2f}")
            except KeyError:
                QMessageBox.information(self, "Ticker Error", "Something went wrong, please try again")

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
        if self.lineEdit_curentPrice.text() == '' and self.label_RiskedinTrade.text() == '':
            QMessageBox.information(self, "Ticker", "Please choose a ticker from the list")
        
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
            priceRise = maxGained / float(self.lineEdit_totalShares.text())
            self.table_targetPrice.setItem(0, 0, QtWidgets.QTableWidgetItem(f'$ {priceRise:.2f}'))
            
        except ValueError:
            if self.lineEdit_precentRisked.text() == '':
                self.table_targetPrice.setItem(2, 0, QtWidgets.QTableWidgetItem(''))
                self.table_targetPrice.setItem(3, 0, QtWidgets.QTableWidgetItem(''))

    def logout(self):
        self.currentUser = None
        if self.currentUser == None:
            self.on_user_btn()
            QMessageBox.information(self, 'Logout', 'You are logged out successfully')


    # LOGIN SYSTEM2
    def loginFunction(self):
        user = self.inputEmail_login.text()
        password = self.inputPassword_login.text()

        if len(user) == 0 or len(password) == 0:
            self.errorLabel_login.setText('Please fill in all fields')
        else:
            profile = self.data.get_user_profile(user)
                        
            if bcrypt.checkpw(password.encode('utf-8'), profile[2].encode('utf-8')):
                self.errorLabel_login.setText('')
                self.stackedWidget.setCurrentIndex(0)
                
                self.currentUser = profile
                self.fetch_watchlist()
                self.nav_userName.setText(self.currentUser[3])
            else:
                self.inputEmail_login.setText('')
                self.inputPassword_login.setText('')
                self.errorLabel_login.setText("Invalid username or password")

    # SIGNUP SYSTEM
    def signupFunction(self):
        user = self.inputEmail_signup.text()
        name = self.inputName_login.text()
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
                self.inputName_login.setText('')
                self.inputPassword_signup1.text('')
                self.inputPassword_signup2.text('')
            else:
                hash = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
                hashed_pwd = hash.decode('utf-8')
                #add data
                self.data.insert_user_profile(user, hashed_pwd, name)
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

                #fetch quote data
                symbol_quote = get_quote_symbol(ticker[1])

                # fetch actual price data
                symbol_price = get_price_symbol(ticker[1])

                # display data
                self.table_watchlist.setItem(rowPosition, 0, QtWidgets.QTableWidgetItem(ticker[1]))
                self.table_watchlist.setItem(rowPosition, 1, QtWidgets.QTableWidgetItem(ticker[2]))
                self.table_watchlist.setItem(rowPosition, 2, QtWidgets.QTableWidgetItem(f"{float(symbol_price['price']):.2f}"))
                self.table_watchlist.setItem(rowPosition, 3, QtWidgets.QTableWidgetItem(f"{float(symbol_quote['change']):.2f}"))
                self.table_watchlist.setItem(rowPosition, 4, QtWidgets.QTableWidgetItem(f"{float(symbol_quote['percent_change']):.2f}"))
                self.table_watchlist.setItem(rowPosition, 5, QtWidgets.QTableWidgetItem(f"{symbol_quote['volume']}"))

                if float(symbol_quote['change']) > 0 and float(symbol_quote['percent_change']) > 0:
                    self.table_watchlist.item(rowPosition, 3).setForeground(QtGui.QColor(0,255,0))
                    self.table_watchlist.item(rowPosition, 4).setForeground(QtGui.QColor(0,255,0))
                
                else:
                    self.table_watchlist.item(rowPosition, 3).setForeground(QtGui.QColor(255,0,0))
                    self.table_watchlist.item(rowPosition, 4).setForeground(QtGui.QColor(255,0,0))

    # FETCH TICKER INFORMATION
    def fetchTickerInformation(self):
        #get ticker
        itemRow = self.table_watchlist.currentRow()
        ticker = self.table_watchlist.item(itemRow, 0).text()

        #fetch data
        symbol_quote = get_quote_symbol(ticker)

        #fetch profile
        symbol_profile = get_profile_symbol(ticker)

        #display profile
        try:
            # SUMMARY_1
            self.tableWidget_sum_1.setItem(0, 0, QtWidgets.QTableWidgetItem(f"{float(symbol_quote['open']):.2f}"))
            self.tableWidget_sum_1.setItem(0, 1, QtWidgets.QTableWidgetItem(f"{float(symbol_quote['high']):.2f}"))
            self.tableWidget_sum_1.setItem(0, 2, QtWidgets.QTableWidgetItem(f"{float(symbol_quote['low']):.2f}"))
            self.tableWidget_sum_1.setItem(0, 3, QtWidgets.QTableWidgetItem(f"{float(symbol_quote['close']):.2f}"))
            self.tableWidget_sum_1.setItem(0, 4, QtWidgets.QTableWidgetItem(f"{float(symbol_quote['previous_close']):.2f}"))
            self.tableWidget_sum_1.setItem(0, 5, QtWidgets.QTableWidgetItem(f"{symbol_quote['volume']}"))
            self.tableWidget_sum_1.setItem(0, 6, QtWidgets.QTableWidgetItem(f"{symbol_quote['average_volume']}"))

            #SUMMARY_2
            self.tableWidget_sum_2.setItem(0, 0, QtWidgets.QTableWidgetItem(f"{float(symbol_quote['fifty_two_week']['high']):.2f}"))
            self.tableWidget_sum_2.setItem(0, 1, QtWidgets.QTableWidgetItem(f"{float(symbol_quote['fifty_two_week']['low']):.2f}"))
            self.tableWidget_sum_2.setItem(0, 2, QtWidgets.QTableWidgetItem(f"{symbol_quote['fifty_two_week']['range']}"))         

            #SUMMARY_3
            self.tableWidget_sum_3.setHorizontalHeaderItem(0, QtWidgets.QTableWidgetItem(f'{ticker} PROFILE'))
            self.tableWidget_sum_3.setItem(0, 0, QtWidgets.QTableWidgetItem(f"{symbol_profile['name']}"))
            self.tableWidget_sum_3.setItem(0, 1, QtWidgets.QTableWidgetItem(f"{symbol_profile['exchange']}"))
            self.tableWidget_sum_3.setItem(0, 2, QtWidgets.QTableWidgetItem(f"{symbol_profile['sector']}"))
            self.tableWidget_sum_3.setItem(0, 3, QtWidgets.QTableWidgetItem(f"{symbol_profile['industry']}"))
            self.tableWidget_sum_3.setItem(0, 4, QtWidgets.QTableWidgetItem(f"{symbol_profile['employees']}"))
            self.tableWidget_sum_3.setItem(0, 5, QtWidgets.QTableWidgetItem(f"{symbol_profile['type']}"))
            self.tableWidget_sum_3.setItem(0, 6, QtWidgets.QTableWidgetItem(f"{symbol_profile['website']}"))

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
        try:
            # choose ticker
            itemRow = self.table_watchlist.currentRow()
            ticker = self.table_watchlist.item(itemRow, 0).text()
            
            # delete from db
            self.data.delete_ticker(ticker)

            # delete from the table
            self.table_watchlist.removeRow(itemRow) 
        
        except KeyError:
            QMessageBox.information(self, "Delete Ticker", "Please select a ticker to delete.")
        except AttributeError:
            QMessageBox.information(self, "Delete Ticker", "Please select a ticker to delete.")
        
           
    
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
        symbol_quote = get_quote_symbol(ticker)

        # REAL-TIME PRICE
        symbol_price = get_price_symbol(ticker)

        # ADD DATA TO DB
        self.data.add_ticker(ticker, symbol_quote['name'], symbol_quote['exchange'], self.currentUser[0])

        # display data
        rowPosition = self.table_watchlist.rowCount()
        self.table_watchlist.insertRow(rowPosition)

        try:
            self.table_watchlist.setItem(rowPosition, 0, QtWidgets.QTableWidgetItem(ticker))
            self.table_watchlist.setItem(rowPosition, 1, QtWidgets.QTableWidgetItem(f"{symbol_quote['name']}"))
            self.table_watchlist.setItem(rowPosition, 2, QtWidgets.QTableWidgetItem(f"{float(symbol_price['price']):.2f}"))
            self.table_watchlist.setItem(rowPosition, 3, QtWidgets.QTableWidgetItem(f"{float(symbol_quote['change']):.2f}"))
            self.table_watchlist.setItem(rowPosition, 4, QtWidgets.QTableWidgetItem(f"{float(symbol_quote['percent_change']):.2f}"))
            self.table_watchlist.setItem(rowPosition, 5, QtWidgets.QTableWidgetItem(f"{symbol_quote['volume']}"))
        except KeyError:
            pass

        if float(symbol_quote['change']) > 0 and float(symbol_quote['percent_change']) > 0:
                self.table_watchlist.item(rowPosition, 3).setForeground(QtGui.QColor(0,255,0))
                self.table_watchlist.item(rowPosition, 4).setForeground(QtGui.QColor(0,255,0))
        else:
            self.table_watchlist.item(rowPosition, 3).setForeground(QtGui.QColor(255,0,0))
            self.table_watchlist.item(rowPosition, 4).setForeground(QtGui.QColor(255,0,0))


       



 
app = QApplication(sys.argv)
window = MainWindow()
app.exec_()













