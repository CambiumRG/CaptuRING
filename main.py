"""Main application entry-point for the CaptuRING GUI.

This module provides the `WindInterfaz` QWidget which wires the UI
(`Ui_interfaz`) to database parameters and the Arduino control helpers
(`placeSample`, `takeSamples`). It also exposes `createDB()` to ensure the
database exists before the GUI starts.

Notes / Requirements:
- This application expects a POSIX-like environment for the serial port
    path used in `createSample()` (currently '/dev/ttyUSB0').
- External tools such as `gphoto2` are used by the capture routines (in
    `arduino.pruebaSerial`) and must be installed separately.
"""

from PyQt5 import QtWidgets as qtw
from interfaz.interfaz import Ui_interfaz
from db.controllerDB import createDataBase, getParams, changeData
from arduino.pruebaSerial import placeSample, takeSamples
import os
import serial
import errno

class WindInterfaz(qtw.QWidget):
    """Main widget that connects UI controls to backend actions.

    The widget initializes the UI from saved parameters, wires control
    signals (value changes and button clicks) to database updates and
    action handlers, and exposes methods to create a sample and trigger
    the image capture workflow.
    """

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
        """Read and validate the core name from the UI and prepare output dir.

        Reads the `nameCore` text field, stores `coreName` and `corePath`
        as module-level globals, and ensures the output directory exists.
        If the name is invalid or empty, a critical message box is shown.

        Side effects:
            - Creates `Outputs/<coreName>` directory when necessary.
            - Shows QMessageBox dialogs for errors, info, or warnings.
        """
        global coreName
        coreName = self.ui.nameCore.text()
        global corePath
        corePath = "Outputs/" + coreName

        if coreName.strip() == "" or coreName.strip() == "None":
            qtw.QMessageBox.critical(
                self, "Fail", "No valid name for the core.")
            # Keep the capture button disabled when the name is invalid
            try:
                self.ui.crearMuestra.setEnabled(False)
            except Exception:
                pass
        else:
                if not os.path.isdir(corePath):
                    qtw.QMessageBox.information(
                    self, "New directory", 'The Sample Name folder does not exist. New one created.')
                    try:
                        os.mkdir(corePath)
                    except OSError as exc:
                        if exc.errno != errno.EEXIST:
                            pass
                else:
                    qtw.QMessageBox.warning(
                    self, "Duplicated Name",'New images will overwrite the existing ones.\n Are you sure to continue?')
        # If we arrive here the core name was accepted/processed — enable capture
        try:
            self.ui.crearMuestra.setEnabled(True)
        except Exception:
            pass


    def createSample(self):
        """Open a serial connection, position the stage, and run acquisition.

        This method opens a serial connection to the motion controller
        (currently hard-coded to '/dev/ttyUSB0' at 250000 baud), validates
        that a `coreName` has been set, runs `placeSample()` to move the
        stage to the start position, prompts the user for placement
        confirmation, and if accepted runs `takeSamples()` to perform the
        capture routine.

        Side effects:
            - Opens a serial connection and passes it to `placeSample` and
              `takeSamples` which will close it when finished.
            - Shows QMessageBox dialogs to communicate status and prompt
              the user for confirmation.
            - Uses UI fields for motor and sample parameters.
        """
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
    """Ensure the database file exists and initialize it if needed.

    Checks for the presence of `.CaptuRING.db` in the current working
    directory and calls `createDataBase()` to create it if absent.
    """
    if not os.path.isfile('.CaptuRING.db'):
        createDataBase()


if __name__ == "__main__":
    app = qtw.QApplication([])
    createDB()
    widget = WindInterfaz()
    widget.show()
    app.exec_()
