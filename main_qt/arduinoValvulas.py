import os
import serial
import serial.tools.list_ports
from PyQt4.QtCore import (Qt, pyqtSignature, QSignalMapper, QRegExp, QThread, QEvent, QObject, QString)
from PyQt4.QtCore import pyqtSignal as Signal
from PyQt4.QtGui import (QMainWindow, QFileDialog, QKeySequence, QRegExpValidator, QLabel, QFrame, QIcon, QAction,
                         QComboBox, QMessageBox, QProgressDialog)
import Valvulas
import resources

class Connection_TimeOut_Arduino(Exception):
    pass


class Connection_Successful_Arduino(Exception):
    pass


class Uncompatible_Data(Exception):
    pass


# Main window imported from ui file
class Valvulas(QMainWindow,
               Valvulas.Ui_ValvulasMainWindow):
    def __init__(self, parent=None):
        super(Valvulas, self).__init__(parent)
        self.myMapper = QSignalMapper(self)
        self.setupUi(self)

        self._filter = Filter()
        self.filename = QString(u'')
        self.edit1_delayh.installEventFilter(self._filter)
        # self.btn_save.setShortcut(QKeySequence.SaveAs)
        # self.btn_save_2.setShortcut(QKeySequence.Save)
        self.sizeLabel = QLabel()
        self.sizeLabel.setFrameStyle(QFrame.StyledPanel | QFrame.Sunken)
        self.statusBar1.addPermanentWidget(self.sizeLabel)
        self.statusBar1.setSizeGripEnabled(False)
        # self.checkArduinoState()
        self.createToolBar()
        self.updateDevicesList()
        self.button_stop.clicked.connect(self.stop_all)
        # List of valve pushbuttons
        self.valve_list = [self.valve1, self.valve2, self.valve3, self.valve4,
                           self.valve5, self.valve6, self.valve7, self.valve8]

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

        #index = 1
        for index, editLabels in enumerate(self.lineEdits_list, 1):
            editLabels[0].installEventFilter(self._filter)
            editLabels[1].installEventFilter(self._filter)
            editLabels[2].installEventFilter(self._filter)
            editLabels[3].installEventFilter(self._filter)
            editLabels[4].installEventFilter(self._filter)
            editLabels[5].installEventFilter(self._filter)
            editLabels[6].installEventFilter(self._filter)
            editLabels[7].installEventFilter(self._filter)
            editLabels[8].installEventFilter(self._filter)
            editLabels[9].installEventFilter(self._filter)
            editLabels[10].installEventFilter(self._filter)
            editLabels[11].installEventFilter(self._filter)

            self.myMapper.setMapping(self.valve_list[index - 1], index)
            (self.valve_list[index - 1]).clicked.connect(self.myMapper.map)

            # Comment
            # self.myMapper.setMapping(editLabels[0], index)
            # editLabels[0].editingFinished.connect(self.myMapper.map)
            #
            # self.myMapper.setMapping(editLabels[1], index)
            # editLabels[1].returnPressed .connect(self.myMapper.map)
            #
            # self.myMapper.setMapping(editLabels[2], index)
            # editLabels[2].returnPressed.connect(self.myMapper.map)
            #
            # self.myMapper.setMapping(editLabels[3], index)
            # editLabels[3].returnPressed.connect(self.myMapper.map)
            #
            # self.myMapper.setMapping(editLabels[4], index)
            # editLabels[4].returnPressed.connect(self.myMapper.map)
            #
            # self.myMapper.setMapping(editLabels[5], index)
            # editLabels[5].returnPressed.connect(self.myMapper.map)
            #
            # index = index + 1
        self.myMapper.mapped['int'].connect(self.enable_fields)
        #self.myMapper.mapped['int'].connect(self.print_me)
        self.btn_stop_usb.clicked.connect(self.stop_usb)

    def stop_usb(self):
        try:
            print self.thread_connection.isRunning()
            if self.thread_connection.isRunning():
                self.thread_connection.terminate()
        except AttributeError:
            pass


    def stop_all(self):
        self.thread_connection = Arduino_Communication(str(self.arduino_combobox.currentText()))
        self.thread_connection.start()
        self.btn_execute.setEnabled(False)
        self.button_stop.setEnabled(False)
        self.thread_connection.finished.connect(self.finished_thread)
        self.thread_connection.connection_error.connect(self.finished_thread)
        self.thread_connection.connection_success.connect(self.finished_thread)

    def createToolBar(self):

        self.label_arduino = QLabel('Dispositivos: ')
        self.toolBar1.addWidget(self.label_arduino)

        self.arduino_combobox = QComboBox()
        self.arduino_combobox.setToolTip('Select Arduino')
        self.arduino_combobox.setFocusPolicy(Qt.NoFocus)
        # self.arduino_combobox.activated.connect(self.updateChoosenArduino)

        # Update List of Arduino devices
        self.reload = QAction(QIcon(":/reload.png"), "&Reload", self)
        self.reload.setShortcut(QKeySequence.Refresh)
        self.reload.setToolTip('Reload Devices')
        self.reload.triggered.connect(self.updateDevicesList)

        self.toolBar1.addWidget(self.arduino_combobox)
        self.toolBar1.addAction(self.reload)

    def updateDevicesList(self):
        device_list = serial.tools.list_ports.comports()
        current_arduino = self.arduino_combobox.currentText()
        self.arduino_combobox.clear()
        for device_index, device in enumerate(sorted(device_list)):
            self.arduino_combobox.addItem(device.device)
            if device.device == current_arduino:
                self.arduino_combobox.setCurrentIndex(device_index)

    # def calculateTime(self, index):
    #     pass
        #print index
        # counter = 0
        # hours = 0
        # minutes = 0
        # for line_edit in self.lineEdits_list[index - 1]:
        #     if line_edit.text():
        #         if counter < 6:
        #             if counter % 2 == 0:
        #                 hours = hours + int(line_edit.text())
        #             else:
        #                 minutes = minutes + int(line_edit.text())
        #             line_edit.setEnabled(self.valve_list[index - 1].isChecked())

        # elif counter == 6:
        #     line_edit.setText(str(hours))
        # elif counter == 7:
        #     if minutes > 59:
        #         print minutes
        #         hours = hours + (minutes / 60)
        #         minutes = minutes % 60
        #         self.lineEdits_list[index - 1][6].setText(str(hours))
        #         line_edit.setText(str(hours))
        #     line_edit.setText(str(minutes))

    #            counter = counter + 1

    @pyqtSignature("")
    def on_btn_save_clicked(self):
        self.saveFileAs()

    @pyqtSignature("")
    def on_btn_save_2_clicked(self):
        if self.filename.isEmpty():
            self.saveFileAs()
        else:
            self.writeDataToFile('w')

# TODO check line 427 flushInput() raised Exception IMPORTANT
# TODO change lineEdits to spinbox?
    # 1hr --> 3600 sec
    # 1min --> 60 sec
    # 1sec --> 1 sec
    # Sum them and multiply them by 1000
    @pyqtSignature("")
    def on_btn_execute_clicked(self):
        string_data = ''
        list_strings = []
        if str(self.arduino_combobox.currentText()):
            self.statusBar1.showMessage('Connecting...')
            for elem_edit in self.lineEdits_list:
                # delay
                string_data = string_data + str(((int(elem_edit[0].text()) * 3600) + (int(elem_edit[1].text()) * 60) \
                + (int(elem_edit[2].text()))) * 1000) + ';'
                # ON
                string_data = string_data + str(((int(elem_edit[3].text()) * 3600) + (int(elem_edit[4].text()) * 60) \
                                                 + (int(elem_edit[5].text()))) * 1000) + ';'
                # OFF
                string_data = string_data + str(((int(elem_edit[6].text()) * 3600) + (int(elem_edit[7].text()) * 60) \
                                                 + (int(elem_edit[8].text()))) * 1000) + ';'
                # Total
                string_data = string_data + str(((int(elem_edit[9].text()) * 3600) + (int(elem_edit[10].text()) * 60) \
                                                 + (int(elem_edit[11].text()))) * 1000) + ';'

                list_strings.append(string_data)
                string_data = ''

            self.thread_connection = Arduino_Communication(str(self.arduino_combobox.currentText()), list_strings)
            self.thread_connection.start()
            self.btn_execute.setEnabled(False)
            self.button_stop.setEnabled(False)
            self.thread_connection.finished.connect(self.finished_thread)
            self.thread_connection.connection_error.connect(self.finished_thread)
            self.thread_connection.connection_success.connect(self.finished_thread)
        else:
            QMessageBox.warning(self, 'Warning', 'No arduino selected', QMessageBox.Ok)

    def finished_thread(self, error=None):
        if error == 'error':
            QMessageBox.critical(self, 'Connection Error', "Error couldn't connect to arduino", QMessageBox.Ok)
            return
        elif error == 'success':
            QMessageBox.information(self, 'Connection Successful', "Connection to arduino was a success", QMessageBox.Ok)
            return
        self.btn_execute.setEnabled(True)
        self.button_stop.setEnabled(True)
        self.statusBar1.clear()

    @pyqtSignature("")
    def on_btn_open_clicked(self):
        self.openFile()

    # @pyqtSignature("")
    # def on_valve1_clicked(self):
    #     self.enable_fields(1)

    # @pyqtSignature("")
    # def on_valve2_clicked(self):
    #     self.enable_fields(2)
    #
    # @pyqtSignature("")
    # def on_valve3_clicked(self):
    #     self.enable_fields(3)
    #
    # @pyqtSignature("")
    # def on_valve4_clicked(self):
    #     self.enable_fields(4)
    #
    # @pyqtSignature("")
    # def on_valve5_clicked(self):
    #     self.enable_fields(5)
    #
    # @pyqtSignature("")
    # def on_valve6_clicked(self):
    #     self.enable_fields(6)
    #
    # @pyqtSignature("")
    # def on_valve7_clicked(self):
    #     self.enable_fields(7)
    #
    # @pyqtSignature("")
    # def on_valve8_clicked(self):
    #     self.enable_fields(8)

    # Enables/Disables lineedits for time inputs
    def enable_fields(self, index):
        hours_reg = QRegExp(r"([0-9])|([0-9][0-9][0-9])")
        sec_reg = QRegExp(r"([0-9])|([0-5][0-9])")
        for counter, line_edit in enumerate(self.lineEdits_list[index - 1]):
            # if counter < 6:
            line_edit.setEnabled(self.valve_list[index - 1].isChecked())
            if counter % 3 == 0:
                line_edit.setValidator(QRegExpValidator(hours_reg, self))
            else:
                line_edit.setValidator(QRegExpValidator(sec_reg, self))
        # if self.valve_list[index-1].isChecked():
        #     self.edit1_delayh.setEnabled(True)
        # else:
        #     self.edit1_delayh.setEnabled(False)

    # TODO add save button
    def saveFileAs(self):
        my_home = os.path.expanduser('~')
        self.filename = QFileDialog.getSaveFileName(self, 'Save As', os.path.join(my_home, "archivo.txt"), "", "",
                                                    QFileDialog.DontUseNativeDialog)
        print ("me", self.filename)
        if not self.filename.isNull():
            self.writeDataToFile('w')

    def writeDataToFile(self, open_mode):

        progressDialog = QProgressDialog()
        progressDialog.setModal(True)
        progressDialog.setLabelText('Saving...')
        progressDialog.setMaximum(8)
        progressDialog.setCancelButton(None)
        # self.save_data = SaveDataThread(listx,
        #                                                   listy, self.plot_settings['separator'], self.filename, self)
        # self.save_data.start()
        progressDialog.show()

        try:
            with open(self.filename, open_mode) as file_obj:
                for count, elem_edit in enumerate(self.lineEdits_list, 1):
                    file_obj.write(''.join([str(elem_edit[0].text()), '\n']))
                    file_obj.write(''.join([str(elem_edit[1].text()), '\n']))
                    file_obj.write(''.join([str(elem_edit[2].text()), '\n']))
                    file_obj.write(''.join([str(elem_edit[3].text()), '\n']))
                    file_obj.write(''.join([str(elem_edit[4].text()), '\n']))
                    file_obj.write(''.join([str(elem_edit[5].text()), '\n']))
                    file_obj.write(''.join([str(elem_edit[6].text()), '\n']))
                    file_obj.write(''.join([str(elem_edit[7].text()), '\n']))
                    file_obj.write(''.join([str(elem_edit[8].text()), '\n']))
                    file_obj.write(''.join([str(elem_edit[9].text()), '\n']))
                    file_obj.write(''.join([str(elem_edit[10].text()), '\n']))
                    file_obj.write(''.join([str(elem_edit[11].text()), '\n']))
                    progressDialog.setValue(count)
        except (IOError, OSError):
            QMessageBox.critical(self, 'Error', 'Error while saving.', QMessageBox.Ok)
        else:
            self.statusBar1.showMessage('Saved', 3000)

    def closeEvent(self, QCloseEvent):
        try:
            self.thread_connection.serial_connection.close()
            print "Closed"
        except AttributeError:
            print "Error closing"

    def openFile(self):
        # self.save_data = SaveDataThread(listx,
        #                                                   listy, self.plot_settings['separator'], self.filename, self)
        # self.save_data.start()
        try:
            my_home = os.path.expanduser('~')
            file_name = QFileDialog.getOpenFileName(self, 'Open File', my_home, '*.txt')
            list_values = []
            if not file_name.isNull():
                with open(file_name) as fp:
                    for line in fp:
                        list_values.extend([line.replace('\n', '')])

                print list_values
                count = 0
                for elems in self.lineEdits_list:
                    for inner_elem in elems:
                        if not unicode(list_values[count]).isdigit():
                            raise Uncompatible_Data()
                        inner_elem.setText(list_values[count])
                        count = count + 1

        except (IOError, OSError):
            QMessageBox.critical(self, 'Error', 'Unable to open file.', QMessageBox.Ok)
        except (IndexError, Uncompatible_Data):
            QMessageBox.warning(self, 'Warning', 'Uncompatible format', QMessageBox.Ok)

# TODO rebuild GUI and add Stop to Serial
class Arduino_Communication(QThread):
    connection_error = Signal(str)
    connection_success = Signal(str)

    def __init__(self, device=None, list_data='', parent=None):
        super(Arduino_Communication, self).__init__(parent)
        self.device = device
        self.list_data = list_data
        self.serial_connection = None

    def run(self):
        try:
            self.serial_connection = serial.Serial(self.device, 9600, timeout=4, write_timeout=4)
            if not self.list_data:
                print "None, kill all valves"
                self.sleep(2)
                self.serial_connection.write("KILL")
                self.serial_connection.flushOutput()
                # raise Connection_Killed()
            else:
                print self.list_data
                for count, elem_string in enumerate(self.list_data, 0):
                    tries = 0
                    self.sleep(2)
                    print "post sleep"
                    self.serial_connection.write(self.list_data[count])
                    print "post write"
                    # self.serial_connection.flushOutput()
                    while tries < 4:
                        data = self.serial_connection.readline()
                        # self.serial_connection.flushInput()
                        if data:
                            if data.replace('\r\n', '') == self.list_data[count]:
                                print ("receive", data)
                                self.serial_connection.write('OK')
                                # self.serial_connection.flushOutput()
                                # self.sleep(2)
                                break
                        print "err data me"
                        tries = tries + 1

                    if tries >= 4:
                        print "retries err"
                        raise Connection_TimeOut_Arduino()
                # self.serial_connection.write('--DONE--')
        # TODO Check if KO is still used
        except (serial.SerialException, Connection_TimeOut_Arduino):
            print "closed err"
            try:
                #TODO check if this affects
                # self.serial_connection.write('KO')
                self.serial_connection.close()
            except AttributeError:
                print "No such object"
            print "err"
            self.connection_error.emit('error')
        else:
            self.connection_success.emit('success')





class Filter(QObject):
    def eventFilter(self, widget, event):
        # FocusOut event
        if event.type() == QEvent.FocusOut:
            # do custom stuff
            print 'focus out'
            if widget.text() == '':
                widget.setText('0')
            # return False so that the widget will also handle the event
            # otherwise it won't focus out
            return False
        else:
            # we don't care about other events
            return False