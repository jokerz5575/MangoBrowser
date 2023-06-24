import sys
import json
import requests
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtWebEngineWidgets import *

def getSettingsData(dataName):
    f = open('settings.json')
    json_obj = f.read()
    settings = json.loads(json_obj)
    print(settings)
    for i in settings:
        print(settings[0][dataName])
        return settings[0][dataName]

def setSettingsData(dataName, newValue):
    f = open('settings.json')
    json_obj = f.read()
    settings = json.loads(json_obj)
    for i in settings:
        settings[0][dataName] = newValue
    
    with open('settings.json', "w") as outfile:
        json.dump(settings, outfile)

class MainWindow(QMainWindow):
    
    def __init__(self):
        super(MainWindow, self).__init__()
        self.browser = QWebEngineView()
        self.browser.setUrl(QUrl(getSettingsData('defaultUrl')))
        self.setCentralWidget(self.browser)
        self.showMaximized()
    
        # navbar
        navbar = QToolBar()
        self.addToolBar(navbar)

        back_btn = QAction('Back', self)
        back_btn.triggered.connect(self.browser.back)
        navbar.addAction(back_btn)

        forward_btn = QAction('Forward', self)
        forward_btn.triggered.connect(self.browser.forward)
        navbar.addAction(forward_btn)

        reload_btn = QAction('Reload', self)
        reload_btn.triggered.connect(self.browser.reload)
        navbar.addAction(reload_btn)

        home_btn = QAction('Home', self)
        home_btn.triggered.connect(self.navigate_home)
        navbar.addAction(home_btn)

        self.url_bar = QLineEdit()
        self.url_bar.returnPressed.connect(self.navigate_to_url)
        navbar.addWidget(self.url_bar)

        settings_btn = QAction('Settings', self)
        settings_btn.triggered.connect(self.open_settings)
        navbar.addAction(settings_btn)

        self.browser.urlChanged.connect(self.update_url)

    def navigate_home(self):
        self.browser.setUrl(QUrl(getSettingsData('defaultUrl')))

    def navigate_to_url(self):
        url = self.url_bar.text()
        print(QUrl(url))
        if(url.startswith('https://')):
            self.browser.setUrl(QUrl(url))
        else:
            self.browser.setUrl(QUrl("https://"+url))
        

    def update_url(self, q):
        self.url_bar.setText(q.toString())

    def open_settings(self):

        dlg = QDialog(self)
        dlg.setWindowTitle("Settings")

        layout = QGridLayout(dlg)

        layout.addWidget(QLabel("Default page:"),0,0)

        input_field = QLineEdit()
        input_field.setText(getSettingsData('defaultUrl')) 
        layout.addWidget(input_field,0,1)

        save_btn = QPushButton("Save")
        layout.addWidget(save_btn,1,0)

        close_btn = QPushButton("Close")
        layout.addWidget(close_btn,1,1)

        save_btn.clicked.connect(lambda: self.save_settings(input_field.text()))
        save_btn.clicked.connect(dlg.reject)
        close_btn.clicked.connect(dlg.reject)
        
        dlg.exec()

    def save_settings(self, newUrl):
        #Update JSON
        print("In here!!! New url is: "+newUrl)
        if(newUrl.startswith('https://')):
            setSettingsData('defaultUrl', newUrl)
        else:
            newUrl = "https://" + newUrl
            setSettingsData('defaultUrl', newUrl)


app = QApplication(sys.argv)
QApplication.setApplicationName('MangoBrowser')
window = MainWindow()
app.exec_()
