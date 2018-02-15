from PyQt4.QtGui import QApplication, QIcon, QMainWindow
from PyQt4.QtCore import Qt
import arduinoValvulas
import MainWindow


class MainWindowStart(QMainWindow, MainWindow.Ui_MainWindow):
    def __init__(self, parent=None):
        super(MainWindowStart, self).__init__(parent)
        self.setupUi(self)

        self.btn_yes.clicked.connect(self.start_valve_window)

    def start_valve_window(self):
        arduino_valves = arduinoValvulas.ValvulasMainWindow(self)
        # arduino_valves.setWindowFlags(Qt.WindowStaysOnTopHint)

        # arduino_valves.setWindowModality(Qt.WindowModal)
        arduino_valves.show()
        arduino_valves.closedInform.connect(self.reshow_window)
        # arduino_valves.activateWindow()
        self.hide()

    def reshow_window(self):
        self.show()