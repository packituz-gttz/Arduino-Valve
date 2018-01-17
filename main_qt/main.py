import sys
from PyQt4.QtGui import QApplication
import arduinoValvulas

def main():
    app = QApplication(['Arduino Valvulas'])
    app.setOrganizationName('Gatituz PK')
    app.setOrganizationDomain('http://gatituzmes-server.duckdns.org/')
    window = arduinoValvulas.Valvulas()
    window.show()
    app.exec_()

if __name__ == '__main__':
    main()