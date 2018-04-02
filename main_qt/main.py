import sys
from PyQt4.QtGui import QApplication, QIcon, QPixmap, QSplashScreen
from PyQt4.QtCore import Qt
import resources

def main():

    app = QApplication(sys.argv)

    splash_pixmap = QPixmap(':/cover.png')
    splash_screen = QSplashScreen(splash_pixmap, Qt.WindowStaysOnTopHint)
    # splash = QLabel("<font color=red>CARGANDO...</font>")
    # splash.setWindowFlags(Qt.SplashScreen)
    splash_screen.show()

    # Translation, implemented but won't be used for this version
    # locale = QLocale.system().name()
    # qtTranslator = QTranslator()
    # print locale
    # if qtTranslator.load("qt_" + locale, ":/"):
    #     app.installTranslator(qtTranslator)
    # appTranslator = QTranslator()
    # if appTranslator.load("valves_" + locale, ":/"):
    #     app.installTranslator(appTranslator)

    app.processEvents()
    # LOAD, QApplication
    import mainWindow
    import Valves_Main
    import time
    app.processEvents()
    app.setOrganizationName('Gatituz PK')
    app.setOrganizationDomain('http://gatituzmes-server.duckdns.org/')
    app.setApplicationName('VAL 518')
    app.processEvents()
#    window = mainWindow.MainWindowStart()
    window = Valves_Main.MainWindowStart()
    app.setWindowIcon(QIcon(":/logo.png"))
    app.processEvents()

    app.processEvents()
    # TODO Check loading speed
    time.sleep(2)
    app.processEvents()
    time.sleep(1)
    app.processEvents()
    time.sleep(1)
    window.showMaximized()
    splash_screen.close()
    # Exec app
    app.exec_()

if __name__ == '__main__':
    main()