from PyQt4.QtCore import (QUrl, Qt)
from PyQt4.QtGui import (QAction, QApplication, QDialog, QIcon,
        QKeySequence, QLabel, QTextBrowser, QToolBar, QVBoxLayout)

class HelpForm(QDialog):

    def __init__(self, page, parent=None):
        super(HelpForm, self).__init__(parent)
        self.setAttribute(Qt.WA_DeleteOnClose)
        self.setAttribute(Qt.WA_GroupLeader)
        self.create_widgets()
        self.layout_widgets()
        self.create_connections()
        self.textBrowser.setSearchPaths([":/help"])
        self.textBrowser.setSource(QUrl(page))
        self.resize(450, 400)
        self.setWindowTitle("{0} Help".format(
            QApplication.applicationName()))

    def create_widgets(self):
        self.backAction = QAction(QIcon(":/back.png"), "&Atras", self)
        self.backAction.setShortcut(QKeySequence.Back)
        self.homeAction = QAction(QIcon(":/home.png"), "&Inicio", self)
        self.homeAction.setShortcut("Inicio")
        self.pageLabel = QLabel()

        self.toolBar = QToolBar()
        self.toolBar.addAction(self.backAction)
        self.toolBar.addAction(self.homeAction)
        self.toolBar.addWidget(self.pageLabel)
        self.textBrowser = QTextBrowser()

    def layout_widgets(self):
        layout = QVBoxLayout()
        layout.addWidget(self.toolBar)
        layout.addWidget(self.textBrowser, 1)
        self.setLayout(layout)

    def create_connections(self):
        self.backAction.triggered.connect(self.textBrowser.backward)
        self.homeAction.triggered.connect(self.textBrowser.home)
        self.textBrowser.sourceChanged.connect(self.updatePageTitle)

    def updatePageTitle(self):
        self.pageLabel.setText(self.textBrowser.documentTitle())


if __name__ == "__main__":
    import sys

    app = QApplication(sys.argv)
    form = HelpForm("Help.html")
    form.show()
    app.exec_()

