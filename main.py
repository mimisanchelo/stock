import sys
from PyQt5.uic import loadUi
from PyQt5 import QtWidgets, QtGui
from PyQt5.QtWidgets import QMainWindow, QWidget, QLabel, QLineEdit, QApplication, QStackedWidget, QPushButton, QTableWidget, QMessageBox
from PyQt5.QtGui import QFont as qfont
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
        self.pushButton_sum_main = self.findChild(QPushButton, 'pushButton_summary_main')
        self.user_btn = self.findChild(QPushButton, 'user_btn')
        self.watchlist_btn = self.findChild(QPushButton, 'watchlist_btn')
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
        #pages
        self.watchlist_page = self.findChild(QWidget, 'watchlitMenu_page') 
        self.welcome_page = self.findChild(QWidget, 'welcome_page') 
        self.login_page = self.findChild(QWidget, 'login_page') 
        self.signup_page = self.findChild(QWidget, 'signup_page') 
        
        #------------ CONNECT BTNS
        # watchlist menu
        self.addTicker_main.clicked.connect(self.openAddTicker)
        self.deleteTicker_main.clicked.connect(self.deleteTicker)
        self.clearList_main.clicked.connect(self.clearWatchList)
        # on click show data of ticker
        self.table_watchlist.selectionModel().selectionChanged.connect(self.fetchTickerInformation)
        
        # connect pages
        self.user_btn.clicked.connect(self.on_user_btn)
        self.watchlist_btn.clicked.connect(self.on_watchlist)
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

    # LOGIN SYSTEM
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
                print(self.currentUser)
            else:
                self.inputEmail_login.setText('')
                self.inputPassword_login.setText('')
                
                self.errorLabel_login.setText("Invalid username or password")

    # SIGNUP SYSTEM
    def signupFunction(self):
        user = self.inputEmail_signup.text()
        password = self.inputPassword_signup1.text()
        password2 = self.inputPassword_signup2.text()
        print(user, password, password2)

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
                #clean fields
                self.inputEmail_signup.text('')
                self.inputPassword_signup1.text('')
                self.inputPassword_signup2.text('')
                self.errorLabel_signup.setText("")
                #move on
                self.stackedWidget.setCurrentIndex(2)
                QMessageBox.information(self, 'Success', 'You have successfully signed up')    
    
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

            if float(response_ticker['change']) > 0 and float(response_ticker['percent_change']) > 0:
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













