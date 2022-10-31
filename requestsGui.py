import sys
from PyQt5 import QtWidgets, uic
from PyQt5.QtCore import QThread
import requests

import time

# This works, it's necessary that the URL's match
ip = "127.0.0.1"
clientID = "User1"

def increment_count():
    global ip
    try:
        req = requests.post(f'http://{ip}:5000/api/counter', json={"add": 1})
        if req.ok:
            print(req.json())
            UI.label_status.setText("Connected: " + str(ip))
        else:
            print("Error: " + str(req.status_code))
    except requests.exceptions.ConnectionError as errc:
        UI.label_status.setText("No Connection")
        print("An Error Connecting to the API occurred: No connection")
        print(repr(errc))


def decrement_count():
    global ip
    global clientID
    try:
        req = requests.post(f'http://{ip}:5000/api/counter', json={"add": -1})
        if req.ok:
            print(req.json())
            UI.label_status.setText("Connected: " + str(ip))
        else:
            print("Error: " + str(req.status_code))
    except requests.exceptions.ConnectionError as errc:
        UI.label_status.setText("No Connection")
        print("An Error Connecting to the API occurred: No connection")
        print(repr(errc))


def send_text():
    if len(UI.lineEdit.text()) > 0:
        text = UI.lineEdit.text()
        UI.lineEdit.clear()
        try:
            r = requests.post('http://127.0.0.1:5000/api/set_text', json={"message": text})
            if r.ok:
                print(r.json())
                UI.label_status.setText("Connected: " + str(ip))
            else:
                print("Error: " + str(r.status_code))
        except requests.exceptions.ConnectionError as errc:
            UI.label_status.setText("No Connection")
            print("An Error Connecting to the API occurred: No connection")
            print(repr(errc))


def send_feedback():
    if len(UI.lineEdit.text()) > 0:
        feedback = UI.lineEdit.text()
        UI.lineEdit.clear()
        try:
            r = requests.post('http://127.0.0.1:5000/api/send_feedback', json={"message": feedback, "id": "User1"})
            if r.ok:
                print(r.json())
                UI.label_status.setText("Connected: " + str(ip))
            else:
                print("Error: " + str(r.status_code))
        except requests.exceptions.ConnectionError as errc:
            UI.label_status.setText("No Connection")
            print("An Error Connecting to the API occurred: No connection")
            print(repr(errc))


def make_connection(ip_address=ip):
    """This is to make a connection to the server via entering an IP"""
    connected = False
    try:
        r = requests.get(f'http://{ip_address}/')
        if r.ok:
            print(r.json())
            UI.label_status.setText("Connected: " + str(ip))
            connected = True
        else:
            print("Error: " + str(r.status_code))
    except requests.exceptions.ConnectionError as errc:
        UI.label_status.setText("No Connection")
        print("An Error Connecting to the API occurred: No connection")
        print(repr(errc))
    return connected

App = QtWidgets.QApplication([])
UI = uic.loadUi("testUi.ui")


UI.decrementButton.clicked.connect(decrement_count)
UI.incrementButton.clicked.connect(increment_count)
UI.sendButton.clicked.connect(send_feedback)
make_connection()


UI.show()
sys.exit(App.exec_())
