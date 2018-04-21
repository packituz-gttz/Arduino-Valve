# -*- coding: utf-8 -*-
import os
import serial
import serial.tools.list_ports
from PyQt4.QtCore import (Qt, pyqtSignature, QSignalMapper, QRegExp, QThread, QEvent, QObject, QString, QMutex,
                          QWaitCondition)
from PyQt4.QtCore import pyqtSignal as Signal
from PyQt4.QtGui import (QMainWindow, QFileDialog, QKeySequence, QRegExpValidator, QLabel, QFrame, QIcon, QAction,
                         QComboBox, QMessageBox, QProgressDialog, QPixmap)
import MainWindow_Pro
import resources
import logging
import helpform
import aboutdialog

logging.basicConfig(level=logging.DEBUG, format=' %(asctime)s - %(levelname)s => %(message)s')
logging.debug('Start of program')


wait_condition = QWaitCondition()
mutex = QMutex()

class Connection_TimeOut_Arduino(Exception):
    pass


class Connection_Successful_Arduino(Exception):
    pass


class Uncompatible_Data(Exception):
    pass


class Connection_Killed(Exception):
    pass


class Saved_Canceled(Exception):
    pass


class Saved_Accepted(Exception):
    pass


class Connection_Stopped(Exception):
    pass


class MainWindowStart(QMainWindow, MainWindow_Pro.Ui_MainWindow):
    def __init__(self, parent=None):
        super(MainWindowStart, self).__init__(parent)
        self.myMapper = QSignalMapper(self)
        self.myMapper_StyleSheet = QSignalMapper(self)
        self.setupUi(self)

        self.regex_edits = QRegExp(r"(^[0]+$|^$)")
        self._filter = Filter()
        self.filename = QString()
        self.edit1_delayh.installEventFilter(self._filter)
        self.sizeLabel = QLabel()
        self.sizeLabel.setFrameStyle(QFrame.StyledPanel | QFrame.Sunken)
        self.statusBar1.addPermanentWidget(self.sizeLabel)
        self.statusBar1.setSizeGripEnabled(False)

        self.create_connections()
        self.assign_shortcuts()

        self.create_tool_bar()
        self.update_devices_list()
        # self.button_stop.clicked.connect(self.stop_all)
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

    def assign_shortcuts(self):
        self.actionArchivo_Nuevo.setShortcut(QKeySequence.New)
        self.action_Abrir.setShortcut(QKeySequence.Open)
        self.action_Guardar.setShortcut(QKeySequence.Save)
        self.actionGuardar_Como.setShortcut(QKeySequence.SaveAs)
        self.action_Limpiar.setShortcut('Ctrl+L')
        self.actionVAL_508_Ayuda.setShortcut(QKeySequence.HelpContents)
        self.action_Salir.setShortcut(QKeySequence.Close)
        # self.actionPreferencias.setShortcut(QKeySequence.Preferences)

        self.action_Detener_USB.setShortcut('Ctrl+Shift+C')
        self.action_Ejecutar.setShortcut('Ctrl+Shift+X')
        self.action_Para_Valvulas.setShortcut('Ctrl+Shift+P')

    def create_connections(self):
        self.actionArchivo_Nuevo.triggered.connect(self.new_file)
        self.action_Abrir.triggered.connect(self.open_file)
        self.action_Guardar.triggered.connect(self.save_file)
        self.actionGuardar_Como.triggered.connect(self.save_file_as)
        self.action_Limpiar.triggered.connect(self.clean_fields)
        self.action_Salir.triggered.connect(self.close)
        self.actionPreferencias.triggered.connect(self.settings)
        self.actionVAL_508_Ayuda.triggered.connect(self.show_help)
        self.actionAcerca_de_VAL_508.triggered.connect(self.show_about)

        self.action_Detener_USB.triggered.connect(self.stop_usb)
        self.action_Ejecutar.triggered.connect(self.execute)
        self.action_Para_Valvulas.triggered.connect(self.stop_all)

    def show_about(self):
        about = aboutdialog.AboutDialog(self)
        about.show()

    def show_help(self):
        form = helpform.HelpForm('Help.html', self)
        form.show()

    def new_file(self):
        self.filename = QString()
        self.clean_fields()

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
        filename_copy = self.filename
        logging.info("Current filename: %s" % self.filename)
        my_home = os.path.expanduser('~')
        self.filename = QFileDialog.getSaveFileName(self, self.tr('Guardar como'), os.path.join(my_home, "archivo.txt"), "", "",
                                                    QFileDialog.DontUseNativeDialog)
        logging.info("Filename to save: %s" % self.filename)
        if not self.filename.isNull():
            if self.filename.endsWith(QString('.txt')):
                self.write_data_to_file('w')
            else:
                self.filename.append(QString('.txt'))
                messageBox = QMessageBox(self)
                messageBox.setStyleSheet('QMessageBox QLabel {font: bold 14pt "Cantarell";}')
                messageBox.setWindowTitle(self.tr('Advertencia'))
                messageBox.setText(self.tr(u"El archivo ya existe, ¿Reemplazar?"))
                messageBox.setStandardButtons(QMessageBox.Yes|QMessageBox.No)
                messageBox.setIconPixmap(QPixmap(':/broken_file.png'))
                if messageBox.exec_() == QMessageBox.Yes:
                    self.write_data_to_file('w')
                else:
                    try:
                        while True:
                            self.filename = QFileDialog.getSaveFileName(self, self.tr('Guardar como'),
                                                                    os.path.join(my_home, "archivo.txt"), "", "",
                                                                    QFileDialog.DontUseNativeDialog)
                            if self.filename.isNull():
                                raise Saved_Canceled()
                            else:
                                messageBox = QMessageBox(self)
                                messageBox.setStyleSheet('QMessageBox QLabel {font: bold 14pt "Cantarell";}')
                                messageBox.setWindowTitle(self.tr('Advertencia'))
                                messageBox.setText(self.tr(u"El archivo ya existe, ¿Reemplazar?"))
                                messageBox.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
                                messageBox.setIconPixmap(QPixmap(':/broken_file.png'))
                                if messageBox.exec_() == QMessageBox.Yes:
                                    self.write_data_to_file('w')
                                    raise Saved_Accepted()
                    except Saved_Canceled:
                        self.filename = filename_copy
                    except Saved_Accepted:
                        pass
        logging.info("Current filename after operation: %s" % self.filename)

    def save_file(self):
        if self.filename.isNull():
            self.save_file_as()
        else:
            self.write_data_to_file('w')

    def execute(self):
        string_data = ''
        list_strings = []
        if str(self.arduino_combobox.currentText()):
            self.statusBar1.showMessage(self.tr('Conectando...'))
            for elem_edit in self.lineEdits_list:
                # delay
                string_data = string_data + str(((int(elem_edit[0].text()) * 3600) + (int(elem_edit[1].text()) * 60)
                                                 + (int(elem_edit[2].text()))) * 1000) + ';'
                # ON
                string_data = string_data + str(((int(elem_edit[3].text()) * 3600) + (int(elem_edit[4].text()) * 60)
                                                 + (int(elem_edit[5].text()))) * 1000) + ';'
                # OFF
                string_data = string_data + str(((int(elem_edit[6].text()) * 3600) + (int(elem_edit[7].text()) * 60)
                                                 + (int(elem_edit[8].text()))) * 1000) + ';'
                # Total
                string_data = string_data + str(((int(elem_edit[9].text()) * 3600) + (int(elem_edit[10].text()) * 60)
                                                 + (int(elem_edit[11].text()))) * 1000) + ';'

                list_strings.append(string_data)
                string_data = ''

            self.thread_connection = Arduino_Communication(str(self.arduino_combobox.currentText()), list_strings)
            self.thread_connection.start()
            self.action_Ejecutar.setEnabled(False)
            self.action_Para_Valvulas.setEnabled(False)

            # self.btn_execute.setEnabled(False)
            # self.button_stop.setEnabled(False)
            self.thread_connection.finished.connect(self.finished_thread)
            self.thread_connection.connection_exit_status.connect(self.finished_thread)
        else:
            messageBox = QMessageBox(self)
            messageBox.setStyleSheet('QMessageBox QLabel {font: bold 14pt "Cantarell";}')
            messageBox.setWindowTitle(self.tr('Advertencia'))
            messageBox.setText(self.tr("Arduino no seleccionado"))
            messageBox.setStandardButtons(QMessageBox.Ok)
            messageBox.setIconPixmap(QPixmap(':/usb_error.png'))
            messageBox.exec_()
            # QMessageBox.warning(self, self.tr('Advertencia'), self.tr("Arduino no seleccionado"), QMessageBox.Ok)

    def stop_usb(self):
        if str(self.arduino_combobox.currentText()):
            try:
                self.statusBar1.showMessage(self.tr(u'Conexión detenida'))
                if self.thread_connection.isRunning():
                    mutex.lock()
                    self.thread_connection.kill_serial = True
                    mutex.unlock()
                    # self.thread_connection.terminate()
            except AttributeError:
                logging.debug("Thread not running \'disconnected! \'")
        else:
            messageBox = QMessageBox(self)
            messageBox.setStyleSheet('QMessageBox QLabel {font: bold 14pt "Cantarell";}')
            messageBox.setWindowTitle(self.tr('Advertencia'))
            messageBox.setText(self.tr("Arduino no seleccionado"))
            messageBox.setStandardButtons(QMessageBox.Ok)
            messageBox.setIconPixmap(QPixmap(':/usb_error.png'))
            messageBox.exec_()

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
        self.label_arduino = QLabel(self.tr('Dispositivos: '))
        self.toolBar.addWidget(self.label_arduino)

        self.arduino_combobox = QComboBox()
        self.arduino_combobox.setToolTip(self.tr('Seleccionar Arduino'))
        self.arduino_combobox.setFocusPolicy(Qt.NoFocus)
        # self.arduino_combobox.activated.connect(self.updateChoosenArduino)

        # Update List of Arduino devices
        self.reload = QAction(QIcon(":/reload.png"), self.tr("&Refrescar"), self)
        self.reload.setShortcut(QKeySequence.Refresh)
        self.reload.setToolTip(self.tr('Refrescar Dispositivos'))
        self.reload.triggered.connect(self.update_devices_list)

        self.toolBar.addWidget(self.arduino_combobox)
        self.toolBar.addAction(self.reload)

    def update_devices_list(self):
        device_list = serial.tools.list_ports.comports()
        current_arduino = self.arduino_combobox.currentText()
        self.arduino_combobox.clear()
        for device_index, device in enumerate(sorted(device_list)):
            self.arduino_combobox.addItem(device.device)
            if device.device == current_arduino:
                self.arduino_combobox.setCurrentIndex(device_index)

    def stop_all(self):
        if str(self.arduino_combobox.currentText()):
            self.thread_connection = Arduino_Communication(str(self.arduino_combobox.currentText()))
            self.thread_connection.start()
            self.action_Ejecutar.setEnabled(False)
            self.action_Para_Valvulas.setEnabled(False)
            self.action_Detener_USB.setEnabled(False)
            # self.btn_execute.setEnabled(False)
            # self.button_stop.setEnabled(False)
            # self.btn_stop_usb.setEnabled(False)
            self.thread_connection.finished.connect(self.finished_thread)
            self.thread_connection.connection_exit_status.connect(self.finished_thread)
        else:
            messageBox = QMessageBox(self)
            messageBox.setStyleSheet('QMessageBox QLabel {font: bold 14pt "Cantarell";}')
            messageBox.setWindowTitle(self.tr('Advertencia'))
            messageBox.setText(self.tr("Arduino no seleccionado"))
            messageBox.setStandardButtons(QMessageBox.Ok)
            messageBox.setIconPixmap(QPixmap(':/usb_error.png'))
            messageBox.exec_()

    def open_file(self):
        try:
            my_home = os.path.expanduser('~')
            file_name = QFileDialog.getOpenFileName(self, self.tr('Abrir archivo'), my_home, '*.txt', '*.txt',
                                                    QFileDialog.DontUseNativeDialog)
            logging.warning("file_name type: %s" % type(file_name))
            list_values = []
            if not file_name.isNull():
                with open(file_name) as fp:
                    for line in fp:
                        list_values.extend([line.replace('\n', '')])
                logging.info("List Content: %s" % list_values)
                count = 0
                for elems in self.lineEdits_list:
                    for inner_elem in elems:
                        if not unicode(list_values[count]).isdigit():
                            raise Uncompatible_Data()
                        inner_elem.setText(list_values[count])
                        count = count + 1
                self.filename = file_name
        except (IOError, OSError):
            messageBox = QMessageBox(self)
            messageBox.setStyleSheet('QMessageBox QLabel {font: bold 14pt "Cantarell";}')
            messageBox.setWindowTitle(self.tr('Error'))
            messageBox.setText(self.tr('No se pudo abrir el archivo'))
            messageBox.setStandardButtons(QMessageBox.Ok)
            messageBox.setIconPixmap(QPixmap(':/broken_file.png'))
            messageBox.exec_()
            # QMessageBox.critical(self, self.tr('Error'), self.tr('No se pudo abrir el archivo.'), QMessageBox.Ok)
        except (IndexError, Uncompatible_Data):
            messageBox = QMessageBox(self)
            messageBox.setStyleSheet('QMessageBox QLabel {font: bold 14pt "Cantarell";}')
            messageBox.setWindowTitle(self.tr('Error'))
            messageBox.setText(self.tr('Formato Incompatible'))
            messageBox.setStandardButtons(QMessageBox.Ok)
            messageBox.setIconPixmap(QPixmap(':/broken_file.png'))
            messageBox.exec_()

    def finished_thread(self, error=None,  message=''):
        if error == 'error':
            messageBox = QMessageBox(self)
            messageBox.setStyleSheet('QMessageBox QLabel {font: bold 14pt "Cantarell";}')
            messageBox.setWindowTitle(self.tr('Error'))
            messageBox.setText(message)
            messageBox.setStandardButtons(QMessageBox.Ok)
            messageBox.setIconPixmap(QPixmap(':/usb_error.png'))
            messageBox.exec_()
            # QMessageBox.critical(self, 'Error', message, QMessageBox.Ok)
            return
        elif error == 'success':
            messageBox = QMessageBox(self)
            messageBox.setStyleSheet('QMessageBox QLabel {font: bold 14pt "Cantarell";}')
            messageBox.setWindowTitle(self.tr(u'Éxito'))
            messageBox.setText(message)
            messageBox.setStandardButtons(QMessageBox.Ok)
            messageBox.setIconPixmap(QPixmap(':/usb_success.png'))
            messageBox.exec_()
            # QMessageBox.information(self, self.tr(u'Éxito'), message, QMessageBox.Ok)
            return
        elif error == 'stopped':
            messageBox = QMessageBox(self)
            messageBox.setStyleSheet('QMessageBox QLabel {font: bold 14pt "Cantarell";}')
            messageBox.setWindowTitle(self.tr(u'Éxito'))
            messageBox.setText(message)
            messageBox.setStandardButtons(QMessageBox.Ok)
            messageBox.setIconPixmap(QPixmap(':/success_general.png'))
            messageBox.exec_()
            return
        self.action_Ejecutar.setEnabled(True)
        self.action_Para_Valvulas.setEnabled(True)
        self.action_Detener_USB.setEnabled(True)
        # self.btn_execute.setEnabled(True)
        # self.button_stop.setEnabled(True)
        # self.btn_stop_usb.setEnabled(True)
        self.statusBar1.showMessage(self.tr('Finalizado'))

    def write_data_to_file(self, open_mode):
        progressDialog = QProgressDialog()
        progressDialog.setModal(True)
        progressDialog.setLabelText(self.tr('Guardando...'))
        progressDialog.setMaximum(8)
        progressDialog.setCancelButton(None)
        # self.save_data = SaveDataThread(listx,
        #                                                   listy, self.plot_settings['separator'], self.filename, self)
        # self.save_data.start()
        progressDialog.show()

        try:
            with open(unicode(self.filename), open_mode) as file_obj:
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
            progressDialog.close()
            # QMessageBox.critical(self, self.tr('Error'), self.tr('Error al guardar.'), QMessageBox.Ok)
            messageBox = QMessageBox(self)
            messageBox.setStyleSheet('QMessageBox QLabel {font: bold 14pt "Cantarell";}')
            messageBox.setWindowTitle(self.tr('Error'))
            messageBox.setText(self.tr('Error al guardar'))
            messageBox.setStandardButtons(QMessageBox.Ok)
            messageBox.setIcon(QMessageBox.Critical)
            messageBox.exec_()

        else:
            self.statusBar1.showMessage(self.tr('Guardado'), 3000)


class Arduino_Communication(QThread):
    # Custom Signal, inform GUI about the way the connection ended
    connection_exit_status = Signal(str, str)

    # Receives Arduino path and line_edits' text as a list
    def __init__(self, device=None, list_data=None, parent=None):
        super(Arduino_Communication, self).__init__(parent)
        self.device = device
        self.list_data = list_data
        self.serial_connection = None
        self.kill_serial = False

    def run(self):
        try:
            self.serial_connection = serial.Serial(self.device, 9600, timeout=4, write_timeout=4)
            # If list_data is empty it means we must stop the valves
            if not self.list_data:
                logging.info("None, kill all valves")
                # Sleep to prevent a dead-lock
                self.sleep(2)
                self.serial_connection.write("KILL")
                # self.serial_connection.flushOutput()
                raise Connection_Killed()
            else:
                # Send parameters for valves programming, KO cleans all vars on arduino
                self.list_data.insert(0, "KO")
                logging.warning("Appended KO to list_data" % self.list_data)
                for count, elem_string in enumerate(self.list_data, 0):
                    tries = 0
                    self.sleep(2)
                    logging.info("Post Sleep")
                    self.serial_connection.write(self.list_data[count])
                    logging.info("Post Write")
                    # self.serial_connection.flushOutput()
                    # Check data was sent correctly
                    # if data got corrupted, try to resend 4 times
                    while tries < 4:
                        mutex.lock()
                        if self.kill_serial:
                            mutex.unlock()
                            raise Connection_Stopped()
                        mutex.unlock()
                        data = self.serial_connection.readline()
                        # self.serial_connection.flushInput()
                        if data:
                            logging.debug("Data Sent: %s" % data)
                            if data.replace('\r\n', '') == self.list_data[count]:
                                logging.warning("OK, data returned %s:" % data)
                                self.serial_connection.write('OK')
                                # self.serial_connection.flushOutput()
                                # self.sleep(2)
                                break
                        logging.info("Data malformed, retrying %s" % tries)
                        tries = tries + 1
                    # Close connection if data corruption couldn't be corrected
                    if tries >= 4:
                        logging.error("Unable to send data due to corruption")
                        raise Connection_TimeOut_Arduino()
                # self.serial_connection.write('--DONE--')
        except (serial.SerialException, Connection_TimeOut_Arduino):
            logging.error("Unable to send data")
            try:
                # self.serial_connection.write('KO')
                self.serial_connection.close()
            except AttributeError:
                logging.info("Closed Serial because of error")
            finally:
                self.connection_exit_status.emit('error', self.tr(u"Error en conexión."))
        except Connection_Killed:
            self.connection_exit_status.emit('stopped', self.tr(u'Válvulas detenidas.'))
        except Connection_Stopped:
            pass
        else:
            self.connection_exit_status.emit('success', self.tr(u'Conexión exitosa.'))


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
