import sys
from PyQt5 import QtWidgets, uic
from PyQt5.QtCore import QThread
import requests

import time

# This works, it's necessary that the URL's match
ip = "127.0.0.1"


def post2count(num):
    global ip
    req = requests.post(f'http://{ip}:5000/api/counter', json={"add": num})
    if req.ok:
        print(req.json())
    else:
        print("Error: " + str(req.status_code))


App = QtWidgets.QApplication([])
UI = uic.loadUi("testUi.ui")

#UI.decrementButton.clicked.connect(post2count(-1))
#UI.incrementButton.clicked.connect(post2count(1))
#UI.actionQuit.triggered.connect(App.quit())

UI.show()
sys.exit(App.exec_())
