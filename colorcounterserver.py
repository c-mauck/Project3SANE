from PyQt5.QtWidgets import QWidget, QApplication, QLabel, QVBoxLayout
from PyQt5.QtGui import QPixmap, QColor
from PyQt5 import uic
from PyQt5.QtCore import QThread, QTimer
import flask
from flask import Flask
import sys
import time

PORT = 5000
counter = 0
ROOT_URL = 'http://localhost:{}'.format(PORT)


class FlaskThread(QThread):
    app = flask.Flask(__name__)
    app.config["DEBUG"] = False

    def run(self):
        global PORT
        self.app.run(port=PORT, host="0.0.0.0")

    @app.route("/", methods=['GET'])
    def Home():
        return flask.jsonify({"connection":"successful"})

    @app.route("/<name>", methods=['GET'])
    def entry(name):
        return "Hello! This is the main page <h1>%s<h1>" % name

    @app.route("/api/counter", methods=['POST'])
    def server_count_increment():
        """Method to post and adjust the internal counter"""
        global counter
        content = flask.request.json
        add = content['add']
        print(f"Number to add: {add}")
        counter += add
        print(f"Counter is now: {counter}")
        a.setcountlabel(counter)
        return flask.jsonify({'counter': counter})

    @app.route("/api/counter", methods=['GET'])
    def server_get_count():
        global counter
        return flask.jsonify({'counter': counter})

    @app.route("/api/set_text", methods=['POST'])
    def setLabel2():
        content = flask.request.json
        strtopass = content['message']
        print(strtopass)
        a.settextlabel(strtopass)
        return flask.jsonify({'message': strtopass})

    @app.route("/api/send_feedback", methods=['POST'])
    def storeFeedback():
        content = flask.request.json
        identifier = content['id']
        strtopass = content['message']
        print(f"{identifier} says: \n{strtopass}")
        return flask.jsonify({'id': identifier, 'message': strtopass})


class App(QWidget):
    def __init__(self):
        super().__init__()
        self.UI = uic.loadUi("serverUi.ui")
        width = 640
        height = 480
        self.speechMax = 300
        self.speechMid = 240
        self.speechMin = 120
        self.timer_BGColor = "rgb(255,255,255);"
        self.timer_FGColor = "rgb(0,0,0);"
        self.UI.textLabel2.setStyleSheet(
            "QLabel {background-color :" + self.timer_BGColor + "color : " + self.timer_FGColor + "}")
        # create a grey pixmap
        grey = QPixmap(width, height)
        grey.fill(QColor('darkGray'))
        # set the image to the grey pixmap
        self.UI.image_label.setText("Text message")
        self.UI.image_label.setPixmap(grey)
        self.UI.stopButton.clicked.connect(self.end_speech)
        self.startTimer()

    def setcountlabel(self, num):
        numtext = str(num)
        self.UI.textLabel.setText("Counter: " + numtext)

    def settextlabel(self, string):
        strtext = str(string)
        self.UI.textLabel2.setText(strtext)

    def start_speech(self):
        print("Speech is started")

    def end_speech(self):
        print("Speech has ended")
        new_file = input("File name: ")
        speechandname = input ("Speech title and speaker name: ")
        f = open((new_file + ".txt"), "w+")
        f.write(speechandname + "\r\n")
        f.write("Final " + self.UI.textLabel2.getText())
        f.close()
        self.endTimer()

    def timer_timeout(self):
        self.running_time += 1
        num = self.running_time
        seconds = num % 60
        if num > 60:
            minutes = (num - (num % 60))/60
        else:
            minutes = 0
        if num == self.speechMax:
            print("overtime")
            self.timer_BGColor = "rgb(255,0,0);"
            self.timer_FGColor = "rgb(0,0,0);"
            self.UI.textLabel2.setStyleSheet(
                "QLabel {background-color :" + self.timer_BGColor + "color : " + self.timer_FGColor + "}")
        elif num == (self.speechMax - 10):
            self.UI.textLabel2.setStyleSheet("QLabel {font-weight:bold;}")
        elif num == self.speechMid:
            print("At time")
            self.timer_BGColor = "rgb(255,255,0);"
            self.timer_FGColor = "rgb(0,0,0);"
            self.UI.textLabel2.setStyleSheet(
                "QLabel {background-color :" + self.timer_BGColor + "color : " + self.timer_FGColor + "}")
        elif num == self.speechMin:
            print("In time")
            self.timer_BGColor = "rgb(0,255,0);"
            self.timer_FGColor = "rgb(0,0,0);"
            self.UI.textLabel2.setStyleSheet(
                "QLabel {background-color :" + self.timer_BGColor + "color : " + self.timer_FGColor + "}")
        elif num == self.speechMin:
            print("undertime")

        current_time = ("Timer: " + str(int(minutes)) + ":" + str(seconds))
        self.settextlabel(current_time)

    def startTimer(self):
        self.timer = QTimer(self)
        self.running_time = 0
        self.timer.timeout.connect(self.timer_timeout)
        self.timer.start(1000)

    def endTimer(self):
        self.timer.stop()


if __name__ == "__main__":
    qtApp = QApplication(sys.argv)
    a = App()
    flaskThread = FlaskThread(a)
    flaskThread.start()
    a.UI.textLabel.setText(str(counter))
    a.UI.show()
    sys.exit(qtApp.exec_())
