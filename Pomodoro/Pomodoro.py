import random
import sys

from PyQt6.QtCore import *
from PyQt6.QtWidgets import *
from PyQt6.QtGui import *
from PyQt6 import QtCore
import playsound
import json


        #TODO: Fix Line 119 - Center the Test and though the text size adjusts, it should always remain center.
        #TODO: Fix Victory Lines the same way


        #TODO: Fix the timer reset from an in progress pom to break (Break does not reset.)
        # There is no difference in set up between Pom/Timer
        # timer_start is being implied when timer_type exists.
        # Check values and definition through code.
        # break complete text size
        # Most likely self.timer.singleshot(True) will be the way to go, but trying to figure out how to do this.
        # Do we want to clear the Type Flag when the timer ends? Then check if flags exist, if not buttonwork

                    #SOLUTION:### Solution ###

                    # The Status property was NOT being changed for Break Button.
                    #  Because of this - wasn't doing anything.

        #TODO: Bug Report - When a break/pomo ends, and another pomo is started, it will reset to 60 minutes.
            # Error handling - if no value exists in the pom fields, should automatically add a default amount from
            # Future settings screen.
            #Happens on both pom and break

            ## I tracked it down to the case statement for what type of break the timer should be doing. I can get the value,
            ## and set it too - but it doesn't seem to update the timer value.

                                    #### Solution ####
                                    # self.timer.disconnect was needed

class TWindow(QWidget):
    def __init__(self):
        super().__init__()


        with open('hiddenmessage.json') as f:
            self.hmvalue = json.load(f)

        self.t_type = None
        self.pom_min_label = 0

        self.setWindowTitle("Pomodoro Timer")
        #self.setWindowIcon(QIcon("icon.png"))
        self.setFixedWidth(500)
        self.setFixedHeight(200)

        # for a future update to not include the title
        self.setWindowFlag(QtCore.Qt.WindowType.FramelessWindowHint)
        #self.setWindowOpacity(.5)
        # background: transparent;
        self.setStyleSheet("background-color: #495252; ")

        self.create_buttons()
        self.timer_details()

        #Sets up some stuff
        #This creates the minimize view bool. It starts unhidden, so false.
        self.hiding = False

        self.timer = QtCore.QTimer()

    # Mouse Events

    def mousePressEvent(self, event):
        self.oldPosition = event.globalPosition().toPoint()

    def mouseMoveEvent(self, event):
        self.move(self.pos() + event.globalPosition().toPoint() - self.oldPosition)
        self.oldPosition = event.globalPosition().toPoint()

    def mouseDoubleClickEvent(self, QMouseEvent):
        self.minimizeview()

    #Build the pieces
    def create_buttons(self):

        # C/D Button
        self.playbutton = "AddOn_Functionality/Pomodoro/Play.png"
        self.pausebutton = "AddOn_Functionality/Pomodoro/Pause.ico"

        self.connect_button = QPushButton("Start Timer", self)
        self.connect_button.setGeometry(130, 100, 100, 40)
        self.connect_button.setStyleSheet("background-color: #191D1D;")
        # self.connect_button.clicked.connect(lambda: self.timer_start())
        self.connect_button.clicked.connect(lambda: self.timer_decide(timer_type='pom'))
        self.connect_button.setProperty("status", "Off")

        self.breakbutton = QPushButton("Start break", self)
        self.breakbutton.setGeometry(250, 100, 100, 40)
        self.breakbutton.setStyleSheet("background-color: #191D1D;")
        self.breakbutton.clicked.connect(lambda: self.timer_decide(timer_type='break'))
        self.breakbutton.setProperty("status", "Off")

        self.pom_dropdown = QComboBox(self)
        self.pom_dropdown.addItem("Short Pomodoro")
        self.pom_dropdown.addItem("Long Pomodoro")
        self.pom_dropdown.addItem("Short Break")
        self.pom_dropdown.addItem("Long Break")
        self.pom_dropdown.setStyleSheet("QComboBox" 
                                        "{"
                                        "background-color: #495252;"
                                        "}")
        self.pom_dropdown.setStyleSheet("QListView"
                                     "{"
                                     "background-color: #191D1D;"
                                     "}")
        self.pom_dropdown.setGeometry(175, 145, 150, 25)

        # For when minimal view is showing
        self.hiddenmessage = QLabel(self)
        self.hiddenmessage.hide()
        self.hiddenmessage.setGeometry(50, 100, 275, 175)
        self.hiddenmessage.setFont(QFont("Helvetica", 20))
        self.hiddenmessage.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.hiddenmessage.setStyleSheet("border: 1px solid black;")

        # Below will later be updated to its own property window to save the settings.

        self.short_pom = QLineEdit(self)
        self.short_pom.setPlaceholderText("Short Pom")
        self.short_pom.setGeometry(50, 170, 75, 25)

        self.long_pom = QLineEdit(self)
        self.long_pom.setPlaceholderText("Long Pom")
        self.long_pom.setGeometry(130, 170, 75, 25)

        self.short_break = QLineEdit(self)
        self.short_break.setPlaceholderText("Short Break")
        self.short_break.setGeometry(250, 170, 75, 25)

        self.long_break = QLineEdit(self)
        self.long_break.setPlaceholderText("Long Break")
        self.long_break.setGeometry(325, 170, 75, 25)

        quit_button = QPushButton("Quit", self)
        quit_button.setGeometry(0, 0, 75, 30)
        quit_button.setStyleSheet("background-color: #191D1D;")
        quit_button.clicked.connect(lambda: sys.exit())

        # Create the Pomo Counter
        self.counter_pom = 0
        self.pom_counter_label = QLabel(self)
        self.pom_counter_label.setText(f"Pomo Count: {str(self.counter_pom)}")
        self.pom_counter_label.setFont(QFont("Arial", 15))
        self.pom_counter_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.pom_counter_label.setGeometry(380, 10, 100, 30)

    def minimizeview(self):
        if self.hiding:
            self.short_pom.show()
            self.long_pom.show()
            self.short_break.show()
            self.long_break.show()
            self.connect_button.show()
            self.breakbutton.show()
            self.breakbutton.setVisible(True)
            self.pom_dropdown.show()
            self.hiding = False
            self.hiddenmessage.hide()
        else:
            self.hiddenmessages = self.hmvalue["replymsg"]

            self.hiding = True
            self.short_pom.hide()
            self.long_pom.hide()
            self.short_break.hide()
            self.long_break.hide()
            self.connect_button.hide()
            self.breakbutton.hide()
            self.breakbutton.setVisible(False)
            # self.breakbutton.setStyleSheet('background:transparent;')
            # self.breakbutton.setStyleSheet('border: transparent;')
            self.pom_dropdown.hide()
            self.hiddenmessage.setText(random.choice(self.hiddenmessages))
            self.hiddenmessage.adjustSize()
            self.hiddenmessage.show()

    ### Timer Stuff
    def timer_decide(self, timer_type):
        print("I got hit")
        self.t_type = timer_type
        print(self.t_type)

        match timer_type:
            case 'pom':
                self.currenttime_button = self.connect_button
                self.opposite_button = self.breakbutton
                self.timer_type = timer_type

                match self.pom_dropdown.currentText():
                    case 'Short Pomodoro':
                        self.timer_amt = int(self.short_pom.text())
                    case 'Long Pomodoro':
                        self.timer_amt = int(self.long_pom.text())

            case 'break':
                print("I got to the break")
                self.currenttime_button = self.breakbutton
                self.opposite_button = self.connect_button

                match self.pom_dropdown.currentText():
                    case 'Short Break':
                        print("I got to the short break")
                        self.timer_amt = int(self.short_break.text())
                        print(self.currenttime_button.property("status"))
                    case 'Long Break':
                        print("I got to the long break")
                        self.timer_amt = int(self.long_break.text())

                print(f"Timer Amount: {self.timer_amt}")

        if self.currenttime_button.property("status") == "Off":
            print("I got to the off line")
            self.currenttime_button.setProperty("status", "On")
            print("I got to the on line")
            self.currenttime_button.setIcon(QIcon(self.playbutton))
            self.opposite_button.setDisabled(True)
            self.opposite_button.setIcon(QIcon())
            print(self.short_pom.text())
            self.timer_start(stime=int(self.timer_amt), t_type=timer_type)

        elif self.currenttime_button.property("status") == "On":
            self.currenttime_button.setProperty("status", "Paused")
            self.opposite_button.setDisabled(False)
            self.opposite_button.setIcon(QIcon())
            self.currenttime_button.setIcon(QIcon(self.pausebutton))
            self.timer.stop()

        elif self.currenttime_button.property("status") == "Paused":
            self.currenttime_button.setProperty("status", "On")
            self.opposite_button.setDisabled(True)
            self.opposite_button.setIcon(QIcon())
            self.currenttime_button.setIcon(QIcon(self.playbutton))
            self.timer.start(1000)

    def timer_details(self):
        #Time Label
        self.pom_label = QLabel(self)
        # self.pom_label.setStyleSheet("border: 1px solid black;")
        self.pom_label.setText("00:00")
        self.pom_label.setFont(QFont("Arial", 40))
        self.pom_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.pom_label.setGeometry(130, 50, 220, 50)

    def timer_start(self, stime, t_type):
        print(f"Timer Started at:{self.timer_amt}")
        print(f"T_type: {t_type}")
        if t_type == 'pom':
            print("This is a pom")
            if stime == 0 or stime is None or stime == "":
                print(f"Stime={stime}")
                self.self.timer_amt = 25

            else:
                # self.pom_min_label = int(stime)
                print("Temp")

        if t_type == 'break':
            print("This is a break")
            if stime == 0 or stime is None or stime == "":
                self.self.timer_amt = 10

            else:
                self.pom_min_label = int(stime)

        self.pomtime = QtCore.QTime(00, int(self.timer_amt), 00)
        # self.pomtime = QtCore.QTime(00, 00, 10)

        self.timer.timeout.connect(lambda: self.time())
        self.timer.start(1000)


    def time(self):
        self.pomtime = self.pomtime.addSecs(-1)
        print(f"minute:{self.pomtime.minute()}:second:{self.pomtime.second()}:type:{self.t_type}")
        self.rem_time = '{:02d}:{:02d}'.format(self.pomtime.minute(), self.pomtime.second())
        self.pom_label.setText(self.rem_time)

        ### We need to confirm the break or pom type and play the appropiate sound

        if self.pomtime.minute() == 0 and self.pomtime.second() == 0 and self.t_type =='pom':
            self.victory()

        if self.pomtime.minute() == 0 and self.pomtime.second() == 0 and self.t_type =='break':
            self.victory()

    def victory(self):
        QTimer.stop(self.timer)
        self.connect_button.setProperty("status", "Off")
        self.breakbutton.setProperty("status", "Off")
        self.opposite_button = self.connect_button
        self.breakbutton.setDisabled(False)
        self.connect_button.setDisabled(False)

        if self.t_type == 'pom':
            self.pom_label.setText("VICTORY")
            self.pom_label.adjustSize()
            self.play_victory()

        elif self.t_type =='break':
            self.pom_label.setText("CRUSHED IT")
            self.pom_label.adjustSize()
            self.play_breakend()

        else:
            print("Not sure why it got here.")
            pass

        self.t_type = None

        print("----")
        print(f'{self.pomtime.minute()},{self.pomtime.second()},{self.t_type}')
        print("----")
        if QTimer.remainingTime(self.timer) == -1:
            print(f"Ok I'm in the negative with the value of: {QTimer.remainingTime(self.timer)}")

    def play_victory(self):
        playsound.playsound("Victory.m4a", False)
        self.counter_pom += 1
        self.pom_counter_label.setText(f"Pomo Count: {str(self.counter_pom)}")
        self.timer.disconnect()

    def play_breakend(self):
        print('break Ended')
        self.timer.disconnect()

def main():
    bot_app = QApplication([])
    window = TWindow()
    window.show()
    sys.exit(bot_app.exec())


if __name__ == '__main__':
    main()
