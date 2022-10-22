from PyQt5.QtWidgets import QWidget, QApplication, QLabel, QVBoxLayout
from PyQt5.QtGui import QPixmap, QColor
from PyQt5.QtCore import QThread
import flask
from flask import Flask
import sys

PORT = 5000
counter = 0
ROOT_URL = 'http://localhost:{}'.format(PORT)
flaskApp = Flask(__name__)


class FlaskThread(QThread):
    app = flask.Flask(__name__)
    #counter = 0

    def __init__(self, application):
        QThread.__init__(self)
        global counter
        # self._run_flag = True
        self.activeApp = application

    def run(self):
        global PORT
        self.activeApp.run(port=PORT, host="0.0.0.0")

    @app.route("/")
    def home():
        return "Hello! This is the main page <h1>Hello<h1>"

    @app.route("/<name>")
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
        return flask.jsonify({'counter': counter})

    @app.route("/api/counter", methods=['GET'])
    def server_get_count():
        global counter
        return flask.jsonify({'counter': counter})


class App(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Qt static label demo")
        width = 640
        height = 480
        # create the label that holds the image
        self.image_label = QLabel(self)
        # create a text label
        self.textLabel = QLabel('Demo')

        # create a vertical box layout and add the two labels
        vbox = QVBoxLayout()
        vbox.addWidget(self.image_label)
        vbox.addWidget(self.textLabel)
        # set the vbox layout as the widgets layout
        self.setLayout(vbox)
        # create a grey pixmap
        grey = QPixmap(width, height)
        grey.fill(QColor('darkGray'))
        # set the image to the grey pixmap
        self.image_label.setPixmap(grey)

    def setcountlabel(self, num):
        numtext = str(num)
        self.textLabel.setText("Counter: " + numtext)


if __name__ == "__main__":
    qtApp = QApplication(sys.argv)
    flaskThread = FlaskThread(flaskApp)
    flaskThread.start()
    a = App()
    a.show()
    sys.exit(qtApp.exec_())
