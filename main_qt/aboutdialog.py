from PyQt4.QtGui import QMainWindow
import About_Dialog


class AboutDialog(QMainWindow, About_Dialog.Ui_Dialog):
    def __init__(self, parent=None):
        super(AboutDialog, self).__init__(parent)
        self.setupUi(self)

