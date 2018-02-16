from PyQt4.QtGui import QMainWindow
import MainWindow
import arduinoValvulas


class MainWindowStart(QMainWindow, MainWindow.Ui_MainWindow):
    def __init__(self, parent=None):
        super(MainWindowStart, self).__init__(parent)
        self.setupUi(self)
        self.geometry = None
        self.state = None
        self.btn_yes.clicked.connect(self.start_valve_window)
        self.btn_no.clicked.connect(self.close)

    def start_valve_window(self):
        arduino_valves = arduinoValvulas.ValvulasMainWindow(self)
        # arduino_valves.setWindowFlags(Qt.WindowStaysOnTopHint)

        # arduino_valves.setWindowModality(Qt.WindowModal)
        arduino_valves.show()
        arduino_valves.closedInform.connect(self.reshow_window)
        # arduino_valves.activateWindow()
        self.geometry = self.saveGeometry()
        self.state = self.saveState()
        self.hide()

    def reshow_window(self):
        self.restoreGeometry(self.geometry)
        self.restoreState(self.state)
        self.show()