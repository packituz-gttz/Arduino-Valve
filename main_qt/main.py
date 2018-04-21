import sys
from PyQt4.QtGui import QApplication, QIcon, QPixmap, QSplashScreen
from PyQt4.QtCore import Qt
import resources_rc


def main():
    app = QApplication(sys.argv)
    # Show SplashScreen
    splash_pixmap = QPixmap(':/cover.png')
    splash_screen = QSplashScreen(splash_pixmap, Qt.WindowStaysOnTopHint)
    splash_screen.show()

    app.processEvents()
    # Runtime imports
    import Valves_Main
    import time
    app.processEvents()
    app.setOrganizationName('Gatituz PK')
    app.setOrganizationDomain('http://gatituzmes-server.duckdns.org/')
    app.setApplicationName('VAL 518')
    app.processEvents()
    window = Valves_Main.MainWindowStart()
    app.setWindowIcon(QIcon(":/logo.png"))
    app.processEvents()

    app.processEvents()
    time.sleep(2)
    app.processEvents()
    time.sleep(1)
    app.processEvents()
    time.sleep(1)
    window.showMaximized()
    splash_screen.close()

    # Execute app
    app.exec_()


if __name__ == '__main__':
    main()
