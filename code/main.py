from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtWebEngineWidgets import *
from PyQt5.QtPrintSupport import *
import os
import sys
import re
import json
from urllib.request import urlopen
import requests
from PyQt5 import QtWidgets, QtCore



class MainWindow(QMainWindow):


    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)


        self.tabs = QTabWidget()

        self.tabs.setDocumentMode(True)

        self.tabs.tabBarDoubleClicked.connect(self.tab_open_doubleclick)

        self.tabs.currentChanged.connect(self.current_tab_changed)

        self.tabs.setTabsClosable(True)

        self.tabs.tabCloseRequested.connect(self.close_current_tab)

        self.setCentralWidget(self.tabs)

        self.status = QStatusBar()

        self.setStatusBar(self.status)


        navtb = QToolBar("Navigation")

        self.addToolBar(navtb)

        back_btn = QAction("Back", self)

        back_btn.setStatusTip("Back to previous page")


        back_btn.triggered.connect(lambda: self.tabs.currentWidget().back())

        navtb.addAction(back_btn)

        next_btn = QAction("Forward", self)
        next_btn.setStatusTip("Forward to next page")
        next_btn.triggered.connect(lambda: self.tabs.currentWidget().forward())
        navtb.addAction(next_btn)

        reload_btn = QAction("Reload", self)
        reload_btn.setStatusTip("Reload page")
        reload_btn.triggered.connect(lambda: self.tabs.currentWidget().reload())
        navtb.addAction(reload_btn)

        home_btn = QAction("Home", self)
        home_btn.setStatusTip("Go home")

        home_btn.triggered.connect(self.navigate_home)
        navtb.addAction(home_btn)

        navtb.addSeparator()

        self.urlbar = QLineEdit()

        self.urlbar.returnPressed.connect(self.navigate_to_url)

        navtb.addWidget(self.urlbar)

        stop_btn = QAction("Stop", self)
        stop_btn.setStatusTip("Stop loading current page")
        stop_btn.triggered.connect(lambda: self.tabs.currentWidget().stop())
        navtb.addAction(stop_btn)

        url = 'http://ipinfo.io/json'
        response = urlopen(url)
        data = json.load(response)
        country = data['country']
        if country == "Russia" or "Belarus":
            self.add_new_tab(QUrl('http://yandex.ru'), 'Homepage')
        else:
            self.add_new_tab(QUrl('http://google.com'), 'Homepage')


        self.show()

        self.setWindowTitle("Browui")

    def add_new_tab(self, qurl=None, label="Blank"):

        if qurl is None:
            url = 'http://ipinfo.io/json'
            response = urlopen(url)
            data = json.load(response)
            country = data['country']
            if country == "Russia" or "Belarus":
                qurl = QUrl('http://yandex.ru')
            else:
                qurl = QUrl('http://google.com')

        browser = QWebEngineView()

        browser.setUrl(qurl)

        i = self.tabs.addTab(browser, label)
        self.tabs.setCurrentIndex(i)
        browser.urlChanged.connect(lambda qurl, browser=browser:
                                   self.update_urlbar(qurl, browser))

        browser.loadFinished.connect(lambda _, i=i, browser=browser:
                                     self.tabs.setTabText(i, browser.page().title()))

    def tab_open_doubleclick(self, i):

        if i == -1:
            self.add_new_tab()

    def current_tab_changed(self, i):

        qurl = self.tabs.currentWidget().url()

        self.update_urlbar(qurl, self.tabs.currentWidget())
        self.update_title(self.tabs.currentWidget())


    def close_current_tab(self, i):

        if self.tabs.count() < 2:
            return

        self.tabs.removeTab(i)

    def update_title(self, browser):

        if browser != self.tabs.currentWidget():
            return

        title = self.tabs.currentWidget().page().title()
        self.setWindowTitle("% s - Browui" % title)

    def navigate_home(self):
        url = 'http://ipinfo.io/json'
        response = urlopen(url)
        data = json.load(response)
        country = data['country']
        if country == "Russia" or "Belarus":
            self.tabs.currentWidget().setUrl(QUrl("http://yandex.ru"))
        else:
            self.tabs.currentWidget().setUrl(QUrl("http://www.google.com"))
    def navigate_to_url(self):
        q = QUrl(self.urlbar.text())

        if q.scheme() == "":
            q.setScheme("http")

        self.tabs.currentWidget().setUrl(q)

    def update_urlbar(self, q, browser=None):

        if browser != self.tabs.currentWidget():
            return

        self.urlbar.setText(q.toString())

        self.urlbar.setCursorPosition(0)

    def mousePressEvent(self, event):
        if event.button() == QtCore.Qt.LeftButton:
            self.dragPosition = event.globalPos() - self.mainWindow.frameGeometry().topLeft()
            event.accept()
    def mouseMoveEvent(self, event):
        if event.buttons() == QtCore.Qt.LeftButton:
            self.mainWindow.move(event.globalPos() - self.dragPosition)
            event.accept()

    #    class Tab(QtWidgets.QWidget, Ui_tabWidget):


#        clicked = QtCore.pyqtSignal(int)

        #        def __init__(self, parent=None):
    #            super(Tab, self).__init__(parent=parent)
            #            self.setupUi(self)
        #
        #        def setActive(self, act):
    #            if act == 0:
        #                self.tabWidget_2.setStyleSheet("QWidget{\n"
#                                               "    background-color:rgba(0, 0, 0, 0);\n"
#                                               "    color:rgb(144, 144, 144);\n"
#                                               "    padding:2px;\n"
#                                               "}QWidget:hover{\n"
#                                               "    background-color:rgb(25, 25, 25);\n"
#                                               "    border-top-left-radius:5px;\n"
#                                               "    border-top-right-radius:5px;\n"
#                                               "}")
                #            else:
        #                self.tabWidget_2.setStyleSheet("QWidget{\n"
#                                               "    background-color:rgb(35, 34, 39);\n"
#                                               "    color:rgb(170, 170, 170);\n"
#                                               "    border-top-left-radius:5px;\n"
#                                              "    border-top-right-radius:5px;\n"
#                                               "    padding:2px;\n"
#                                               "}")
#
#        def setId(self, bId):
#            self.tabPushButton.setObjectName(str(bId))
#
#        def mousePressEvent(self, event):
#            if event.button() == QtCore.Qt.LeftButton:
#                self.clicked.emit(int(self.tabPushButton.objectName()))


app = QApplication(sys.argv)

app.setApplicationName("Browui")

window = MainWindow()

app.exec_()
