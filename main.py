# Required libraries for the complete tool:
## os, serial, errno, gphoto2 (run as subprocess), time, math, subprocess, PyQt5, sqlite3

from PyQt5 import QtWidgets as qtw
from interfaz.interfaz import Ui_interfaz
from db.controllerDB import createDataBase, getParams, changeData
from arduino.pruebaSerial import placeSample, takeSamples
import os
import serial
import errno # TODO Confirm adequate use


#TODO Interface options from lab computer
class WindInterfaz(qtw.QWidget):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.ui = Ui_interfaz()
        params = getParams()
        self.ui.setupUi(self, params)

        # control parameters
        self.ui.offset.valueChanged.connect(
            lambda: changeData("OFFSET", self.ui.offset.value()))
        self.ui.stepSpeed.valueChanged.connect(
            lambda: changeData("SPEED_STEP", self.ui.stepSpeed.value()))
        self.ui.initSpeed.valueChanged.connect(
            lambda: changeData("INITIAL_SPEED", self.ui.initSpeed.value()))
        self.ui.tamanioMuestra.valueChanged.connect(
            lambda: changeData("SAMPLE_SIZE", self.ui.tamanioMuestra.value()))
        self.ui.sizeStep.valueChanged.connect(
            lambda: changeData("SIZE_STEP", self.ui.sizeStep.value()))
        self.ui.tamanioHusillo.valueChanged.connect(
            lambda: changeData("SPINDLE_SIZE", self.ui.tamanioHusillo.value()))
        self.ui.platform.valueChanged.connect(
            lambda: changeData("PLATFORM", self.ui.platform.value()))
        self.ui.newcoreName.clicked.connect(self.coreNamef)
        self.ui.crearMuestra.clicked.connect(lambda: self.createSample())

    def coreNamef(self):
        global coreName
        coreName = self.ui.nameCore.text()
        global corePath
        corePath = "Outputs/" + coreName

        if coreName.strip() == "" or coreName.strip() == "None":
            qtw.QMessageBox.critical(
                self, "Fail", "No valid name for the core.")
        else:
                if not os.path.isdir(dirPath):
                    qtw.QMessageBox.information(
                    self, "New directory", 'The Sample Name folder does not exist. New one created.')
                    try:
                        os.mkdir(dirPath)
                    except OSError as exc:
                        if exc.errno != errno.EEXIST:
                            pass
                else:
                    qtw.QMessageBox.warning(
                    self, "Duplicated Name",'New images will overwrite the existing ones.\n Are you sure to continue?')


    def createSample(self):
        conn = serial.Serial('/dev/ttyUSB0', 250000, timeout=1, exclusive=True)
        aux = True
        reply = qtw.QMessageBox

        ###
        try:
            coreName
        except NameError:
            qtw.QMessageBox.critical(
                self, "Incorrect Core Name", "Input a valid (alphanumeric) Core Name.")
        else:

            if coreName.strip() == '' or coreName.strip() == "None":
                qtw.QMessageBox.critical(
                    self, "Empty Core Name", "Input a valid (alphanumeric) Core Name.")

            else:

                placeSample(conn,
                            self.ui.offset.value(),
                            self.ui.initSpeed.value(),
                            self.ui.tamanioMuestra.value(),
                            self.ui.tamanioHusillo.value(),
                            self.ui.platform.value())

                reply = qtw.QMessageBox.information(
                    self, "Check placement", "Is the sample correctly placed?", qtw.QMessageBox.Yes, qtw.QMessageBox.No)

                if reply == qtw.QMessageBox.Yes:
                    takeSamples(conn,
                                self.ui.offset.value(),
                                self.ui.stepSpeed.value(),
                                self.ui.tamanioMuestra.value(),
                                self.ui.sizeStep.value(),
                                self.ui.tamanioHusillo.value(),
                                self.ui.platform.value(),
                                ##
                                coreName)

                    reply2 = qtw.QMessageBox.information(
                        self, "Task finished", "Image shooting finished", qtw.QMessageBox.Ok)

                else:
                    reply3 = qtw.QMessageBox.critical(
                        self, "Incorrect placement", "Fix the core correctly and retry", qtw.QMessageBox.Ok)


def createDB():
    if not os.path.isfile('.CaptuRING.db'):
        createDataBase()


if __name__ == "__main__":
    app = qtw.QApplication([])
    createDB()
    widget = WindInterfaz()
    widget.show()
    app.exec_()
