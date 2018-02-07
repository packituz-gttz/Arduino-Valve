import sys
from PyQt4.QtGui import QApplication, QIcon
from PyQt4.QtCore import QLocale, QTranslator
import arduinoValvulas
import resources


def main():
    app = QApplication(['Arduino Valvulas'])
    locale = QLocale.system().name()
    qtTranslator = QTranslator()
    print locale
    if qtTranslator.load("qt_" + locale, ":/"):
        app.installTranslator(qtTranslator)
    appTranslator = QTranslator()
    if appTranslator.load("valves_" + locale, ":/"):
        app.installTranslator(appTranslator)
    app.setOrganizationName('Gatituz PK')
    app.setOrganizationDomain('http://gatituzmes-server.duckdns.org/')
    window = arduinoValvulas.ValvulasMainWindow()
    app.setWindowIcon(QIcon(":/main.png"))
    window.show()
    app.exec_()

if __name__ == '__main__':
    main()