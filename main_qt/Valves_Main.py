# -*- coding: utf-8 -*-
import os
import serial
import serial.tools.list_ports
from PyQt4.QtCore import (Qt, pyqtSignature, QSignalMapper, QRegExp, QThread, QEvent, QObject, QString)
from PyQt4.QtCore import pyqtSignal as Signal
from PyQt4.QtGui import (QMainWindow, QFileDialog, QKeySequence, QRegExpValidator, QLabel, QFrame, QIcon, QAction,
                         QComboBox, QMessageBox, QProgressDialog, QPixmap)
import MainWindow_Pro
import resources
import logging

logging.basicConfig(level=logging.DEBUG, format=' %(asctime)s - %(levelname)s => %(message)s')
logging.debug('Start of program')


class Connection_TimeOut_Arduino(Exception):
    pass


class Connection_Successful_Arduino(Exception):
    pass


class Uncompatible_Data(Exception):
    pass


class Connection_Killed(Exception):
    pass


class MainWindowStart(QMainWindow, MainWindow_Pro.Ui_MainWindow):
    def __init__(self, parent=None):
        super(MainWindowStart, self).__init__(parent)
        self.myMapper = QSignalMapper(self)
        self.myMapper_StyleSheet = QSignalMapper(self)
        self.setupUi(self)

        self.regex_edits = QRegExp(r"(^[0]+$|^$)")
        self._filter = Filter()
        self.filename = QString(u'')
        self.edit1_delayh.installEventFilter(self._filter)
        self.sizeLabel = QLabel()
        self.sizeLabel.setFrameStyle(QFrame.StyledPanel | QFrame.Sunken)
        self.statusBar1.addPermanentWidget(self.sizeLabel)
        self.statusBar1.setSizeGripEnabled(False)

        self.create_connections()

        self.create_tool_bar()
        self.update_devices_list()
        #self.button_stop.clicked.connect(self.stop_all)
        # List of valve pushbuttons
        self.valve_list = [self.valve1, self.valve2, self.valve3, self.valve4,
                           self.valve5, self.valve6, self.valve7, self.valve8]

        self.group_boxes = [self.groupbox1, self.groupbox2, self.groupbox3, self.groupbox4, self.groupbox5,
                            self.groupbox6, self.groupbox7, self.groupbox8]

        self.lineEdits_list = [(self.edit1_delayh, self.edit1_delaym, self.edit1_delays,
                                self.edit1_onh, self.edit1_onm, self.edit1_ons,
                                self.edit1_offh, self.edit1_offm, self.edit1_offs,
                                self.edit1_totalh, self.edit1_totalm, self.edit1_totals),

                               (self.edit2_delayh, self.edit2_delaym, self.edit2_delays,
                                self.edit2_onh, self.edit2_onm, self.edit2_ons,
                                self.edit2_offh, self.edit2_offm, self.edit2_offs,
                                self.edit2_totalh, self.edit2_totalm, self.edit2_totals),

                               (self.edit3_delayh, self.edit3_delaym, self.edit3_delays,
                                self.edit3_onh, self.edit3_onm, self.edit3_ons,
                                self.edit3_offh, self.edit3_offm, self.edit3_offs,
                                self.edit3_totalh, self.edit3_totalm, self.edit3_totals),

                               (self.edit4_delayh, self.edit4_delaym, self.edit4_delays,
                                self.edit4_onh, self.edit4_onm, self.edit4_ons,
                                self.edit4_offh, self.edit4_offm, self.edit4_offs,
                                self.edit4_totalh, self.edit4_totalm, self.edit4_totals),

                               (self.edit5_delayh, self.edit5_delaym, self.edit5_delays,
                                self.edit5_onh, self.edit5_onm, self.edit5_ons,
                                self.edit5_offh, self.edit5_offm, self.edit5_offs,
                                self.edit5_totalh, self.edit5_totalm, self.edit5_totals),

                               (self.edit6_delayh, self.edit6_delaym, self.edit6_delays,
                                self.edit6_onh, self.edit6_onm, self.edit6_ons,
                                self.edit6_offh, self.edit6_offm, self.edit6_offs,
                                self.edit6_totalh, self.edit6_totalm, self.edit6_totals),

                               (self.edit7_delayh, self.edit7_delaym, self.edit7_delays,
                                self.edit7_onh, self.edit7_onm, self.edit7_ons,
                                self.edit7_offh, self.edit7_offm, self.edit7_offs,
                                self.edit7_totalh, self.edit7_totalm, self.edit7_totals),

                               (self.edit8_delayh, self.edit8_delaym, self.edit8_delays,
                                self.edit8_onh, self.edit8_onm, self.edit8_ons,
                                self.edit8_offh, self.edit8_offm, self.edit8_offs,
                                self.edit8_totalh, self.edit8_totalm, self.edit8_totals)]

        # index = 1
        for index, editLabels in enumerate(self.lineEdits_list, 1):

            for index2, lineedits in enumerate(editLabels, 0):
                self.myMapper_StyleSheet.setMapping(self.lineEdits_list[index - 1][index2], index - 1)
                (self.lineEdits_list[index - 1][index2]).textChanged.connect(self.myMapper_StyleSheet.map)
                self.lineEdits_list[index - 1][index2].installEventFilter(self._filter)

            self.myMapper.setMapping(self.valve_list[index - 1], index)
            (self.valve_list[index - 1]).clicked.connect(self.myMapper.map)

        self.myMapper.mapped['int'].connect(self.enable_fields)
        self.myMapper_StyleSheet.mapped['int'].connect(self.valve_color_status)
        # self.myMapper.mapped['int'].connect(self.print_me)
#        self.btn_stop_usb.clicked.connect(self.stop_usb)
        # self.edit1_delayh.textChanged.connect(self.valve_color_status)

    def create_connections(self):
        self.action_Abrir.triggered.connect(self.open_file)
        self.action_Guardar.triggered.connect(self.save_file)
        self.actionGuardar_Como.triggered.connect(self.save_file_as)
        self.action_Limpiar.triggered.connect(self.clean_fields)
        self.action_Salir.triggered.connect(self.close)

        self.action_Detener_USB.triggered.connect(self.stop_usb)
        self.action_Ejecutar.triggered.connect(self.execute)
        self.action_Para_Valvulas.triggered.connect(self.stop_all)


    def closeEvent(self, QCloseEvent):
        try:
            self.closedInform.emit()
            self.thread_connection.serial_connection.close()
            logging.debug("Thread running and killed at closing program")
        except AttributeError:
            logging.debug("Thread was not running when closing program OK")



    def clean_fields(self):
        for index, editLabels in enumerate(self.lineEdits_list, 1):
            for index2, lineedits in enumerate(editLabels, 0):
                self.lineEdits_list[index - 1][index2].setText('0')

    def save_file_as(self):
        pass

    def save_file(self):
        pass

    def execute(self):
        pass

    def stop_usb(self):
        pass

    def enable_fields(self, index):
        # hours_reg = QRegExp(r"([0-9])|([0-9][0-9][0-9])")
        hours_reg = QRegExp(r"0*[0-9]{1,3}")
        sec_reg = QRegExp(r"(0*[0-9])|(0*[0-5][0-9])")
        for counter, line_edit in enumerate(self.lineEdits_list[index - 1]):
            # if counter < 6:
            line_edit.setEnabled(self.valve_list[index - 1].isChecked())
            if counter % 3 == 0:
                line_edit.setValidator(QRegExpValidator(hours_reg, self))
            else:
                line_edit.setValidator(QRegExpValidator(sec_reg, self))

    def valve_color_status(self, index):
        logging.info("Checking color from valve button")
        for edit in self.lineEdits_list[index]:
            if edit.text().contains(self.regex_edits):
                self.group_boxes[index].setStyleSheet('''QGroupBox {
                                                      border: 2px solid;
                                                      border-color: rgba(255, 255, 255, 0);}''')
            else:
                # self.valve_list[index].setStyleSheet('background-color: rgb(29, 255, 36);')
                self.group_boxes[index].setStyleSheet('''QGroupBox {background-color: rgba(103, 255, 126, 150);
                                                      border: 2px solid;
                                                      border-color: rgba(255, 255, 255, 255);}''')
                break

    def create_tool_bar(self):
        pass

    def update_devices_list(self):
        pass

    def stop_all(self):
        pass

    def open_file(self):
        pass

# Filter for catching focus out event
class Filter(QObject):
    def eventFilter(self, widget, event):
        # FocusOut event
        if event.type() == QEvent.FocusOut:
            # do custom stuff
            if widget.text() == '':
                widget.setText('0')
            # return False so that the widget will also handle the event
            # otherwise it won't focus out
            return False
        else:
            # we don't care about other events
            return False
