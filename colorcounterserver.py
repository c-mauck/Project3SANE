from PyQt5.QtWidgets import QWidget, QApplication
from PyQt5.QtGui import QPixmap, QColor
from PyQt5 import uic, QtGui
from PyQt5.QtCore import QThread, QTimer, pyqtSignal, pyqtSlot, Qt
import flask
import json
from fer import FER
import cv2
import numpy as np
import sys
import datetime

PORT = 5000
counter = 0
ROOT_URL = 'http://localhost:{}'.format(PORT)


class FlaskThread(QThread):
    app = flask.Flask(__name__)
    app.config["DEBUG"] = False
    _run_flag = True

    def run(self):
        global PORT
        self.app.run(port=PORT, host="0.0.0.0")
        while self._run_flag:
            pass
        return

    @app.route("/", methods=['GET'])
    def Home():
        return flask.jsonify({"connection": "successful"})

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
        App.feedback.append({identifier: strtopass})
        print("Printing feedback:")
        print(App.feedback)
        return flask.jsonify({'id': identifier, 'message': strtopass})

    def stop(self):
        """Sets run flag to False and waits for thread to finish"""
        self._run_flag = False
        self.wait()
        self.quit()


class FPS:
    def __init__(self):
        # store the start time, end time, and total number of frames
        # that were examined between the start and end intervals
        self._start = None
        self._end = None
        self._numFrames = 0

    def get_num_frames(self):
        """Returns the numbers of frames counted thus far"""
        return self._numFrames

    def start(self):
        # start the timer
        self._numFrames = 0
        self._start = datetime.datetime.now()
        return self

    def stop(self):
        # stop the timer
        self._end = datetime.datetime.now()

    def update(self):
        # increment the total number of frames examined during the
        # start and end intervals
        self._numFrames += 1

    def elapsed(self):
        # return the total number of seconds between the start and
        # end interval
        return (self._end - self._start).total_seconds()

    def fps(self):
        # compute the (approximate) frames per second
        return self._numFrames / self.elapsed()


updated = True


class VideoThread(QThread):
    change_pixmap_signal = pyqtSignal(np.ndarray)
    detector = FER()

    def __init__(self, widget):
        super().__init__()
        self._run_flag = True
        self.activeApp = widget

    def run(self):
        # capture from webcam
        cap = cv2.VideoCapture(0)
        global updated
        # SEMAPHORE ATTEMPT
        # global updated
        while self._run_flag:
            ret, cv_img = cap.read()
            if ret and updated:
                # SEMAPHORE ATTEMPT
                updated = False

                # Tell other thread to update image
                self.change_pixmap_signal.emit(cv_img)
                emotion, score = self.detector.top_emotion(cv_img)
                # DEBUG
                # print(emotion)
                if emotion and self.activeApp.new_emotion(emotion):
                    # DEBUG
                    # print(emotion)
                    self.activeApp.set_emotion_label(emotion)
                elif not emotion and self.activeApp.new_emotion("No Emotion Detected"):
                    # DEBUG
                    # print("No Face Detected")
                    self.activeApp.set_emotion_label("No Emotion Detected")
                else:
                    # nothing happens, there isn't anything to update
                    pass
        # shut down capture system
        cap.release()

    def stop(self):
        """Sets run flag to False and waits for thread to finish"""
        self._run_flag = False
        self.wait()

class App(QWidget):
    feedback = [{"Default0": "You are cool"}, {"Default2": "I like your face"}]

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
        self.UI.startButton.clicked.connect(self.start_speech)
        self.UI.pushButton.clicked.connect(self.change_set_times)

        # create the video capture thread
        self.thread = VideoThread(self)
        # create an FPS counter
        self.num_frames = 20
        self.fps = FPS().start()
        # connect its signal to the update_image slot
        self.thread.change_pixmap_signal.connect(self.update_image)
        # start the thread
        self.thread.start()

    def setFlask(self, flask):
        self.f_thread = flask

    def setcountlabel(self, num):
        numtext = str(num)
        self.UI.textLabel.setText("Grammar: " + numtext)

    def settextlabel(self, string):
        strtext = str(string)
        self.UI.textLabel2.setText("Timer: " + strtext)

    def start_speech(self):
        self.start_timer()
        print("Speech is started")

    #DEBUG
    def new_emotion(self, string):
        if string == self.emotion_label.text():
            return False
        else:
            return True

    def set_emotion_label(self, string):
        print(string)
        # self.emotion_label.setText(string)

    def set_fps_label(self, string):
        print(string)
        # self.fps_label.setText(string)

    def end_speech(self):
        now = datetime.datetime.now()
        print("Speech has ended")
        new_file = "speech"
        speechandname = "Speech title and speaker name"
        dt_string = now.strftime("%b-%d-%Y %H:%M:%S")
        f = open((new_file + ".txt"), "w+")
        f.write(speechandname + "\r\n")
        f.write(dt_string + "\r\n")
        f.write("Final " + self.UI.textLabel2.text() + "\n")
        f.write("======= Feedback =======\n")
        output = (json.dumps(self.feedback))
        f.write(output)
        f.close()
        self.end_timer()

    def change_set_times(self):
        """Get settings for the time change page"""
        print("Trying to change set times")
        if len(self.UI.min_time_edit.text()) > 0:
            text = self.UI.min_time_edit.text()
            print(text)
            seconds = self.get_sec(text)
            print("Min stored: " + str(seconds))
            self.speechMin = seconds
            self.UI.min_time_edit.clear()
        if len(self.UI.mid_time_edit.text()) > 0:
            text = self.UI.mid_time_edit.text()
            print(text)
            seconds = self.get_sec(text)
            print("Mid stored: " + str(seconds))
            self.speechMid = seconds
            self.UI.mid_time_edit.clear()
        if len(self.UI.max_time_edit.text()) > 0:
            text = self.UI.max_time_edit.text()
            print(text)
            seconds = self.get_sec(text)
            print("Max stored: " + str(seconds))
            self.speechMax = seconds
            self.UI.max_time_edit.clear()

    def get_sec(self, time_str):
        """Get seconds from time."""
        m, s = time_str.split(':')
        print("Seconds parsed: " + str(datetime.timedelta(hours=0, minutes=int(m), seconds=int(s)).total_seconds()))
        return int(datetime.timedelta(hours=0, minutes=int(m), seconds=int(s)).total_seconds())

    def timer_timeout(self):
        self.running_time += 1
        num = self.running_time
        seconds = num % 60
        if num >= 60:
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

        if seconds < 10:
            current_time = (str(int(minutes)) + ":0" + str(seconds))
        else:
            current_time = (str(int(minutes)) + ":" + str(seconds))
        self.settextlabel(current_time)

    def start_timer(self):
        self.timer = QTimer(self)
        self.running_time = 0
        self.timer.timeout.connect(self.timer_timeout)
        self.timer.start(1000)

    def end_timer(self):
        self.timer.stop()

    def convert_cv_qt(self, cv_img):
        """Convert from an opencv image to QPixmap"""
        rgb_image = cv2.cvtColor(cv_img, cv2.COLOR_BGR2RGB)
        h, w, ch = rgb_image.shape
        bytes_per_line = ch * w
        convert_to_Qt_format = QtGui.QImage(rgb_image.data, w, h, bytes_per_line, QtGui.QImage.Format_RGB888)
        p = convert_to_Qt_format.scaled(self.width, self.height, Qt.KeepAspectRatio)
        return QPixmap.fromImage(p)

    def closeEvent(self, event):
        flaskThread.stop()
        event.accept()


if __name__ == "__main__":
    qtApp = QApplication(sys.argv)
    a = App()
    flaskThread = FlaskThread(a)
    a.setFlask(flaskThread)
    flaskThread.start()
    a.settextlabel("0:00")
    a.setcountlabel(0)
    a.UI.show()
    sys.exit(qtApp.exec_())
